import uuid

from sqlalchemy import JSON, UUID, Column, DateTime, String, func

from src.configs.database import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    title = Column(String)
    description = Column(String)
    origin = Column(String)
    config = Column(JSON)
    repo_owner = Column(String, nullable=True)
    repo_name = Column(String, nullable=True)
    repo_organization = Column(String, nullable=True)
    repo_token = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
