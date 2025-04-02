import pytest
from pydantic import ValidationError

from src.domain.schemas.template.v1beta2.template import (
    TemplateSchema as TemplateSchemaV1Beta2,
)


@pytest.mark.asyncio
async def test_validate_template_with_success(parserd_file_v1beta2):
    TemplateSchemaV1Beta2.model_validate(parserd_file_v1beta2)


@pytest.mark.asyncio
async def test_validate_template_with_error_and_empty_file():
    with pytest.raises(ValidationError):
        TemplateSchemaV1Beta2.model_validate({})
