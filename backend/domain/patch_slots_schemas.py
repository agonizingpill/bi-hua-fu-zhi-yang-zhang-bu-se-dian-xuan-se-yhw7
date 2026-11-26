from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ReservePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    study: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    x_mm: int
    y_mm: int
    reader: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class ConsumePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    slot: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    receipt: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    observed_de: FiniteFloat
