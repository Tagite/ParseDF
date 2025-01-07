from pydantic import BaseModel, Field

from entites.label import Label


class Page(BaseModel):
    labels: list[Label] = Field(
        default_factory=list,
        private=True)

    def add_label(self, label: Label) -> None:
        self.labels.append(label)

    def get_label(self, label_id: str) -> Label:
        label = next((label for label in self.labels if label.id == label_id), None)
        if label is None:
            raise ValueError(f"{label_id} is not found")
        return label

    def remove_label(self, label_id: str) -> None:
        new_labels = [label for label in self.labels if label.id != label_id]
        if len(new_labels) == len(self.labels):  # No label was removed
            raise ValueError(f"{label_id} is not found")
        self.labels = new_labels
    
    class config:
        frozen = True
