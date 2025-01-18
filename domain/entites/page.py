from pydantic import BaseModel

from domain.entites.label import Label


class Page(BaseModel):
    index: int
    lables: list[Label]