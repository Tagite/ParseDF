from __future__ import annotations

import uuid
from pydantic import BaseModel
from pydantic import Field

from domain.value_objects.label_type import LabelType
from domain.value_objects.bbox import BBox


class Label(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    label_type: LabelType
    bbox: BBox

    class Config:
        frozen = True

    def update_bbox(self, bbox: BBox) -> Label:
        return self._update_field(bbox=bbox)

    def update_label_type(self, label_type: LabelType) -> Label:
        return self._update_field(label_type=label_type)

    def _update_field(self, **fields) -> Label:
        return self.model_copy(update=fields)
