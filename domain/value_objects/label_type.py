from pydantic import BaseModel

from domain.services.validator import NotBlankStr


class LabelType(BaseModel):
    name: NotBlankStr

    class Config:
        frozen = True
