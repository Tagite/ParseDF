from pydantic import BaseModel


DEFAULT_LABEL_LIST = ["table", "image"]


class LabelTypeManager(BaseModel):
    types: set[str] = set(DEFAULT_LABEL_LIST)

    def add_type(self, label_type: str) -> None:
        self.types.add(label_type)

    def remove_type(self, label_type: str) -> None:
        if not self.is_register(label_type):
            raise ValueError(f"{label_type} is not registered")
        self.types.remove(label_type)

    def is_register(self, label_type: str) -> bool:
        return label_type in self.types

    def __repr__(self):
        return f"LabelTypeManager(types={self.types})"
    
    class Config:
        frozen = True
