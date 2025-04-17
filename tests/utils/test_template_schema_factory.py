import pytest

from src.utils.template_schema_factory import create_template_schema


@pytest.mark.asyncio
async def test_validate_template_with_success(
    parserd_file_v1beta1, parserd_file_v1beta2
):
    template_schema_v1beta1 = create_template_schema(parserd_file_v1beta1)
    assert (
        "src.adapters.api.schemas.template.v1beta1.template"
        == template_schema_v1beta1.__module__
    )

    template_schema_v1beta2 = create_template_schema(parserd_file_v1beta2)
    assert (
        "src.adapters.api.schemas.template.v1beta2.template"
        == template_schema_v1beta2.__module__
    )


@pytest.mark.asyncio
async def test_validate_template_with_not_supported_error():
    with pytest.raises(ValueError):
        create_template_schema({"apiVersion": "v1betaN", "kind": "Template"})
    with pytest.raises(ValueError):
        create_template_schema({"apiVersion": "v1beta2", "kind": "Unsuported"})
