import subprocess
import tempfile
from pathlib import Path

from docx import Document as DocxDocument
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader
from pypdf import PdfReader


def _read_pdf(file_path: Path) -> list[Document]:
    reader = PdfReader(str(file_path))
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file_path.name,
                        "page": page_number,
                    },
                )
            )

    return documents


def _read_docx(file_path: Path) -> list[Document]:
    doc = DocxDocument(str(file_path))

    paragraphs = [
        paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()
    ]

    table_text = [
        cell.text
        for table in doc.tables
        for row in table.rows
        for cell in row.cells
        if cell.text.strip()
    ]

    text = "\n".join(paragraphs + table_text)

    if not text.strip():
        return []

    return [Document(page_content=text, metadata={"source": file_path.name})]


def _convert_doc_to_pdf(file_path: Path, output_dir: Path) -> Path:
    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(file_path),
        ],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    converted_path = output_dir / f"{file_path.stem}.pdf"

    if result.returncode != 0 or not converted_path.exists():
        raise ValueError(
            f"Could not convert legacy DOC file: "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )

    return converted_path


def _read_with_unstructured(file_path: Path) -> list[Document]:
    loader = UnstructuredLoader(file_path=str(file_path))

    documents = loader.load()

    return [
        Document(
            page_content=doc.page_content,
            metadata={**doc.metadata, "source": file_path.name},
        )
        for doc in documents
        if doc.page_content and doc.page_content.strip()
    ]


def load_document(
    file_bytes: bytes,
    file_name: str,
) -> list[Document]:
    if not file_bytes:
        return []

    suffix = Path(file_name).suffix.lower()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        input_path = temp_path / f"input{suffix}"

        input_path.write_bytes(file_bytes)

        is_pdf = file_bytes.startswith(b"%PDF-")
        is_zip = file_bytes.startswith(b"PK\x03\x04")
        is_ole = file_bytes.startswith(bytes.fromhex("D0CF11E0A1B11AE1"))

        try:
            if is_pdf or suffix == ".pdf":
                return _read_pdf(input_path)

            if suffix == ".docx" or (is_zip and suffix == ".docx"):
                return _read_docx(input_path)

            if suffix == ".doc" or is_ole:
                converted_pdf = _convert_doc_to_pdf(
                    input_path,
                    temp_path,
                )
                return _read_pdf(converted_pdf)

            return _read_with_unstructured(input_path)

        except subprocess.TimeoutExpired as exc:
            raise ValueError("Document conversion timed out.") from exc

        except Exception as exc:
            raise ValueError(
                f"Could not extract text from '{file_name}': {exc}"
            ) from exc
