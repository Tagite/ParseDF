from pydantic import BaseModel, Field

from entites.page import Page
from entites.label import Label


class PDF(BaseModel):
    now_index: int = 0
    pages: list[Page] = Field(default_factory=list)

    def change_page(self, index: int) -> None:
        self.now_index = index

    def inject_label(self, index: int, label: Label) -> None:
        self.pages[index].add_label(label)

    def __len__(self):
        return len(self.pages)
    
    class Config:
        frozen = True
