from typing import Optional

from pydantic import BaseModel


class PropertyScheme(BaseModel):
    title: str
    type: str
    description: Optional[str] = None
