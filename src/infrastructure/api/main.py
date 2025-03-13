from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.user_service import UserService
from src.domain.entities.user import User
from src.infrastructure.adapters.memory_user_repository import InMemoryUserRepository
from src.infrastructure.config.database import get_db

app = FastAPI(title="FastAPI Hexagonal Template")
user_repository = InMemoryUserRepository()
user_service = UserService(user_repository)


@app.get("/users/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users")
async def get_users():
    return await user_service.get_all_users()


@app.post("/users")
async def create_user(user: User):
    return await user_service.create_user(user)


@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User):
    user.id = user_id
    updated_user = await user_service.update_user(user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    if not await user_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
