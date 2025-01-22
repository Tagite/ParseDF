from domain.entites.pdf import Pdf
from application.usecases.pdf import get_pdf_usecase
from application.usecases.pdf import update_pdf_usecase
from application.usecases.pdf import remove_pdf_usecase
from application.usecases.pdf import create_page_usecase
from application.usecases.pdf import create_pdf_usecase


class PdfController:
    def __init__(
        self,
        get_pdf_usecase: get_pdf_usecase.GetPdfUsecase,
        update_pdf_usecase: update_pdf_usecase.UpdatePdfUsecase,
        remove_pdf_usecase: remove_pdf_usecase.RemovePdfUsecase,
        create_page_usecase: create_page_usecase.CreatePageUseCase,
        create_pdf_usecase: create_pdf_usecase.CreatePdfUsecase,
    ):
        self.get_pdf_usecase = get_pdf_usecase
        self.update_pdf_usecase = update_pdf_usecase
        self.remove_pdf_usecase = remove_pdf_usecase
        self.create_page_usecase = create_page_usecase
        self.create_pdf_usecase = create_pdf_usecase

    def get_pdf(self, pdf_id: str) -> Pdf:
        return self.get_pdf_usecase.execute(pdf_id)

    def update_pdf(self, pdf: Pdf) -> None:
        self.update_pdf_usecase.execute(pdf)

    def remove_pdf(self, pdf: Pdf) -> None:
        self.remove_pdf_usecase.execute(pdf)

    def create_page(self, pdf_id: str, page_index: int) -> None:
        self.create_page_usecase.execute(pdf_id, page_index)

    def create_pdf(self, pdf_name: str) -> Pdf:
        return self.create_pdf_usecase.execute(pdf_name)
