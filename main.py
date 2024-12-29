import sys
from typing import Optional, Dict, List
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QLabel,
    QAction,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QMouseEvent, QPaintEvent
from PyQt5.QtCore import Qt, QRect, QPoint
import fitz  # PyMuPDF
from PIL import Image
import io


class DrawableQLabel(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.begin: Optional[QPoint] = None
        self.end: Optional[QPoint] = None
        self.is_drawing: bool = False
        self.current_page_boxes: Dict[
            int, List[QRect]
        ] = {}  # Dictionary to store boxes for each page
        self.current_page: int = 0

    def set_page(self, page_number: int) -> None:
        self.current_page = page_number
        if page_number not in self.current_page_boxes:
            self.current_page_boxes[page_number] = []
        self.update()

    def mousePressEvent(self, ev: QMouseEvent | None) -> None:
        if ev is None:
            return

        if ev.button() == Qt.MouseButton.LeftButton:
            self.begin = ev.pos()
            self.end = self.begin
            self.is_drawing = True

    def mouseMoveEvent(self, ev: QMouseEvent | None) -> None:
        if ev is None:
            return

        if self.is_drawing:
            self.end = ev.pos()
            self.update()

    def mouseReleaseEvent(self, ev: QMouseEvent | None) -> None:
        if ev is None:
            return

        if ev.button() == Qt.MouseButton.LeftButton:
            self.is_drawing = False
            if self.begin is not None and self.end is not None:
                # Add the completed box to the current page's list
                self.current_page_boxes[self.current_page].append(
                    QRect(self.begin, self.end).normalized()
                )
            self.update()

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        if a0 is None:
            return

        super().paintEvent(a0)
        if self.pixmap():
            painter = QPainter(self)
            painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine))

            # Draw all saved boxes for the current page
            if self.current_page in self.current_page_boxes:
                for box in self.current_page_boxes[self.current_page]:
                    painter.drawRect(box)

            # Draw the current box being created
            if self.begin is not None and self.end is not None and self.is_drawing:
                painter.drawRect(QRect(self.begin, self.end).normalized())

    def clear_boxes(self) -> None:
        if self.current_page in self.current_page_boxes:
            self.current_page_boxes[self.current_page] = []
            self.update()

    def clear_all_boxes(self) -> None:
        self.current_page_boxes = {}
        self.update()

    def get_boxes(self) -> Dict[int, List[QRect]]:
        return self.current_page_boxes


class PDFViewer(QMainWindow):
    def __init__(self, pdf_path: str) -> None:
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Load PDF
        self.pdf_path: str = pdf_path
        self.doc: fitz.Document = fitz.open(pdf_path)
        self.num_pages: int = len(self.doc)
        self.current_page: int = 0

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

        # Clear All Boxes Button
        self.clear_all_action: QAction = QAction("Clear All Pages", self)
        self.clear_all_action.triggered.connect(self.clear_all_boxes)
        self.toolbar.addAction(self.clear_all_action)

        # Layout
        self.main_layout: QVBoxLayout = QVBoxLayout()

        # Image Label (now using custom DrawableQLabel)
        self.image_label: DrawableQLabel = DrawableQLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.image_label)

        # Container
        container: QWidget = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Show first page
        self.update_page()

    def update_page(self) -> None:
        image: Optional[Image.Image] = self.convert_pdf_page_to_image(self.current_page)
        if image:
            qimage: QImage = QImage(
                image.tobytes(),
                image.width,
                image.height,
                image.width * 3,
                QImage.Format.Format_RGB888,
            )
            pixmap: QPixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap)
            self.image_label.set_page(
                self.current_page
            )  # Update current page in DrawableQLabel
            self.page_label.setText(f"Page {self.current_page + 1} / {self.num_pages}")
            self.setWindowTitle(
                f"PDF Viewer - Page {self.current_page + 1} / {self.num_pages}"
            )

    def clear_current_page_boxes(self) -> None:
        self.image_label.clear_boxes()

    def clear_all_boxes(self) -> None:
        self.image_label.clear_all_boxes()

    def convert_pdf_page_to_image(self, page_number: int) -> Optional[Image.Image]:
        page: fitz.Page = self.doc.load_page(page_number)  # Load specific page
        pix: fitz.Pixmap = page.get_pixmap()  # type: ignore [attr-defined]
        image: Image.Image = Image.open(io.BytesIO(pix.tobytes("png")))
        return image

    def show_previous_page(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def show_next_page(self) -> None:
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.update_page()


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    pdf_path: str = "crawler.pdf"  # Replace with your PDF file path
    viewer: PDFViewer = PDFViewer(pdf_path)
    viewer.show()
    sys.exit(app.exec_())
