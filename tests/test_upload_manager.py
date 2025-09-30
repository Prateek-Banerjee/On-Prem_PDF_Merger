import os
import sys
import pathlib
from unittest import TestCase

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from src.pdf_upload_manager import PDFUploadManager
from src.errors import FileLimitedExceededError, UnsupportedFileTypeError

class TestUploadManager(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = pathlib.Path(__file__).parent / "data"
        cls.pdf_files = sorted(cls.data_dir.glob(
            "*.pdf"))
        cls.non_pdf_file = cls.data_dir / "not_a_pdf.txt"

    def setUp(self):
        self.manager = PDFUploadManager()

    def test_add_files_under_limit(self):
        # Add 5 valid PDF files (less than 20)
        files_to_add = self.pdf_files[:5]
        self.manager.add_files(files_to_add)
        self.assertEqual(len(self.manager.get_ordered_files()), 5)
        self.assertEqual(self.manager.get_ordered_files(), tuple(files_to_add))

    def test_add_non_pdf_file_raises_error(self):
        # Simulate a non-PDF file
        with self.assertRaises(UnsupportedFileTypeError):
            self.manager.add_files([self.non_pdf_file])

    def test_add_more_than_max_files_raises_error(self):
        with self.assertRaises(FileLimitedExceededError):
            self.manager.add_files(self.pdf_files)

    def test_rearrange_pdf_file(self):
        files_to_add = self.pdf_files[:3]
        self.manager.add_files(files_to_add)

        # Rearrange file2 to the start
        self.manager.rearrange_pdf(files_to_add[2], 0)
        ordered_files = self.manager.get_ordered_files()

        self.assertEqual(ordered_files[0], files_to_add[2])
        self.assertEqual(len(ordered_files), 3)

    def test_remove_file(self):
        files_to_add = self.pdf_files[:2]
        self.manager.add_files(files_to_add)

        self.manager.remove_file(files_to_add[0])
        ordered_files = self.manager.get_ordered_files()

        self.assertEqual(len(ordered_files), 1)
        self.assertEqual(ordered_files[0], files_to_add[1])

    def test_get_ordered_files_returns_tuple(self):
        files_to_add = self.pdf_files[:2]
        self.manager.add_files(files_to_add)

        result = self.manager.get_ordered_files()
        self.assertIsInstance(result, tuple)
        self.assertEqual(result, tuple(files_to_add))
