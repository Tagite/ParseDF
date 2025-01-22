from domain.entites.label import Label
from application.usecases.page import add_label_usecase
from application.usecases.page import get_label_usecase
from application.usecases.page import remove_label_usecase
from application.usecases.page import update_label_usecase
from application.usecases.page import get_all_labels_usecase


class PageController:
    def __init__(
        self,
        add_label_usecase: add_label_usecase.AddLabelUseCase,
        get_label_usecase: get_label_usecase.GetLabelUseCase,
        remove_label_usecase: remove_label_usecase.RemoveLabelUseCase,
        update_label_usecase: update_label_usecase.UpdateLabelUseCase,
        get_all_labels_usecase: get_all_labels_usecase.GetAllLabelsUseCase,
    ):
        self.add_label_usecase = add_label_usecase
        self.get_label_usecase = get_label_usecase
        self.remove_label_usecase = remove_label_usecase
        self.update_label_usecase = update_label_usecase
        self.get_all_labels_usecase = get_all_labels_usecase

    def get_labels(self, pdf_id: str, page_index: int) -> list[Label]:
        return self.get_all_labels_usecase.execute(pdf_id, page_index)

    def add_label(self, pdf_id: str, page_index: int, label: Label) -> None:
        self.add_label_usecase.execute(pdf_id, page_index, label)

    def get_label(self, pdf_id: str, page_index: int, label_id: str) -> Label:
        return self.get_label_usecase.execute(pdf_id, page_index, label_id)

    def remove_label(self, pdf_id: str, page_index: int, label_id: str) -> None:
        self.remove_label_usecase.execute(pdf_id, page_index, label_id)

    def update_label(
        self, pdf_id: str, page_index: int, old_label_id: str, new_label: Label
    ) -> None:
        self.update_label_usecase.execute(pdf_id, page_index, old_label_id, new_label)
