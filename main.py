import sys
from typing import Optional, Dict, List, Tuple
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
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QMouseEvent, QPaintEvent
from PyQt5.QtCore import Qt, QRect, QPoint
import fitz  # PyMuPDF
from PIL import Image
import io
import os


class DrawableQLabel(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.begin: Optional[QPoint] = None
        self.end: Optional[QPoint] = None
        self.is_drawing: bool = False
        self.current_page_boxes: Dict[int, List[QRect]] = {}
        self.current_page: int = 0
        self.scale_factor: float = 1.0

    def set_scale_factor(self, factor: float) -> None:
        self.scale_factor = factor

    def get_pdf_coordinates(self, rect: QRect) -> Tuple[float, float, float, float]:
        x1 = rect.left() / self.scale_factor
        y1 = rect.top() / self.scale_factor
        x2 = rect.right() / self.scale_factor
        y2 = rect.bottom() / self.scale_factor
        return (x1, y1, x2, y2)

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

            if self.current_page in self.current_page_boxes:
                for box in self.current_page_boxes[self.current_page]:
                    painter.drawRect(box)

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

        # Save Annotations Button
        self.save_action: QAction = QAction("Save Annotations", self)
        self.save_action.triggered.connect(self.save_annotations)
        self.toolbar.addAction(self.save_action)

        # Crop PDF Button
        self.crop_action: QAction = QAction("Crop PDF", self)
        self.crop_action.triggered.connect(self.crop_pdf_from_annotations)
        self.toolbar.addAction(self.crop_action)

        # Layout
        self.main_layout: QVBoxLayout = QVBoxLayout()

        # Image Label
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
        page = self.doc.load_page(self.current_page)
        pix = page.get_pixmap()
        
        window_width = self.width() - 50
        scale_factor = window_width / pix.width
        
        image = Image.open(io.BytesIO(pix.tobytes("png")))
        scaled_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        image = image.resize(scaled_size, Image.LANCZOS)
        
        qimage = QImage(
            image.tobytes(),
            image.width,
            image.height,
            image.width * 3,
            QImage.Format.Format_RGB888,
        )
        
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
        self.image_label.set_page(self.current_page)
        self.image_label.set_scale_factor(scale_factor)
        
        self.page_label.setText(f"Page {self.current_page + 1} / {self.num_pages}")
        self.setWindowTitle(f"PDF Viewer - Page {self.current_page + 1} / {self.num_pages}")

    def clear_current_page_boxes(self) -> None:
        self.image_label.clear_boxes()

    def clear_all_boxes(self) -> None:
        self.image_label.clear_all_boxes()

    def show_previous_page(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()

    def show_next_page(self) -> None:
        if self.current_page < self.num_pages - 1:
            self.current_page += 1
            self.update_page()

    def save_annotations(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Annotations", "", "Markdown Files (*.md)"
        )
        if not file_path:
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# PDF Annotations\n\n")
            boxes = self.image_label.get_boxes()
            for page_num in sorted(boxes.keys()):
                if boxes[page_num]:  # 박스가 있는 페이지만 저장
                    f.write(f"## Page {page_num + 1}\n\n")
                    for i, rect in enumerate(boxes[page_num], 1):
                        x1, y1, x2, y2 = self.image_label.get_pdf_coordinates(rect)
                        f.write(f"### Box {i}\n")
                        f.write(f"- Coordinates: [{x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}]\n\n")

    def crop_pdf_from_annotations(self) -> None:
        md_path, _ = QFileDialog.getOpenFileName(
            self, "Open Annotations", "", "Markdown Files (*.md)"
        )
        if not md_path:
            return

        output_dir, _ = QFileDialog.getSaveFileName(
            self, "Save Cropped Images", "", "Select Directory"
        )
        if not output_dir:
            return

        output_dir = os.path.dirname(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        current_page = None
        with open(md_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("## Page"):
                    current_page = int(line.split()[2]) - 1
                elif line.startswith("- Coordinates:"):
                    coords = eval(line.split(": ")[1].strip())
                    if current_page is not None:
                        self.crop_and_save_region(current_page, coords, output_dir)

    def crop_and_save_region(self, page_num: int, coords: List[float], output_dir: str) -> None:
        page = self.doc.load_page(page_num)
        x1, y1, x2, y2 = coords
        
        rect = fitz.Rect(x1, y1, x2, y2)
        pix = page.get_pixmap(clip=rect)
        
        image_path = os.path.join(
            output_dir, f"page_{page_num + 1}_crop_{x1:.0f}_{y1:.0f}.png"
        )
        pix.save(image_path)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    pdf_path: str = "crawler.pdf"
    viewer: PDFViewer = PDFViewer(pdf_path)
    viewer.show()
    sys.exit(app.exec_())