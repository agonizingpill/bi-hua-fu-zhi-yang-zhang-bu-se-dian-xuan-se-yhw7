from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.proof_regions_model import proof_regions
from domain.dry_swatches_model import dry_swatches
from domain.shade_studies_model import shade_studies
from domain.patch_slots_model import patch_slots


def reserve_patch(conn, user, data):
    from domain.proof_geometry import demand_point
    study = get(conn, shade_studies, data.study)
    panel = get(conn, proof_regions, study['panel'], lock=True)
    demand_point(panel, data.x_mm, data.y_mm)
    need(panel['revision'] == study['revision'], '边界已改版，旧签认不可领位')
    need((data.x_mm, data.y_mm) == (study['x_mm'], study['y_mm']), '预约坐标与签认点不一致')
    return insert(conn, patch_slots, **data.model_dump(), panel=study['panel'],
        site_key=f"{study['panel']}:{data.x_mm}:{data.y_mm}", state='已领取',
        delta_seen=None, receipt=None)


def consume_patch(conn, user, data):
    from domain.proof_geometry import demand_point
    slot = get(conn, patch_slots, data.slot)
    panel = get(conn, proof_regions, slot['panel'], lock=True)
    slot = get(conn, patch_slots, data.slot, lock=True)
    study = get(conn, shade_studies, slot['study'])
    need(slot['state'] in {'已领取','待复样'}, '试色位已消费')
    demand_point(panel, slot['x_mm'], slot['y_mm'])
    need(study['revision'] == panel['revision'], '保护边界已改版，当前试色位需复核')
    need(data.receipt.startswith('PROOF-') and 0 <= data.observed_de <= 100, '缺少合规的试色回执与色差')
    state = '已消费' if data.observed_de <= study['upper_de'] + .5 else '待复样'
    return update(conn, patch_slots, data.slot, delta_seen=data.observed_de, receipt=data.receipt, state=state)
