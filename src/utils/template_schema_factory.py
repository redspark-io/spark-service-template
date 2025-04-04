from src.domain.enums.kind import KindEnum
from src.domain.schemas.template.v1beta1.template import (
    TemplateSchema as TemplateSchemaV1Beta1,
)
from src.domain.schemas.template.v1beta2.template import (
    TemplateSchema as TemplateSchemaV1Beta2,
)


def create_template_schema(data: dict):
    version = data.get("apiVersion", None)
    kind = data.get("kind", None)

    template_schema = None
    if kind == KindEnum.template:
        if version == "v1beta1":
            template_schema = TemplateSchemaV1Beta1(**data)
        elif version == "v1beta2":
            template_schema = TemplateSchemaV1Beta2(**data)
        else:
            raise ValueError(f"Unsuported version {version}")
    else:
        raise ValueError(f"Unsuported kind {kind}")

    return template_schema
