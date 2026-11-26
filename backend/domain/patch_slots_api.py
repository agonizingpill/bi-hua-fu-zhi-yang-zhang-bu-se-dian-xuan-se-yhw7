from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import patch_slots_service as service
from domain.patch_slots_model import patch_slots
from domain.patch_slots_schemas import ReservePatch, ConsumePatch

router = APIRouter()

@router.get('/patch_slots')
def list_patch_slots(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, patch_slots)


@router.post('/patch_slots/reserve-patch')
def reserve_patch(data: ReservePatch, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.reserve_patch(conn, user, data)
        record(conn, user, 'patch_slots.reserve_patch')
        return output


@router.post('/patch_slots/consume-patch')
def consume_patch(data: ConsumePatch, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.consume_patch(conn, user, data)
        record(conn, user, 'patch_slots.consume_patch')
        return output
