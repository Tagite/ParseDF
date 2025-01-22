import uuid
from domain.entites.pdf import Pdf
from domain.entites.page import Page
from domain.entites.label import Label
from domain.value_objects.label_type import LabelType
from domain.value_objects.bbox import BBox
from domain.value_objects.pos import Pos


class MdPdfConverter:
    @staticmethod
    def md_str_to_pdf(md_str: str) -> Pdf:
        lines = md_str.strip().splitlines()
        if not lines[0].startswith("# File ID:"):
            raise ValueError("Invalid Markdown format: Missing file ID")

        pdf_id = uuid.UUID(lines[0].split(":")[1].strip())

        if not lines[1].startswith("# File Name:"):
            raise ValueError("Invalid Markdown format: Missing file name")

        file_name = lines[1].split(":")[1].strip()
        pdf = Pdf(id=pdf_id, file_name=file_name)

        current_page = None
        for line in lines[2:]:
            if line.startswith("## Page"):
                if current_page:
                    pdf.append_page(current_page)
                index = int(line.split()[2])
                current_page = Page(index=index)
            elif line.startswith("- Label:"):
                label_data = line.replace("- Label:", "").strip()
                id_str, label_type_str, bbox_str = label_data.split(", ", maxsplit=2)
                label_id = uuid.UUID(id_str.split(":")[1].strip())
                label_type = LabelType(name=label_type_str.split(":")[1].strip())

                # 디버깅: bbox_str 확인
                print(f"Raw bbox_str: {bbox_str}")

                # 안전한 bbox_values 처리
                bbox_values = tuple(
                    map(
                        float,
                        bbox_str.strip()
                        .replace("BBox:", "")
                        .replace("(", "")
                        .replace(")", "")
                        .split(","),
                    )
                )
                bbox = BBox(
                    top_left=Pos(x=bbox_values[0], y=bbox_values[1]),
                    bottom_right=Pos(x=bbox_values[2], y=bbox_values[3]),
                )
                label = Label(id=label_id, label_type=label_type, bbox=bbox)
                if current_page:
                    current_page.add_label(label)
        if current_page:
            pdf.append_page(current_page)

        return pdf

    @staticmethod
    def pdf_to_md_str(pdf: Pdf) -> str:
        md_lines = [
            f"# File ID: {pdf.id}",
            f"# File Name: {pdf.file_name}",
        ]

        for page in pdf.pages:
            md_lines.append(f"## Page {page.index}")
            for label in page.labels:
                bbox: BBox = label.bbox
                top_left: Pos = bbox.top_left
                bottom_right: Pos = bbox.bottom_right
                md_lines.append(
                    f"- Label: ID: {label.id}, Type: {label.label_type.name}, BBox: ({top_left.x}, {top_left.y}, {bottom_right.x}, {bottom_right.y})"
                )

        return "\n".join(md_lines)
