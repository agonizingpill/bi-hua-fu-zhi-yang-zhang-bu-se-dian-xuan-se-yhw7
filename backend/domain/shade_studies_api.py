from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import shade_studies_service as service
from domain.shade_studies_model import shade_studies
from domain.shade_studies_schemas import FitAtPoint, ConfirmColor

router = APIRouter()

@router.get('/shade_studies')
def list_shade_studies(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, shade_studies)


@router.post('/shade_studies/fit-at-point')
def fit_at_point(data: FitAtPoint, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.fit_at_point(conn, user, data)
        record(conn, user, 'shade_studies.fit_at_point')
        return output


@router.post('/shade_studies/confirm-color')
def confirm_color(data: ConfirmColor, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.confirm_color(conn, user, data)
        record(conn, user, 'shade_studies.confirm_color')
        return output
