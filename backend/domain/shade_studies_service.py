from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.proof_regions_model import proof_regions
from domain.dry_swatches_model import dry_swatches
from domain.shade_studies_model import shade_studies
from domain.patch_slots_model import patch_slots


def fit_at_point(conn, user, data):
    from domain.proof_geometry import demand_point
    panel = get(conn, proof_regions, data.panel)
    demand_point(panel, data.x_mm, data.y_mm)
    rows = [row for row in scan(conn, dry_swatches)
        if row['witnessed'] and row['family'] == panel['pigment_family']]
    need(len(rows) >= 12, '同色样册已验真干样不足 12 条')
    low, high = min(r['ground_l'] for r in rows), max(r['ground_l'] for r in rows)
    need(low <= data.ground_l <= high, '该点底色亮度落在已测干样范围之外')
    return submit(user, {'studies':rows,'panel':data.panel,'revision':panel['revision'],
        'x_mm':data.x_mm,'y_mm':data.y_mm,'ground_l':data.ground_l})


def confirm_color(conn, user, data):
    from domain.proof_geometry import demand_point
    run = result(user,data.token)
    inputs, metric = run['input'], run['result']
    panel = get(conn,proof_regions,inputs['panel'],lock=True)
    need(panel['revision'] == inputs['revision'],'样张保护边界已修订，请重算')
    demand_point(panel, inputs['x_mm'], inputs['y_mm'])
    need(metric['upper_de'] - metric['lower_de'] <= 3.0, '预测区间过宽，先补采干样')
    return insert(conn, shade_studies, code=data.code, token=data.token,
        **{k:inputs[k] for k in ('panel','revision','x_mm','y_mm','ground_l')},
        **{k:metric[k] for k in ('fraction','mean_de','lower_de','upper_de','test_mae')})
