import pathlib
from typing import Tuple
from pypdf import PdfWriter
from .errors import PdfMergeFailError


class PDFMerger:
    """
    Handles the merging of PDF files.
    Accepts an ordered Tuple of PDFs and generates a merged PDF file.
    """

    def __init__(self, pdf_files: Tuple[pathlib.Path, ...]):
        self.pdf_files: Tuple[pathlib.Path, ...] = pdf_files

    def merge(self, output_file_path: pathlib.Path) -> None:
        """
        Merge all the PDFs in a tuple into one file and saves it to the given output_path.

        Parameters:
            output_file: pathlib.Path
        """
        try:
            pdf_writer: PdfWriter = PdfWriter()

            for pdf in self.pdf_files:
                pdf_writer.append(pdf)

            pdf_writer.write(output_file_path)
            pdf_writer.close()
        except Exception as e:
            raise PdfMergeFailError(f"Failed to merge Pdfs: {e}.")
