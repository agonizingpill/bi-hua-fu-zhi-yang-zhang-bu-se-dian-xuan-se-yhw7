from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class FitAtPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")
    panel: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    x_mm: int
    y_mm: int
    ground_l: FiniteFloat


class ConfirmColor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    token: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
