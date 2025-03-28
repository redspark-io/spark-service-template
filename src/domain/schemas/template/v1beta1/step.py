from typing import Any, Dict, List

from pydantic import BaseModel

from src.domain.schemas.template.v1beta1.enums.action import ActionEnum


class StepSchema(BaseModel):
    id: str
    name: str
    action: ActionEnum
    input: Dict[str, Any]
