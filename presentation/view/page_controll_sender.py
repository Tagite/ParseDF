from domain.entites.label import Label
from presentation.controllers.page_controller import PageController


class PageControllSender:
    def __init__(self,
                 pdf_id: str,
                 page_index: int,
                 controller: PageController,
                 ):
        self.pdf_id: str = pdf_id
        self.page_index: int = page_index
        self.controller: PageController = controller

    def add_label(self, label: Label):
        self.controller.add_label(self.pdf_id, self.page_index, label)
    
    def get_labels(self):
        return self.controller.get_labels(self.pdf_id, self.page_index)
    