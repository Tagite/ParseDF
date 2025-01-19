from __future__ import annotations

import uuid
from pydantic import BaseModel
from pydantic import Field

from domain.label_type import LabelType
from domain.bbox import BBox


class Label(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    label_type: LabelType
    bbox: BBox

    class Config:
        frozen = True









