from src.adapters.api.schemas.template.v1beta1.template import (
    TemplateSchema as TemplateSchemaV1Beta1,
)
from src.adapters.api.schemas.template.v1beta1.template import (
    TemplateSchema as TemplateSchemaV1Beta2,
)
from src.domain.enums.kind import KindEnum
from src.domain.ports.factory_schema_port import FactorySchemaPort


class TemplateSchemaFactory(FactorySchemaPort):
    async def create(self, config: dict) -> dict:
        version = config.get("apiVersion", None)
        kind = config.get("kind", None)

        template_schema = None
        if kind == KindEnum.template:
            if version == "v1beta1":
                template_schema = TemplateSchemaV1Beta1(**config)
            elif version == "v1beta2":
                template_schema = TemplateSchemaV1Beta2(**config)
            else:
                raise ValueError(f"Unsuported version {version}")
        else:
            raise ValueError(f"Unsuported kind {kind}")

        return template_schema.model_dump()


def get_template_factory():
    return TemplateSchemaFactory()
