from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.records import scan
from domain import color_bowls_service as service
from domain.color_bowls_model import color_bowls, bowl_claims
from domain.color_bowls_schemas import FitBowl, ConfirmBowl, ReserveBowl
from core.db import transaction

router = APIRouter()


@router.get('/color_bowls')
def list_color_bowls(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, color_bowls)


@router.get('/bowl_claims')
def list_bowl_claims(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, bowl_claims)


@router.post('/color_bowls/fit-bowl')
def fit_bowl(data: FitBowl, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.fit_bowl(conn, user, data)
        record(conn, user, 'color_bowls.fit_bowl')
        return output


@router.post('/color_bowls/confirm-bowl')
def confirm_bowl(data: ConfirmBowl, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.confirm_bowl(conn, user, data)
        record(conn, user, 'color_bowls.confirm_bowl')
        return output


@router.post('/color_bowls/reserve-bowl')
def reserve_bowl(data: ReserveBowl, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.reserve_bowl(conn, user, data)
        record(conn, user, 'color_bowls.reserve_bowl')
        return output
