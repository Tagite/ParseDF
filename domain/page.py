import uuid
from pydantic import BaseModel
from pydantic import Field

from domain.label import Label
from domain.validator import PositveNumber


class Page(BaseModel):
    index: PositveNumber
    labels: list[Label] = Field(default_factory=list)

    def get_label(self, label_id: uuid.UUID) -> Label:
        target_label = next(filter(lambda x: x.id == label_id, self.labels), None)
        if target_label is None:
            raise ValueError(f"{label_id} is not found")
        return target_label

    def add_label(self, label: Label) -> None:
        self._validate_not_has_label(label)
        self.labels.append(label)

    def remove_label(self, label: Label) -> None:
        self._validate_has_label(label)
        self.labels.remove(label)

    def update_label(self, old_label: Label, new_label: Label) -> None:
        self.remove_label(old_label)
        self.add_label(new_label)

    def _validate_has_label(self, label: Label) -> None:
        if not self._has_label(label):
            raise ValueError("Label is not found")

    def _validate_not_has_label(self, label: Label) -> None:
        if self._has_label(label):
            raise ValueError("Label already exists")

    def _has_label(self, label: Label) -> bool:
        return label in self.labels
