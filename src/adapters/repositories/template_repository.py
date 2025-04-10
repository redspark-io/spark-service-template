from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.database import get_db
from src.domain.entities.template import Template
from src.domain.ports.template_port import TemplatePort


class TemplateRepository(TemplatePort):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, template_id: str) -> Optional[Template]:
        query = await self.db.execute(
            select(Template).where(Template.id == template_id)
        )
        return query.scalars().first()


def get_template_repository(db: AsyncSession = Depends(get_db)) -> TemplateRepository:
    return TemplateRepository(db)
