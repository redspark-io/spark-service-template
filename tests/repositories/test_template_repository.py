import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.persistence.repositories.template_repository import TemplateRepository


@pytest.mark.asyncio(loop_scope="session")
async def test_template_repository_get_by_id_with_success(test_db, test_template):
    template_repository = TemplateRepository(test_db)

    template = await template_repository.get_by_id(test_template.id)

    assert template is not None
    assert template.id == test_template.id
    assert template.name == test_template.name


@pytest.mark.asyncio(loop_scope="session")
async def test_template_repository_get_by_id_with_not_found(test_db: AsyncSession):
    template_repository = TemplateRepository(test_db)

    template = await template_repository.get_by_id(
        "e7608ca5-b173-493a-9a6f-79c97f33c21f"
    )
    assert template is None
