from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TemplateSchema(BaseModel):
    id: UUID
    name: str
    title: str
    description: str
    origin: str
    repo_owner: Optional[str] = None
    repo_name: Optional[str] = None
    repo_organization: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
