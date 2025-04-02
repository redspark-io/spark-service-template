from pydantic import BaseModel
from src.domain.enums.kind import KindEnum

from src.domain.schemas.template.v1beta1.metadata import MetadataScheme
from src.domain.schemas.template.v1beta1.spec import SpecSchema


class TemplateSchema(BaseModel):
    apiVersion: str
    kind: KindEnum

    metadata: MetadataScheme

    spec: SpecSchema
