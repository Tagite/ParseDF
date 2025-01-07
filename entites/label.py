from __future__ import annotations
from pydantic import BaseModel, Field
import uuid


class Pos(BaseModel):
    x: int
    y: int
    
    class Config:
        frozen = True


class BBox(BaseModel):
    top_left: Pos
    bottom_right: Pos

    class Config:
        frozen = True


class Label(BaseModel):
    id: uuid.UUID = Field(
                        default_factory=uuid.uuid4,
                        private=True)
    bbox: BBox
    label_type: str

    class Config:
        frozen = True
