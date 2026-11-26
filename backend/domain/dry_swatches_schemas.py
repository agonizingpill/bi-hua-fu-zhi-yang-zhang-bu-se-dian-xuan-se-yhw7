from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class RecordSwatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    family: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    fraction: FiniteFloat
    ground_l: FiniteFloat
    delta_e: FiniteFloat
    sample_ref: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    dry_hours: int


class WitnessSwatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chip: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
