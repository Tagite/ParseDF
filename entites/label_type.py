from dataclasses import dataclass


DEFAULT_LABEL_LIST = ["table", "image"]


@dataclass(frozen=True)
class LabelTypeManager:
    types: set[str] = set(DEFAULT_LABEL_LIST)

    def add_type(self, label_type: str) -> None:
        if self.is_register(label_type):
            raise ValueError(f"{label_type} is already registered")
        self.types.add(label_type)

    def remove_type(self, label_type: str) -> None:
        if not self.is_register(label_type):
            raise ValueError(f"{label_type} is not registered")
        self.types.remove(label_type)

    def is_register(self, label_type: str) -> bool:
        return label_type in self.types

    def __repr__(self):
        return f"LabelTypeManager(types={self.types})"
