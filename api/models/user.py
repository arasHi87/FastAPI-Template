from sqlalchemy import Column, String

from .base import Base


class User(Base):
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
