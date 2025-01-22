from pydantic import BaseModel

from domain.services.validator import PositveFloatNumber


class Pos(BaseModel):
    x: PositveFloatNumber
    y: PositveFloatNumber

    class Config:
        frozen = True
        from_attributes = True
