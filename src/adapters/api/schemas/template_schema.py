from datetime import datetime
from typing import Optional
from uuid import UUID

from click import File
from fastapi import UploadFile

from pydantic import BaseModel, ConfigDict


class TemplateSchema(BaseModel):
    name: str
    title: str
    description: str
    origin: str
    repo_owner: Optional[str] = None
    repo_name: Optional[str] = None
    repo_organization: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TemplateResponseSchema(TemplateSchema):
    id: UUID
    config: dict
