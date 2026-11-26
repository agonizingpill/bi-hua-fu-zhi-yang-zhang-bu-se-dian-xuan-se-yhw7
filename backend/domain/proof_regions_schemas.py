from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class ReviseMask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    panel: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    frame_inset: int
    hold_x1: int
    hold_y1: int
    hold_x2: int
    hold_y2: int
