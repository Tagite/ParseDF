import os
import uuid
from pathlib import Path

from domain.entites.pdf import Pdf
from domain.repository.pdf_repo_interface import PdfRepoInterface
from infrastructure.repositories.md_pdf_conveter import MdPdfConverter


class LocalPdfRepo(PdfRepoInterface):
    def __init__(self, hidden_folder: str = ".parseDF"):
        super().__init__()
        self.base_path = self._get_cache_dir(hidden_folder)

        if not (self.base_path.exists() and self.base_path.is_dir()):
            self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_cache_dir(self, folder_name: str) -> Path:
        if os.name == "nt":  # Windows
            base_dir = Path(
                os.getenv("LOCALAPPDATA", Path.home() / "AppData" / folder_name)
            )
        else:  # macOS/Linux
            base_dir = Path(os.getenv("XDG_CACHE_HOME", Path.home() / folder_name))

        return base_dir

    def find_by_id(self, id: str) -> Pdf:
        pdf_list = self._load_md_pdf_data()
        target_pdf = list(filter(lambda x: str(x.id) == id, pdf_list))
        if not len(target_pdf):
            raise ValueError(f"{id} is not found.")
        return target_pdf[0]
    
    def find_by_name(self, pdf_name: str) -> list[Pdf]:
        pdf_list = self._load_md_pdf_data()
        target_pdfs = filter(lambda x: x.file_name == pdf_name, pdf_list)
        if not target_pdfs:
            raise ValueError(f"{pdf_name} is not found.")
        return list(target_pdfs)

    def _load_md_pdf_data(self) -> list[Pdf]:
        md_file_list = self._load_md_file_list()
        md_str_list = list(
            map(
                lambda x: x.read_text(encoding="utf-8"),
                md_file_list,
            )
        )
        md_pdf_list = list(
            map(
                lambda x: MdPdfConverter.md_str_to_pdf(x),
                md_str_list,
            )
        )
        return md_pdf_list

    def _load_md_file_list(self) -> list[Path]:
        file_list = self.base_path.glob("*.md")
        md_list = filter(lambda x: x.is_file(), file_list)
        return list(md_list)

    def save(self, pdf: Pdf) -> None:
        md_str = MdPdfConverter.pdf_to_md_str(pdf)
        file_path = self.base_path / f"{pdf.file_name}.md"
        self._write_file(file_path, md_str)

    def remove_by_id(self, id: uuid.UUID) -> None:
        target_pdf = self.find_by_id(id)
        target_name = target_pdf.file_name
        target_path = self.base_path / f"{target_name}.md"
        self._remove_file(target_path)

    def _write_file(self, file_path: Path, data: str) -> None:
        with file_path.open(mode="w", encoding="utf-8") as file:
            file.write(data)

    def _remove_file(self, file_path: Path) -> None:
        if not (file_path.exists() and file_path.is_file()):
            raise ValueError(f"{file_path} is not a file")
        file_path.unlink()
