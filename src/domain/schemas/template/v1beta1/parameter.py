from typing import Dict, List, Optional

from pydantic import BaseModel

from src.domain.schemas.template.v1beta1.property import PropertyScheme


class ParameterScheme(BaseModel):
    title: str
    required: Optional[List[str]] = None
    properties: Dict[str, PropertyScheme]
