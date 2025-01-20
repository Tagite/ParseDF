from abc import ABC, abstractmethod

import uuid

from domain.pdf import Pdf


class PdfRepoInterface(ABC):
    @abstractmethod
    def find_by_id(self, id: uuid.UUID) -> Pdf:
        pass

    @abstractmethod
    def find_by_name(self, pdf_name: str) -> list[Pdf]:
        pass

    @abstractmethod
    def save(self, pdf: Pdf) -> None:
        pass

    @abstractmethod
    def remove_by_id(self, id: uuid.UUID) -> None:
        pass
