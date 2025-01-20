import uuid
from pathlib import Path

from domain.pdf import Pdf
from adapters.pdf_repo_interface import PdfRepoInterface
from adapters.md_pdf_conveter import MdPdfConveter


class LocalPdfRepo(PdfRepoInterface):
    def __init__(self, hidden_folder: str = ".parseDF"):
        super().__init__()
        self.base_path = Path(hidden_folder)

        if not (self.base_path.exists() and self.base_path.is_dir()):
            self.base_path.mkdir(parents=True, exist_ok=True)

    def find_by_id(self, id: uuid.UUID) -> Pdf:
        pdf_list = self._load_md_pdf_data()
        target_pdf = filter(lambda x: x.id == id, pdf_list)
        if not target_pdf:
            raise ValueError(f"{id} is not found.")
        return next(target_pdf)

    def find_by_name(self, pdf_name: str) -> list[Pdf]:
        pdf_list = self._load_md_pdf_data()
        target_pdfs = filter(lambda x: x.file_name == pdf_name, pdf_list)
        if not target_pdfs:
            raise ValueError(f"{id} is not found.")
        return list(target_pdfs)

    def _load_md_pdf_data(self) -> list[Pdf]:
        md_file_list = self._load_md_list()
        md_str_list = list(
            map(
                lambda x: x.read_text(encoding="utf-8"),
                md_file_list,
            )
        )
        md_pdf_list = list(
            map(
                lambda x: MdPdfConveter.md_str_to_pdf(x),
                md_str_list,
            )
        )
        return md_pdf_list

    def _load_md_file_list(self) -> list[str]:
        file_list = self.base_path.glob("*.md")
        md_list = filter(lambda x: x.is_file(), file_list)
        return list(md_list)

    def save(self, pdf: Pdf) -> None:
        md_str = MdPdfConveter.pdf_to_md_str(pdf)
        file_path = self.base_path / pdf.file_name
        self._write_file(file_path, md_str)

    def remove_by_id(self, id: uuid.UUID) -> None:
        target_pdf = self.find_by_id(id)
        target_name = target_pdf.file_name
        target_path = self.base_path / target_name
        self._remove_file(target_path)

    def _write_file(self, file_path: Path, data: str) -> None:
        with file_path.open(mode="w", encoding="utf-8") as file:
            file.write(data)

    def _remove_file(self, file_path: Path) -> None:
        if not (file_path.exists() and file_path.is_file()):
            raise ValueError(f"{file_path} is not file")
        file_path.unlink()
