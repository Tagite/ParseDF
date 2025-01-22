from domain.entites.pdf import Pdf
from domain.repository.pdf_repo_interface import PdfRepoInterface


class GetPdfUsecase:
    def __init__(self, pdf_repo: PdfRepoInterface):
        self.pdf_repo = pdf_repo

    def execute(self, pdf_id: str) -> Pdf:
        pdf = self.pdf_repo.find_by_id(pdf_id)
        return pdf
