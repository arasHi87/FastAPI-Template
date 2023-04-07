from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Article(Base):
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    body = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="articles")
