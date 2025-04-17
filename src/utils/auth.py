import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.adapters.api.schemas.user_schema import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    payload = jwt.decode(token, options={"verify_signature": False})
    return UserSchema(**payload)


def get_current_token(token: str = Depends(oauth2_scheme)) -> str:
    return token
