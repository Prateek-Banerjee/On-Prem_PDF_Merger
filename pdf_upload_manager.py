import pathlib
from typing import List, Tuple
from errors import FileLimitedExceededError, UnsupportedFileTypeError


class PDFUploadManager:
    """
    Handles uploading and rearrangement of PDF files.
    """

    def __init__(self) -> None:
        self.pdf_files: List[pathlib.Path] = []
        self.__max_files: int = 20

    def add_files(self, pdf_files: List[pathlib.Path]) -> None:
        """Add PDF files to the list (max 20)."""

        for pdf in pdf_files:
            if not self.__is_pdf(pdf):
                raise UnsupportedFileTypeError(
                    f"{pdf.name} is not a PDF file.")

        if (len(self.pdf_files) + len(pdf_files)) > self.__max_files:
            raise FileLimitedExceededError(
                f"Only {self.__max_files} PDF files can be merged at once.")

        self.pdf_files.extend(pdf_files)

    def rearrange_pdf(self, pdf: pathlib.Path, index: int):
        """Rearrange the PDF files in the list."""
        self.pdf_files.remove(pdf)
        self.pdf_files.insert(index, pdf)

    def remove_file(self, pdf: pathlib.Path):
        """Remove a file from the list."""
        self.pdf_files.remove(pdf)

    def get_ordered_files(self) -> Tuple[pathlib.Path, ...]:
        """Return the tuple of PDF files in the arranged order so that it is immutable."""
        return tuple(self.pdf_files)

    def __is_pdf(self, file: pathlib.Path) -> bool:
        return file.suffix.lower() == ".pdf"
