import uuid
from pydantic import BaseModel
from pydantic import Field

from domain.page import Page


class Pdf(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    file_name: str
    labels: list[Page] = Field(default_factory=list)

    def get_page_by_index(self, index: int) -> Page:
        if len(self.labels) >= index:
            raise ValueError(f"{index} is invalid index")
        return self.labels[index]

    def append_page(self, page: Page) -> None:
        self.labels.append(page)

    def insert_page(self, page: Page, index: int) -> None:
        self.labels.insert(index, page)

    def remove_page(self, page: Page) -> None:
        self.labels.remove(page)

    def update_page(self, old_page: Page, new_page: Page) -> None:
        old_index = old_page.index
        self.remove_page(old_page)
        self.insert_page(new_page, old_index)
