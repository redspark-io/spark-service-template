import logging

from fastapi import FastAPI

from src.adapters.api.routes.v1 import health_check, template, template_tmp

logger = logging.getLogger("uvicorn")


app = FastAPI()

app.include_router(health_check.router, tags=["health-check"])
app.include_router(template.router, tags=["template"])
app.include_router(template_tmp.router, tags=["template_tmp"])
