from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    active: bool = True
