import sys
from typing import List
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QLabel,
    QAction,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import typer

from presentation.controllers.pdf_controller import PdfController
from presentation.controllers.page_controller import PageController
from presentation.view.draw_label import DrawQLabel
from presentation.view.page_controll_sender import PageControllSender


class PDFViewer(QMainWindow):
    def __init__(
        self,
        pdf_path: str,
        pdf_controller: PdfController,
        page_controller: PageController,
    ) -> None:
        super().__init__()
        self.pdf_controller = pdf_controller
        self.page_controller = page_controller
        
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.current_page: int = 0
        
        self.pdf = self.pdf_controller.create_pdf(pdf_path)
        self.page_sender = PageControllSender(pdf_id=str(self.pdf.id),
                                                page_index=self.current_page,
                                               controller=self.page_controller)

        self.doc: fitz.Document = fitz.open(pdf_path)
        self.num_pages: int = len(self.doc)
        for i in range(self.num_pages):
            try:
                self.pdf_controller.create_page(str(self.pdf.id), i)
            except ValueError:
                pass


        # Create Toolbar
        self.toolbar: QToolBar = QToolBar("Navigation Toolbar")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        # Previous Button
        self.prev_action: QAction = QAction("< Previous", self)
        self.prev_action.triggered.connect(self.show_previous_page)
        self.toolbar.addAction(self.prev_action)

        # Page Display Label
        self.page_label: QLabel = QLabel(
            f"Page {self.current_page + 1} / {self.num_pages}"
        )
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toolbar.addWidget(self.page_label)

        # Next Button
        self.next_action: QAction = QAction("Next >", self)
        self.next_action.triggered.connect(self.show_next_page)
        self.toolbar.addAction(self.next_action)

        # Clear Current Page Boxes Button
        self.clear_action: QAction = QAction("Clear Current Page", self)
        self.clear_action.triggered.connect(self.clear_current_page_boxes)
        self.toolbar.addAction(self.clear_action)

        # Layout
        self.main_layout: QVBoxLayout = QVBoxLayout()

        # Image Label
        self.image_label: DrawQLabel = DrawQLabel(self.page_sender)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.main_layout.addWidget(self.image_label)

        # Container
        container: QWidget = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Show first page
        self.update_page()

    def update_page(self) -> None:
        self.page_sender.page_index = self.current_page
        page = self.doc.load_page(self.current_page)
        self.page_sender = PageControllSender(pdf_id=str(self.pdf.id),
                                                page_index=self.current_page,
                                               controller=self.page_controller)
        self.image_label.sender = self.page_sender
        pix = page.get_pixmap()  # type: ignore [attr-defined]

        window_width = self.width() - 50
        scale_factor = window_width / pix.width

        image = Image.open(io.BytesIO(pix.tobytes("png")))
        scaled_size = (
            int(image.width * scale_factor),
            int(image.height * scale_factor),
        )
        image = image.resize(scaled_size, Image.LANCZOS)  # type: ignore [attr-defined]

        qimage = QImage(
            image.tobytes(),
            image.width,
            image.height,
            image.width * 3,
            QImage.Format.Format_RGB888,
        )

        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
        

        self.page_label.setText(f"Page {self.current_page + 1} / {self.num_pages}")
        self.setWindowTitle(
            f"PDF Viewer - Page {self.current_page + 1} / {self.num_pages}"
        )

    def clear_current_page_boxes(self) -> None:
        labels = self.page_controller.get_labels(str(self.pdf.id), self.current_page)
        for label in labels:
            self.page_controller.remove_label(str(self.pdf.id), self.current_page, str(label.id))
        self.update_page()

    def show_previous_page(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def show_next_page(self) -> None:
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.update_page()

