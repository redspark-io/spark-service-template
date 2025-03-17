import uuid

from sqlalchemy import UUID, Boolean, Column, String

from src.configs.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    active = Column(Boolean, default=True)
