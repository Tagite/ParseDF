import uuid
from domain.entites.pdf import Pdf
from domain.entites.page import Page
from domain.entites.label import Label
from domain.value_objects.label_type import LabelType
from domain.value_objects.bbox import BBox


class MdPdfConverter:
    @staticmethod
    def md_str_to_pdf(md_str: str) -> Pdf:
        lines = md_str.strip().splitlines()
        if not lines[0].startswith("# File Name:"):
            raise ValueError("Invalid Markdown format: Missing file name")

        file_name = lines[0].split(":")[1].strip()
        pdf = Pdf(file_name=file_name)

        current_page = None
        for line in lines[1:]:
            if line.startswith("## Page"):
                if current_page:
                    pdf.append_page(current_page)
                index = int(line.split()[2])
                current_page = Page(index=index)
            elif line.startswith("- Label:"):
                label_data = line.replace("- Label:", "").strip()
                label_type_str, bbox_str = label_data.split(", BBox:")
                label_type = LabelType(label_type_str.strip())
                bbox_values = tuple(map(float, bbox_str.strip().strip("()").split(",")))
                bbox = BBox(*bbox_values)
                label = Label(label_type=label_type, bbox=bbox)
                if current_page:
                    current_page.add_label(label)
        if current_page:
            pdf.append_page(current_page)

        return pdf

    @staticmethod
    def pdf_to_md_str(pdf: Pdf) -> str:
        md_lines = [f"# File Name: {pdf.file_name}"]

        for page in pdf.pages:
            md_lines.append(f"## Page {page.index}")
            for label in page.labels:
                bbox = label.bbox
                md_lines.append(
                    f"- Label: {label.label_type}, BBox: ({bbox.x1}, {bbox.y1}, {bbox.x2}, {bbox.y2})"
                )

        return "\n".join(md_lines)