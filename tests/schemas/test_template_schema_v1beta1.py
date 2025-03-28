import pytest
from pydantic import ValidationError

from src.domain.schemas.template.v1beta1.template import (
    TemplateSchema as TemplateSchemaV1Beta1,
)


@pytest.mark.asyncio
async def test_validate_template_with_success(parserd_file_v1beta1):
    TemplateSchemaV1Beta1.model_validate(parserd_file_v1beta1)


@pytest.mark.asyncio
async def test_validate_template_with_error_and_empty_file():
    with pytest.raises(ValidationError):
        TemplateSchemaV1Beta1.model_validate({})
