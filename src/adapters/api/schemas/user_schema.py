from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    preferred_username: Optional[str] = None
