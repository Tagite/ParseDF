from domain.entites.label import Label
from domain.repository.pdf_repo_interface import PDFRepositoryInterface


class UpdateLabelUseCase:
    def __init__(self, pdf_repo: PDFRepositoryInterface):
        self.pdf_repo = pdf_repo

    def execute(
        self, pdf_id: str, page_index: int, old_label_id: str, new_label: Label
    ) -> None:
        pdf = self.pdf_repo.find_by_id(pdf_id)
        page = pdf.get_page_by_index(page_index)
        old_label = page.get_label(old_label_id)
        page.update_label(old_label, new_label)
        self.pdf_repo.save(pdf)
