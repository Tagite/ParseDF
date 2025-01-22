from domain.entites.page import Page
from domain.repository.pdf_repo_interface import PdfRepoInterface


class CreatePageUseCase:
    def __init__(self, pdf_repo: PdfRepoInterface):
        self.pdf_repo = pdf_repo

    def execute(self, pdf_id: str, page_index: int) -> None:
        pdf = self.pdf_repo.find_by_id(pdf_id)

        try:
            page = pdf.get_page_by_index(page_index)
        except:
            page = Page(index=page_index)
            pdf.append_page(page)
            self.pdf_repo.save(pdf)
