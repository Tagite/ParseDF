import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QLabel,
    QAction,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF
from PIL import Image
import io


class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Load PDF
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.num_pages = len(self.doc)
        self.current_page = 0

        # Create Toolbar
        self.toolbar = QToolBar("Navigation Toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Previous Button
        self.prev_action = QAction("< Previous", self)
        self.prev_action.triggered.connect(self.show_previous_page)
        self.toolbar.addAction(self.prev_action)

        # Page Display Label
        self.page_label = QLabel(f"Page {self.current_page + 1} / {self.num_pages}")
        self.page_label.setAlignment(Qt.AlignCenter)
        self.toolbar.addWidget(self.page_label)

        # Next Button
        self.next_action = QAction("Next >", self)
        self.next_action.triggered.connect(self.show_next_page)
        self.toolbar.addAction(self.next_action)

        # Layout
        self.layout = QVBoxLayout()

        # Image Label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Container
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Show first page
        self.update_page()

    def update_page(self):
        image = self.convert_pdf_page_to_image(self.current_page)
        if image:
            qimage = QImage(
                image.tobytes(),
                image.width,
                image.height,
                image.width * 3,
                QImage.Format_RGB888,
            )
            pixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap)
            self.page_label.setText(f"Page {self.current_page + 1} / {self.num_pages}")
            self.setWindowTitle(
                f"PDF Viewer - Page {self.current_page + 1} / {self.num_pages}"
            )

    def convert_pdf_page_to_image(self, page_number):
        page = self.doc.load_page(page_number)  # Load specific page
        pix = page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes("png")))
        return image

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def show_next_page(self):
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.update_page()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pdf_path = "crawler.pdf"  # Replace with your PDF file path
    viewer = PDFViewer(pdf_path)
    viewer.show()
    sys.exit(app.exec_())
