from typing import List

from pydantic import BaseModel

from src.adapters.api.schemas.template.v1beta1.enums.type import TypeEnum
from src.adapters.api.schemas.template.v1beta1.parameter import ParameterScheme
from src.adapters.api.schemas.template.v1beta1.step import StepSchema


class SpecSchema(BaseModel):
    type: TypeEnum
    parameters: List[ParameterScheme]
    steps: List[StepSchema]
