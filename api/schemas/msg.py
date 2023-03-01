from pydantic import BaseModel


class Msg(BaseModel):
    detail: str
