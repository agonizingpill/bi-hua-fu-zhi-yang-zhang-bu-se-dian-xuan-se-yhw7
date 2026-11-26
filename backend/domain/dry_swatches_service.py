from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.proof_regions_model import proof_regions
from domain.dry_swatches_model import dry_swatches
from domain.shade_studies_model import shade_studies
from domain.patch_slots_model import patch_slots


def record_swatch(conn, user, data):
    allowed = set(r['pigment_family'] for r in scan(conn, proof_regions))
    need(data.family in allowed, '该色样册未绑定复制样张')
    need(0 <= data.fraction <= 1 and 0 <= data.ground_l <= 100, '比例或底色超出量纲')
    need(0 <= data.delta_e <= 100 and 0 <= data.dry_hours <= 240, '点测值或静置小时超范围')
    need(data.sample_ref.startswith('COLOR-'), '须填写点测原始凭证')
    return insert(conn, dry_swatches, **data.model_dump(), witnessed=False)


def witness_swatch(conn, user, data):
    row = get(conn, dry_swatches, data.chip, lock=True)
    need(not row['witnessed'], '该干样已经验真')
    need(row['dry_hours'] >= 24, '静置未满 24 小时，等待干样复测')
    return update(conn, dry_swatches, data.chip, witnessed=True)
