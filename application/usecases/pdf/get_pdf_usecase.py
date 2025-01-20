from domain.entites.pdf import Pdf
from domain.entites.page import Page
from domain.entites.label import Label
from domain.repository.pdf_repo_interface import PDFRepositoryInterface


class GetPdfUsecase:
    def __init__(self, pdf_repo: PDFRepositoryInterface):
        self.pdf_repo = pdf_repo

    def execute(self, pdf_id: str) -> Pdf:
        pdf = self.pdf_repo.find_by_id(pdf_id)
        return pdf