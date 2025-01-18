from __future__ import annotations
from typing_extensions import Self

import uuid
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from pydantic import ValidationError


class Pos(BaseModel):
    x: int
    y: int

    @field_validator("x", "y", mode="after")
    @classmethod
    def ensure_positive(cls, value: int) -> int:
        if value < 0:
            raise ValidationError(f"{value} is not an positive number")
        return value

    class Config:
        frozen = True
    

class BBox(BaseModel):
    top_left: Pos
    bottom_right: Pos

    @model_validator(mode="after")
    def check_relative_pos(self) -> Self:
        if self.top_left.x > self.bottom_right.x \
                or self.top_left.y < self.bottom_right.y:
            raise ValueError("top_left & bottom_right relative don't match")

    class Config:
        frozen = True


class LabelType(BaseModel):
    name: str

    @field_validator("name", mode="after")
    @classmethod
    def ensure_not_blank(cls, value: str) -> str:
        if not len(value.strip()):
            raise ValidationError('name is blank')
            

    class Config:
        frozen = True


class Label(BaseModel):
    id: uuid.UUID = Field(
                        default_factory=uuid.uuid4,
                        )
    bbox: BBox
    label_type: LabelType

    class Config:
        frozen = True