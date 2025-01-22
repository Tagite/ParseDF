from domain.entites.pdf import Pdf
from domain.repository.pdf_repo_interface import PdfRepoInterface


class CreatePdfUsecase:
    def __init__(self, pdf_repo: PdfRepoInterface):
        self.pdf_repo = pdf_repo

    def execute(self, pdf_name: str) -> Pdf:
        try:
            pdf = self.pdf_repo.find_by_name(pdf_name)[0]
        except:
            pdf = Pdf(file_name=pdf_name)
        finally: 
            self.pdf_repo.save(pdf)
            return pdf
