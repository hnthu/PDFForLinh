"""
pdf_ops.py

Pure PDF operations: split and join.
No UI dependencies.
"""

import os
from datetime import datetime

from PyPDF2 import PdfReader, PdfWriter


def get_page_count(file_path):
    """Return the number of pages in a PDF file."""
    return len(PdfReader(file_path).pages)


def split_pdf(input_file, ranges_str):
    """
    Split a PDF into segments defined by ranges_str (e.g. "1-3, 4-6, 7").

    Returns a list of output file paths created.
    Raises ValueError for invalid page ranges.
    """
    reader = PdfReader(input_file)
    total_pages = len(reader.pages)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_folder = os.path.dirname(input_file)

    outputs = []
    for part in ranges_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = map(int, part.split('-'))
        else:
            start = end = int(part)

        if start < 1 or end > total_pages or start > end:
            raise ValueError(f"Invalid range '{part}': file has {total_pages} pages")

        writer = PdfWriter()
        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])

        if start == end:
            out_path = os.path.join(output_folder, f"{base_name}_page_{start}.pdf")
        else:
            out_path = os.path.join(output_folder, f"{base_name}_pages_{start}-{end}.pdf")

        with open(out_path, 'wb') as f:
            writer.write(f)
        outputs.append(out_path)

    return outputs


def join_pdfs(files, output_folder):
    """
    Merge a list of PDF files into a single output file.

    Returns the output file path.
    """
    writer = PdfWriter()
    for pdf_file in files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_folder, f"Merged_PDF_{timestamp}.pdf")

    with open(output_file, 'wb') as f:
        writer.write(f)

    return output_file
