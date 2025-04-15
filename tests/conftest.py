import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.adapters.persistence.entities.template import Template
from src.infrastructure.database import Base

TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/spark_template_test"
)


@pytest.fixture(scope="session")
async def test_db():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def parserd_file_v1beta1():
    return {
        "apiVersion": "v1beta1",
        "kind": "Template",
        "metadata": {
            "name": "template-test",
            "title": "Template Test",
            "description": "Template teste",
            "tags": ["test", "template"],
        },
        "spec": {
            "type": "service",
            "parameters": [
                {
                    "title": "Form 1",
                    "required": ["field1"],
                    "properties": {
                        "field1": {
                            "title": "Field 1",
                            "type": "string",
                            "description": "Field 1 description",
                        },
                        "field2": {
                            "title": "Field 2",
                            "type": "string",
                            "description": "Field 2 description",
                        },
                    },
                },
            ],
            "steps": [
                {
                    "id": "step1",
                    "name": "Step 1",
                    "action": "fetch:template",
                    "input": {"value1": "${value1}"},
                }
            ],
        },
    }


@pytest.fixture
def parserd_file_v1beta2():
    return {
        "apiVersion": "v1beta2",
        "kind": "Template",
        "metadata": {
            "name": "template-test",
            "title": "Template Test",
            "description": "Template teste",
            "tags": ["test", "template"],
        },
        "spec": {
            "type": "service",
            "parameters": [
                {
                    "title": "Form 1",
                    "required": ["field1"],
                    "properties": {
                        "field1": {
                            "title": "Field 1",
                            "type": "string",
                            "description": "Field 1 description",
                        },
                        "field2": {
                            "title": "Field 2",
                            "type": "string",
                            "description": "Field 2 description",
                        },
                    },
                },
            ],
            "steps": [
                {
                    "id": "step1",
                    "name": "Step 1",
                    "action": "fetch:template",
                    "input": {"value1": "${value1}"},
                }
            ],
        },
    }


@pytest.fixture
async def test_template(test_db, parserd_file_v1beta2):
    template = Template(
        id="8becbbf0-a7eb-4f4d-94be-931d60f9f362",
        name="template-test",
        title="Template Test",
        description="Template teste",
        origin="test",
        config=parserd_file_v1beta2,
    )
    test_db.add(template)

    await test_db.commit()
    await test_db.refresh(template)

    yield template

    await test_db.delete(template)
    await test_db.commit()
