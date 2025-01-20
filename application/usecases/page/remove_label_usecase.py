from domain.repository.pdf_repo_interface import PDFRepositoryInterface


class RemoveLabelUseCase:
    def __init__(self, pdf_repo: PDFRepositoryInterface):
        self.pdf_repo = pdf_repo

    def execute(self, pdf_id: str, page_index: int, label_id: str) -> None:
        pdf = self.pdf_repo.find_by_id(pdf_id)
        page = pdf.get_page_by_index(page_index)
        label = page.get_label(label_id)
        page.remove_label(label)
        self.pdf_repo.save(pdf)
