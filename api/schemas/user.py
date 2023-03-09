from pydantic import BaseModel


# Shared properties
class UserBase(BaseModel):
    name: str
    email: str
    password: str


"""
CRUD schemas for User
"""


# Properties to receive on user creation
class UserCreate(UserBase):
    pass


"""
Database schemas for User
"""


# Shared properties
class UserDB(UserBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserDB):
    pass


class UserWithoutPassword(UserDB):
    class Config:
        fields = {"password": {"exclude": True}}
