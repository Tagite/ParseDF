from domain.entites.label import Label
from domain.repository.pdf_repo_interface import PDFRepositoryInterface


class CreateLabelUseCase:
    def __init__(self, pdf_repo: PDFRepositoryInterface):
        self.pdf_repo = pdf_repo

    def execute(self, pdf_id: str, page_index: int, label: Label) -> None:
        pdf = self.pdf_repo.find_by_id(pdf_id)
        page = pdf.get_page_by_index(page_index)
        page.add_label(label)
        self.pdf_repo.save(pdf)
