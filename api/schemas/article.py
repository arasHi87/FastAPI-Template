from pydantic import BaseModel


# Shared properties
class ArticleBase(BaseModel):
    title: str
    description: str
    body: str


"""
CRUD schemas for Article
"""


# Properties to receive on article creation
class ArticleCreate(ArticleBase):
    pass


# Properties to receive on article update
class ArticleUpdate(ArticleBase):
    pass


"""
Database schemas for Article
"""


# Shared properties
class ArticleDB(ArticleBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Article(ArticleDB):
    pass
