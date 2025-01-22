from domain.entites.pdf import Pdf
from domain.repository.pdf_repo_interface import PdfRepoInterface


class UpdatePdfUsecase:
    def __init__(self, pdf_repo: PdfRepoInterface):
        self.pdf_repo = pdf_repo

    def execute(self, pdf: Pdf) -> None:
        self.pdf_repo.save(pdf)
