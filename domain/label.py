from __future__ import annotations
from typing_extensions import Self

import uuid
from pydantic import BaseModel

from pydantic import Field
from pydantic import model_validator

from domain.entites.validator import PositveNumber
from domain.entites.validator import NotBlankStr
from domain.entites.validator import validate_equal_type


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

    def __eq__(self, other: object) -> bool:
        validate_equal_type(self, other)

    class Config:
        frozen = True


class LabelType(BaseModel):
    name: NotBlankStr

    def __eq__(self, other: object) -> bool:
        validate_equal_type(self, other)
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    class Config:
        frozen = True


class BBox(BaseModel):
    top_left: Pos
    bottom_right: Pos

    def __eq__(self, other: object) -> bool:
        validate_equal_type(self, other)
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
    x: PositveNumber
    y: PositveNumber

    def __eq__(self, other: object) -> bool:
        validate_equal_type(self, other)
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x, self.y)

    class Config:
        frozen = True
