from domain.entites.pdf import Pdf
from domain.entites.page import Page
from domain.entites.label import Label
from domain.repository.pdf_repo_interface import PDFRepositoryInterface


class GetLabelUseCase:
    def __init__(self, pdf_repo: PDFRepositoryInterface):
        self.pdf_repo = pdf_repo

    def get_label(self, page_index: int, label_id: int) -> Label:
        pdf: Pdf = self.pdf_repo.find_by_id(label_id)
        page: Page = pdf.get_page_by_index(page_index)
        return page.get_label(label_id)
