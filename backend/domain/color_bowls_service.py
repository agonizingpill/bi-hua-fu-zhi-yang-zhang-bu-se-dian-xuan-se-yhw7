from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.queueing import submit, result
from core.records import get, insert, need, scan
from domain.proof_regions_model import proof_regions
from domain.dry_swatches_model import dry_swatches
from domain.shade_studies_model import shade_studies
from domain.patch_slots_model import patch_slots
from domain.color_bowls_model import color_bowls, bowl_claims


def _validated_points(conn, panel, points):
    from domain.proof_geometry import demand_point
    coords = [(p['x_mm'], p['y_mm']) for p in points]
    need(len(coords) >= 1 and len(set(coords)) == len(coords), '整组点坐标必须非空且不得重复')
    rows = [row for row in scan(conn, dry_swatches)
            if row['witnessed'] and row['family'] == panel['pigment_family']]
    need(len(rows) >= 12, '同色样册已验真干样不足 12 条')
    low, high = min(r['ground_l'] for r in rows), max(r['ground_l'] for r in rows)
    for point in points:
        demand_point(panel, point['x_mm'], point['y_mm'])
        need(low <= point['ground_l'] <= high, '该点底色亮度落在已测干样范围之外')
    return rows


def fit_bowl(conn, user, data):
    panel = get(conn, proof_regions, data.panel)
    points = [p.model_dump() for p in data.points]
    rows = _validated_points(conn, panel, points)
    return submit(user, {'studies': rows, 'panel': data.panel, 'revision': panel['revision'],
                         'bowl_points': points})


def confirm_bowl(conn, user, data):
    run = result(user, data.token)
    inputs, metric = run['input'], run['result']
    need('bowl_points' in inputs, '该凭证不是整碗试算任务')
    panel = get(conn, proof_regions, inputs['panel'], lock=True)
    need(panel['revision'] == inputs['revision'], '样张保护边界已修订，请重算')
    _validated_points(conn, panel, inputs['bowl_points'])
    # 整组签认：一碗记录固化共用比例，同时为每个点落一条签认簿，供试色位与回执沿用
    bowl = insert(conn, color_bowls, code=data.code,
        panel=inputs['panel'], revision=inputs['revision'],
        **{k: metric[k] for k in ('fraction', 'mean_de', 'lower_de', 'upper_de',
                                  'max_upper_de', 'test_mae')},
        token=data.token, points=metric['points'])
    for index, point in enumerate(metric['points'], start=1):
        insert(conn, shade_studies,
            code=f"{data.code}-P{index:02d}",
            panel=inputs['panel'], revision=inputs['revision'],
            x_mm=point['x_mm'], y_mm=point['y_mm'], ground_l=point['ground_l'],
            fraction=point['fraction'], mean_de=point['mean_de'],
            lower_de=point['lower_de'], upper_de=point['upper_de'],
            test_mae=metric['test_mae'], token=f"{data.token}:P{index:02d}",
            bowl=data.code)
    return bowl


def _existing_claim(conn, claim_key):
    row = conn.execute(select(bowl_claims).where(bowl_claims.c.claim_key == claim_key)
                       ).mappings().first()
    return dict(row) if row is not None else None


def _claim_slots(conn, bowl_key):
    return [dict(row) for row in conn.execute(
        select(patch_slots).where(patch_slots.c.claim == bowl_key)
        .order_by(patch_slots.c.code)).mappings()]


def reserve_bowl(conn, user, data):
    # 幂等回查必须在任何预检查之前：并发下另一会话可能已用同一请求键提交，
    # 此时直接取回原组，不再做占点检查，保证“重试取回原组、不重复占位”
    known = _existing_claim(conn, data.claim_key)
    if known is not None:
        need(known['bowl'] == data.bowl and known['reader'] == data.reader,
             '请求键已用于其他整碗领位')
        return {'claim': known, 'slots': _claim_slots(conn, data.claim_key), 'retried': True}

    # 先锁样张行：与边界修订共用同一把行锁，边界修订先提交即先成就，
    # 随后这里的版次检查会让旧签认整组退回，修订本身不占任何点
    bowl = get(conn, color_bowls, data.bowl)
    panel = get(conn, proof_regions, bowl['panel'], lock=True)
    need(panel['revision'] == bowl['revision'], '边界已改版，旧签认整组不可领位')

    from domain.proof_geometry import demand_point
    studies = [dict(row) for row in conn.execute(
        select(shade_studies).where(shade_studies.c.bowl == data.bowl)
        .order_by(shade_studies.c.code)).mappings()]
    need(len(studies) == len(bowl['points']), '整碗签认点不完整，拒绝领位')
    for study in studies:
        demand_point(panel, study['x_mm'], study['y_mm'])

    # 预检查之后再回查一次：覆盖并发会话恰在检查期间用同一请求键提交的时间窗
    known = _existing_claim(conn, data.claim_key)
    if known is not None:
        need(known['bowl'] == data.bowl and known['reader'] == data.reader,
             '请求键已用于其他整碗领位')
        return {'claim': known, 'slots': _claim_slots(conn, data.claim_key), 'retried': True}

    # 占点判断与写入放进同一子事务：任一点已被领（含单点流程或其他整碗），
    # 唯一索引令整段回滚，全组退回；同请求键并发则回查取回原组
    try:
        with conn.begin_nested():
            for study in studies:
                site_key = f"{bowl['panel']}:{study['x_mm']}:{study['y_mm']}"
                occupied = conn.execute(select(patch_slots.c.code).where(
                    patch_slots.c.site_key == site_key)).first()
                need(occupied is None,
                     f'坐标 ({study["x_mm"]},{study["y_mm"]}) 已被领取，整组退回')
            insert(conn, bowl_claims, claim_key=data.claim_key,
                   bowl=data.bowl, reader=data.reader)
            for index, study in enumerate(studies, start=1):
                insert(conn, patch_slots,
                    code=f"{data.bowl}-S{index:02d}",
                    panel=bowl['panel'], study=study['code'],
                    x_mm=study['x_mm'], y_mm=study['y_mm'],
                    site_key=f"{bowl['panel']}:{study['x_mm']}:{study['y_mm']}",
                    reader=data.reader, delta_seen=None, receipt=None,
                    state='已领取', claim=data.claim_key)
    except IntegrityError:
        winner = _existing_claim(conn, data.claim_key)
        if winner is not None and winner['bowl'] == data.bowl and winner['reader'] == data.reader:
            return {'claim': winner, 'slots': _claim_slots(conn, data.claim_key), 'retried': True}
        raise _conflict('领位冲突：整组中存在已被占用的点，整组退回')
    return {'claim': _existing_claim(conn, data.claim_key),
            'slots': _claim_slots(conn, data.claim_key), 'retried': False}


def _conflict(message):
    from fastapi import HTTPException
    return HTTPException(409, detail=message)
