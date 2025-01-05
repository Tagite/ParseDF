from __future__ import annotations
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


@dataclass(frozen=True)
class BBox:
    top_left: Pos
    bottom_right: Pos


@dataclass(frozen=True)
class Label:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    bbox: BBox
    label_type: str

    def with_bbox(self, bbox: BBox) -> Label:
        return Label(bbox=bbox, label_type=self.label_type)

    def with_label_type(self, label_type: str) -> Label:
        return Label(bbox=self.bbox, label_type=label_type)

    def __repr__(self):
        return f"Label(id={self.id}, bbox={self.bbox}, label_type={self.label_type})"
