from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repositories.user_repository import UserRepository
from src.configs.database import get_db
from src.domain.schemas.user import UserSchema

router = APIRouter()
user_repository = UserRepository()


@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[UserSchema])
async def get_users():
    return await user_repository.get_all()


@router.post("/users", response_model=UserSchema)
async def create_user(user: UserSchema):
    return await user_repository.create(user)


@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: str, user: UserSchema):
    user.id = user_id
    updated_user = await user_repository.update(user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    if not await user_repository.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
