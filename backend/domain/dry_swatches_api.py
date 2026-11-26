from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import dry_swatches_service as service
from domain.dry_swatches_model import dry_swatches
from domain.dry_swatches_schemas import RecordSwatch, WitnessSwatch

router = APIRouter()

@router.get('/dry_swatches')
def list_dry_swatches(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, dry_swatches)


@router.post('/dry_swatches/record-swatch')
def record_swatch(data: RecordSwatch, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.record_swatch(conn, user, data)
        record(conn, user, 'dry_swatches.record_swatch')
        return output


@router.post('/dry_swatches/witness-swatch')
def witness_swatch(data: WitnessSwatch, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.witness_swatch(conn, user, data)
        record(conn, user, 'dry_swatches.witness_swatch')
        return output
