from typing import Optional

from pydantic import BaseModel


class ApplicationSchema(BaseModel):
    id: Optional[str] = None
    organization_id: Optional[str] = None
    template_id: Optional[str] = None
    owner_user_id: Optional[str] = None
    status: str
    name: str
    description: str
    repo_url: str
