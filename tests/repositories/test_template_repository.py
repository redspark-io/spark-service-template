import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.persistence.entities.template import Template
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

@pytest.mark.asyncio
async def test_template_repository_get_all_templates_with_success(test_db, test_template):
    template_repository = TemplateRepository(test_db)

    templates = await template_repository.get_all_templates()

    assert len(templates) > 0
    assert any(template.id == test_template.id for template in templates)


@pytest.mark.asyncio
async def test_template_repository_create_template_with_success(test_db):
    template_repository = TemplateRepository(test_db)

    new_template = Template(
        name="Test Template",
        title="Test Title",
        description="Test Description",
        origin="Test Origin",
        config={"key": "value"},
    )

    created_template = await template_repository.create_template(new_template)

    assert created_template.id is not None
    assert created_template.name == "Test Template"
    assert created_template.title == "Test Title"
    assert created_template.description == "Test Description"
    assert created_template.origin == "Test Origin"
    assert created_template.config == {"key": "value"}


@pytest.mark.asyncio
async def test_template_repository_delete_template_with_success(test_db, test_template):
    template_repository = TemplateRepository(test_db)

    await template_repository.delete_template(test_template)

    deleted_template = await template_repository.get_by_id(test_template.id)

    assert deleted_template is None
