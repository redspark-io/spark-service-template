from pydantic import BaseModel

from src.adapters.api.schemas.template.v1beta1.metadata import MetadataScheme
from src.adapters.api.schemas.template.v1beta1.spec import SpecSchema
from src.domain.enums.kind import KindEnum


class TemplateSchema(BaseModel):
    apiVersion: str
    kind: KindEnum

    metadata: MetadataScheme

    spec: SpecSchema
