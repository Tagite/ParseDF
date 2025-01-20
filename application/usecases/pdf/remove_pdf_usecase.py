from domain.entites.pdf import Pdf
from domain.entites.page import Page
from domain.entites.label import Label
from domain.repository.pdf_repo_interface import PDFRepositoryInterface


class RemovePdfUsecase:
    def __init__(self, pdf_repo: PDFRepositoryInterface):
        self.pdf_repo = pdf_repo

    def execute(self, pdf: Pdf) -> None:
        self.pdf_repo.remove(pdf)