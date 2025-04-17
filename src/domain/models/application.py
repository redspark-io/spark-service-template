from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Application:
    status: str
    name: str
    description: str
    repo_url: str
    id: Optional[str] = None
    organization_id: Optional[str] = None
    template_id: Optional[str] = None
    owner_user_id: Optional[str] = None

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
