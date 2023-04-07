from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    articles = relationship("Article", back_populates="owner")
