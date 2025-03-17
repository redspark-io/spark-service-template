import logging

from fastapi import FastAPI

from src.adapters.entrypoints.rest.v1 import health_check, user

logger = logging.getLogger("uvicorn")


app = FastAPI()

app.include_router(health_check.router, tags=["health-check"])
app.include_router(user.router, tags=["user"])
