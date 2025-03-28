import pytest

from src.utils.schemas import handler


@pytest.mark.asyncio
async def test_validate_template_with_success(
    parserd_file_v1beta1, parserd_file_v1beta2
):
    template_schema_v1beta1 = handler(parserd_file_v1beta1)
    assert (
        "src.domain.schemas.template.v1beta1.template"
        == template_schema_v1beta1.__module__
    )

    template_schema_v1beta2 = handler(parserd_file_v1beta2)
    assert (
        "src.domain.schemas.template.v1beta2.template"
        == template_schema_v1beta2.__module__
    )


@pytest.mark.asyncio
async def test_validate_template_with_not_supported_error():
    with pytest.raises(Exception):
        handler(
            {
                "apiVersion": "v1betaN",
                "kind": "Template",
            }
        )

    with pytest.raises(Exception):
        handler(
            {
                "apiVersion": "v1beta1",
                "kind": "Unsuported",
            }
        )
