import pathlib
from typing import List, Tuple
from .errors import FileLimitedExceededError, UnsupportedFileTypeError

PDF_EXTENSION = ".pdf"


class PDFUploadManager:
    """
    Handles uploading, rearrangement and removal of PDF files.
    """

    def __init__(self) -> None:
        self.pdf_files: List[pathlib.Path] = []
        self.__max_files: int = 20

    def add_files(self, pdf_files: List[pathlib.Path]) -> None:
        """
        Adds at most 20 PDF files to the list. Only PDF files are allowed.

        Parameters:
            pdf_files(List[pathlib.Path]):

        Returns:
            None
        """

        for pdf in pdf_files:
            if not self.__is_pdf(pdf):
                raise UnsupportedFileTypeError(
                    f"{pdf.name} is not a PDF file.")

        if (len(self.pdf_files) + len(pdf_files)) > self.__max_files:
            raise FileLimitedExceededError(
                f"Only {self.__max_files} PDF files can be merged at once.")

        self.pdf_files.extend(pdf_files)

    def rearrange_pdf(self, pdf: pathlib.Path, index: int) -> None:
        """
        Rearranges a PDF file in a list. Removes the file from the list and inserts it at the requested index.

        Parameters:
            pdf (pathlib.Path): The PDF file to be moved.
            index (int): The index where the PDF file is to be moved.

        Returns:
            None
        """

        self.pdf_files.remove(pdf)
        self.pdf_files.insert(index, pdf)

    def remove_file(self, pdf: pathlib.Path) -> None:
        """
        Removes a PDF file from the list.

        Parameters:
            pdf (pathlib.Path): The PDF file to be removed.

        Returns:
            None
        """

        self.pdf_files.remove(pdf)

    def get_ordered_files(self) -> Tuple[pathlib.Path, ...]:
        """
        Return a tuple of PDF files in the arranged order so that it is immutable.

        Returns:
            out (Tuple[pathlib.Path, ...]):
        """

        return tuple(self.pdf_files)

    def __is_pdf(self, file: pathlib.Path) -> bool:
        """
        Checks whether a provided file is a PDF or not.

        Parameters:
            file (pathlib.Path): The file to be checked.

        Returns:
            out (bool):
        """

        return file.suffix.lower() == PDF_EXTENSION
