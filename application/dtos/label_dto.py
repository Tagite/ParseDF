from pydantic import BaseModel

from domain.entites.label import Label
from domain.value_objects.bbox import BBox
from domain.value_objects.pos import Pos
from domain.value_objects.label_type import LabelType


class LabelDto(BaseModel):
    label_type: str
    top_left_x: int
    top_left_y: int
    bottom_right_x: int
    bottom_right_y: int

    @staticmethod
    def to_label(dto: "LabelDto") -> Label:
        return Label(
            label_type=LabelType(name=dto.label_type),
            bbox=BBox(
                top_left=Pos(x=dto.top_left_x, y=dto.top_left_y),
                bottom_right=Pos(x=dto.bottom_right_x, y=dto.bottom_right_y),
            ),
        )
