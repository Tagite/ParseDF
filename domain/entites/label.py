from __future__ import annotations
from typing_extensions import Self

import uuid
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator


class Label(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    label_type: LabelType
    bbox: BBox

    def update_by_bbox(self, bbox: BBox) -> Label:
        return self._update_field(bbox=bbox)

    def update_by_label_type(self, label_type: LabelType) -> Label:
        return self._update_field(label_type=label_type)

    def _update_field(self, **fields) -> Label:
        return self.model_copy(update=fields)

    class Config:
        frozen = True


class LabelType(BaseModel):
    name: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LabelType):
            return ValueError("object is not LabelType type")
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @field_validator("name", mode="after")
    @classmethod
    def ensure_not_blank(cls, value: str) -> str:
        if not len(value.strip()):
            raise ValueError("name is blank")

    class Config:
        frozen = True


class BBox(BaseModel):
    top_left: Pos
    bottom_right: Pos

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BBox):
            raise ValueError("object is not BBox type")
        return (
            self.top_left == other.top_left and self.bottom_right == other.bootm_right
        )

    def __hash__(self):
        return hash(self.top_left, self.bottom_right)

    @model_validator(mode="after")
    def check_relative_pos(self) -> Self:
        if (self.top_left.x > self.bottom_right.x) or (
            self.top_left.y < self.bottom_right.y
        ):
            raise ValueError("top_left & bottom_right relative don't match")

    class Config:
        frozen = True


class Pos(BaseModel):
    x: int
    y: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pos):
            raise ValueError("object is not Pos type")
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x, self.y)

    @field_validator("x", "y", mode="after")
    @classmethod
    def ensure_positive(cls, value: int) -> int:
        if value < 0:
            raise ValueError(f"{value} is not an positive number")
        return value

    class Config:
        frozen = True