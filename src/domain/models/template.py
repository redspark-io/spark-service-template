from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Template:
    name: str
    title: str
    description: str
    origin: str
    config: Optional[dict] = None
    id: Optional[UUID] = None
    repo_owner: Optional[str] = None
    repo_name: Optional[str] = None
    repo_organization: Optional[str] = None
    repo_token: Optional[str] = None
