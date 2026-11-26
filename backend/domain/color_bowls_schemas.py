from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints


class BowlPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")
    x_mm: int
    y_mm: int
    ground_l: FiniteFloat


class FitBowl(BaseModel):
    model_config = ConfigDict(extra="forbid")
    panel: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    points: Annotated[list[BowlPoint], ...]


class ConfirmBowl(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=48)]
    token: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class ReserveBowl(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bowl: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=48)]
    claim_key: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    reader: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
