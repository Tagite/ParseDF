from typing import Optional
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPen, QMouseEvent, QPaintEvent
from PyQt5.QtCore import Qt, QRectF, QPointF

from domain.entites.label import Label
from domain.value_objects.label_type import LabelType
from domain.value_objects.bbox import BBox
from domain.value_objects.pos import Pos


class DrawQLabel(QLabel):
    def __init__(self, sender: object) -> None:
        super().__init__()
        self.begin: Optional[QPointF] = None
        self.end: Optional[QPointF] = None
        self.is_drawing: bool = False
        self.sender = sender
        self.label_type = "table"

    def normalize_point(self, point: QPointF) -> QPointF:
        if not self.pixmap():
            return point

        pixmap_size = self.pixmap().size()
        widget_size = self.size()
        scale_x = pixmap_size.width() / widget_size.width()
        scale_y = pixmap_size.height() / widget_size.height()

        return QPointF(point.x() * scale_x, point.y() * scale_y)

    def denormalize_point(self, point: QPointF) -> QPointF:
        if not self.pixmap():
            return point

        pixmap_size = self.pixmap().size()
        widget_size = self.size()
        scale_x = widget_size.width() / pixmap_size.width()
        scale_y = widget_size.height() / pixmap_size.height()

        return QPointF(point.x() * scale_x, point.y() * scale_y)

    def mousePressEvent(self, ev: QMouseEvent | None) -> None:
        if ev is None:
            return

        if ev.button() == Qt.MouseButton.LeftButton:
            self.begin = self.normalize_point(ev.localPos())
            self.end = self.begin
            self.is_drawing = True

    def mouseMoveEvent(self, ev: QMouseEvent | None) -> None:
        if ev is None:
            return

        if self.is_drawing:
            self.end = self.normalize_point(ev.localPos())
            self.update()

    def mouseReleaseEvent(self, ev: QMouseEvent | None) -> None:
        if ev is None:
            return

        if ev.button() == Qt.MouseButton.LeftButton:
            self.is_drawing = False
            if self.begin is not None and self.end is not None:
                self.send_bboxes(
                    QRectF(self.begin, self.end).normalized()
                )
            self.update()

    def send_bboxes(self, rect: QRectF) -> None:
        label: Label = Label(
            label_type=LabelType(name=self.label_type),
            bbox=BBox(
                top_left=Pos(x=rect.topLeft().x(), y=rect.topLeft().y()),
                bottom_right=Pos(x=rect.bottomRight().x(), y=rect.bottomRight().y()),
            ),
        )
        self.sender.add_label(label)

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        if a0 is None:
            return
        super().paintEvent(a0)
        
        if not self.pixmap():
            return
        
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine))

        for label in self.sender.get_labels():
            denormalized_rect = QRectF(
                self.denormalize_point(QPointF(label.bbox.top_left.x, label.bbox.top_left.y)),
                self.denormalize_point(QPointF(label.bbox.bottom_right.x, label.bbox.bottom_right.y)),
            )
            painter.drawRect(denormalized_rect)

        if self.begin is not None and self.end is not None and self.is_drawing:
            temp_rect = QRectF(
                self.denormalize_point(self.begin), self.denormalize_point(self.end)
            ).normalized()
            painter.drawRect(temp_rect)
