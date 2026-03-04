"""
pdf_ops.py

Pure PDF operations: split and join.
No UI dependencies.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


def get_page_count(path: str | Path) -> int:
    """Return the number of pages in a PDF file."""
    return len(PdfReader(str(path)).pages)


def split_pdf(input_path: str | Path, ranges_str: str) -> list[Path]:
    """Split a PDF into segments defined by *ranges_str* (e.g. ``"1-3, 4-6, 7"``).

    Returns a list of output file paths created.
    Raises :class:`ValueError` for invalid page ranges.
    """
    path = Path(input_path)
    reader = PdfReader(str(path))
    total = len(reader.pages)
    out_dir = path.parent

    outputs: list[Path] = []
    for part in ranges_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = map(int, part.split("-"))
        else:
            start = end = int(part)

        if start < 1 or end > total or start > end:
            raise ValueError(f"Invalid range '{part}': file has {total} pages")

        writer = PdfWriter()
        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])

        name = (
            f"{path.stem}_page_{start}.pdf"
            if start == end
            else f"{path.stem}_pages_{start}-{end}.pdf"
        )
        out_path = out_dir / name
        with out_path.open("wb") as f:
            writer.write(f)
        outputs.append(out_path)

    return outputs


def join_pdfs(files: list[str | Path], output_folder: str | Path) -> Path:
    """Merge a list of PDF files into a single output file.

    Returns the output file path.
    """
    writer = PdfWriter()
    for pdf_file in files:
        for page in PdfReader(str(pdf_file)).pages:
            writer.add_page(page)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(output_folder) / f"Merged_PDF_{timestamp}.pdf"
    with out_path.open("wb") as f:
        writer.write(f)
    return out_path
