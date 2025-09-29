import pathlib
from typing import Tuple
from pypdf import PdfWriter
from errors import PdfMergeFailError


class PDFMerger:
    """
    Handles the merging of PDF files.
    Accepts an ordered Tuple of PDFs and outputs a merged file.
    """

    def __init__(self, pdf_files: Tuple[pathlib.Path, ...]):
        self.pdf_files: Tuple[pathlib.Path, ...] = pdf_files

    def merge(self, output_path: pathlib.Path, output_filename: str) -> None:
        """
        Merge the PDFs into one file and save to the given output_path.
        """
        try:
            pdf_writer: PdfWriter = PdfWriter()

            for pdf in self.pdf_files:
                pdf_writer.append(pdf)

            output_file: pathlib.Path = output_path.joinpath(output_filename)

            pdf_writer.write(output_file)
            pdf_writer.close()
        except Exception as e:
            raise PdfMergeFailError(f"Failed to merge Pdfs: {e}.")
