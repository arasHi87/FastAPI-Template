from pydantic import BaseModel


class AuthToken(BaseModel):
    access_token: str
    token_type: str

    def __str__(self):
        return f"{self.token_type} {self.access_token}"


class AuthTokenData(BaseModel):
    id: int
    name: str
    email: str
    exp: int
