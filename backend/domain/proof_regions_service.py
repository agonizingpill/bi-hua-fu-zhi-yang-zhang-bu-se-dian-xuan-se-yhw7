from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.proof_regions_model import proof_regions
from domain.dry_swatches_model import dry_swatches
from domain.shade_studies_model import shade_studies
from domain.patch_slots_model import patch_slots


def revise_mask(conn, user, data):
    from domain.proof_geometry import validate_mask
    panel = get(conn, proof_regions, data.panel, lock=True)
    mask = data.model_dump(exclude={'panel'})
    validate_mask(panel | mask)
    return update(conn, proof_regions, data.panel, **mask, revision=panel['revision']+1)
