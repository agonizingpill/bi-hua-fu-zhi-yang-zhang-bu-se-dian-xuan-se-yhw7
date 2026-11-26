from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import proof_regions_service as service
from domain.proof_regions_model import proof_regions
from domain.proof_regions_schemas import ReviseMask

router = APIRouter()

@router.get('/proof_regions')
def list_proof_regions(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, proof_regions)


@router.post('/proof_regions/revise-mask')
def revise_mask(data: ReviseMask, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.revise_mask(conn, user, data)
        record(conn, user, 'proof_regions.revise_mask')
        return output
