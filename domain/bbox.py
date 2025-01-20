from typing_extensions import Self
from pydantic import BaseModel
from pydantic import model_validator

from domain.pos import Pos


class BBox(BaseModel):
    top_left: Pos
    bottom_right: Pos

    @model_validator(mode="after")
    def check_relative_pos(self) -> Self:
        if (self.top_left.x > self.bottom_right.x) or (
            self.top_left.y < self.bottom_right.y
        ):
            raise ValueError("top_left & bottom_right relative don't match")

    class Config:
        frozen = True
