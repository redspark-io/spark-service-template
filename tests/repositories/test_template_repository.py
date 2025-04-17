from unittest.mock import AsyncMock
from uuid import uuid4
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
async def test_template_repository_get_all_templates_with_success():
    mock_repository = AsyncMock(spec=TemplateRepository)
    mock_template = Template(
        id=uuid4(),
        name="Test Template",
        title="Test Title",
        description="Test Description",
        origin="Test Origin",
        config={"key": "value"},
    )
    mock_repository.get_all_templates.return_value = [mock_template]

    templates = await mock_repository.get_all_templates()

    assert len(templates) > 0
    assert any(template.id == mock_template.id for template in templates)
    mock_repository.get_all_templates.assert_called_once()


@pytest.mark.asyncio
async def test_template_repository_create_template_with_success():
    mock_repository = AsyncMock(spec=TemplateRepository)
    mock_template = Template(
        id=uuid4(),
        name="Test Template",
        title="Test Title",
        description="Test Description",
        origin="Test Origin",
        config={"key": "value"},
    )
    mock_repository.create_template.return_value = mock_template

    created_template = await mock_repository.create_template(mock_template)

    assert created_template.id is not None
    assert created_template.name == "Test Template"
    assert created_template.title == "Test Title"
    assert created_template.description == "Test Description"
    assert created_template.origin == "Test Origin"
    assert created_template.config == {"key": "value"}
    mock_repository.create_template.assert_called_once_with(mock_template)


@pytest.mark.asyncio
async def test_template_repository_delete_template_with_success():
    mock_repository = AsyncMock(spec=TemplateRepository)
    mock_template = Template(
        id=uuid4(),
        name="Test Template",
        title="Test Title",
        description="Test Description",
        origin="Test Origin",
        config={"key": "value"},
    )
    mock_repository.get_by_id.return_value = None

    await mock_repository.delete_template(mock_template)
    deleted_template = await mock_repository.get_by_id(mock_template.id)

    assert deleted_template is None
    mock_repository.delete_template.assert_called_once_with(mock_template)
    mock_repository.get_by_id.assert_called_once_with(mock_template.id)