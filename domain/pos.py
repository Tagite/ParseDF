from pydantic import BaseModel

from domain.validator import PositveNumber


class Pos(BaseModel):
    x: PositveNumber
    y: PositveNumber

    class Config:
        frozen = True
