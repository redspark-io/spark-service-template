from dataclasses import dataclass
from typing import Optional


@dataclass
class Template:
    id: str
    name: str
    title: str
    description: str
    origin: str
    config: dict
    repo_owner: Optional[str] = None
    repo_name: Optional[str] = None
    repo_organization: Optional[str] = None
    repo_token: Optional[str] = None
