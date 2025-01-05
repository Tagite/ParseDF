from dataclasses import dataclass, field

from entites.page import Page
from entites.label import Label


@dataclass
class PDF:
    now_index: int
    pages: list[Page] = field(default_factory=list)

    def change_page(self, index: int) -> None:
        self.now_index = index

    def inject_label(self, index: int, label: Label) -> None:
        self.pages[index].add_label(label)
