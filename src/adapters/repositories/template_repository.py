from typing import Optional

from sqlalchemy import select
from src.domain.entities.template import Template
from src.domain.ports.template_repository_port import TemplateRepositoryPort



class TemplateRepository(TemplateRepositoryPort):

    async def get_by_id(self, template_id: str) -> Optional[Template]:
        query = await self.db.execute(
            select(Template).where(Template.id == template_id)
        )
        return query.scalars().first()
