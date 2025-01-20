from pydantic import BaseModel

from domain.entites.label import Label


class LabelDto(BaseModel):
    label_type: str
    top_left_x: int
    top_left_y: int
    bottom_right_x: int
    bottom_right_y: int

    @staticmethod
    def to_dto(label: Label) -> "LabelDto":
        return LabelDto(
            label_type=label.label_type.name,
            top_left_x=label.bbox.top_left.x,
            top_left_y=label.bbox.top_left.y,
            bottom_right_x=label.bbox.bottom_right.x,
            bottom_right_y=label.bbox.bottom_right.y,
        )