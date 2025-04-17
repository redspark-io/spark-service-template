from typing import List, Optional

from pydantic import BaseModel


class MetadataScheme(BaseModel):
    name: str
    title: str
    description: str
    tags: Optional[List[str]] = None
