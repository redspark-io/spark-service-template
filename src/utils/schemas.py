from src.domain.enums.kind import KindEnum
from src.domain.schemas.template.v1beta1.template import (
    TemplateSchema as TemplateSchemaV1Beta1,
)
from src.domain.schemas.template.v1beta2.template import (
    TemplateSchema as TemplateSchemaV1Beta2,
)


def handler(data: dict):
    version = data.get("apiVersion", None)
    kind = data.get("kind", None)

    template = None
    if kind == KindEnum.template:
        if version == "v1beta1":
            template = TemplateSchemaV1Beta1(**data)
        elif version == "v1beta2":
            template = TemplateSchemaV1Beta2(**data)
        else:
            raise Exception("Unsuported version")
    else:
        raise Exception("Unsuported kind")

    return template
