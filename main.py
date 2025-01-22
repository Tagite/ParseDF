from PyQt5.QtWidgets import QApplication
import sys
import typer

from application.usecases.page.add_label_usecase import AddLabelUseCase
from application.usecases.page.get_label_usecase import GetLabelUseCase
from application.usecases.page.remove_label_usecase import RemoveLabelUseCase
from application.usecases.page.update_label_usecase import UpdateLabelUseCase
from application.usecases.page.get_all_labels_usecase import GetAllLabelsUseCase
from application.usecases.pdf.create_pdf_usecase import CreatePdfUsecase
from application.usecases.pdf.create_page_usecase import CreatePageUseCase
from application.usecases.pdf.get_pdf_usecase import GetPdfUsecase
from application.usecases.pdf.remove_pdf_usecase import RemovePdfUsecase
from application.usecases.pdf.update_pdf_usecase import UpdatePdfUsecase

from infrastructure.repositories.local_pdf_repo import LocalPdfRepo

from presentation.view.main_window import PDFViewer
from presentation.controllers.pdf_controller import PdfController
from presentation.controllers.page_controller import PageController


def main(pdf_path: str):
    pdf_repo = LocalPdfRepo()


    pdf_controller = PdfController(
        GetPdfUsecase(pdf_repo),
        UpdatePdfUsecase(pdf_repo),
        RemovePdfUsecase(pdf_repo),
        CreatePageUseCase(pdf_repo),
        CreatePdfUsecase(pdf_repo),
    )
    page_controller = PageController(
        AddLabelUseCase(pdf_repo),
        GetLabelUseCase(pdf_repo),
        RemoveLabelUseCase(pdf_repo),
        UpdateLabelUseCase(pdf_repo),
        GetAllLabelsUseCase(pdf_repo),
    )

    app: QApplication = QApplication(sys.argv)
    viewer: PDFViewer = PDFViewer(pdf_path,
                                  pdf_controller,
                                page_controller)
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    typer.run(main)