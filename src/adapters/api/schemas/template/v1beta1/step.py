from typing import Any, Dict, List

from pydantic import BaseModel

from src.adapters.api.schemas.template.v1beta1.enums.action import ActionEnum


class StepSchema(BaseModel):
    id: str
    name: str
    action: ActionEnum
    input: Dict[str, Any]
