import pathlib
import tempfile
import os
import sys
from unittest import TestCase
from pypdf import PdfReader

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from src.pdf_merge_logic import PDFMerger
from src.errors import PdfMergeFailError

class TestPDFMerger(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = pathlib.Path(__file__).parent / "data"
        cls.pdf_files = sorted(cls.data_dir.glob("*.pdf"))[:3]
        cls.invalid_file = cls.data_dir / "corrupt_or_missing.pdf"

    def test_merge_successfully_creates_output_file(self):
        merger = PDFMerger(tuple(self.pdf_files))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
            output_path = pathlib.Path(temp_output.name)

        try:
            merger.merge(output_path)
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)

            # Check page count in the finally merged pdf
            reader = PdfReader(str(output_path))
            expected_pages = sum(len(PdfReader(str(pdf)).pages) for pdf in self.pdf_files)
            self.assertEqual(len(reader.pages), expected_pages)
        finally:
            output_path.unlink(missing_ok=True)

    def test_merge_with_invalid_file_raises_error(self):
        invalid_files = list(self.pdf_files[:2]) + [self.invalid_file]
        merger = PDFMerger(tuple(invalid_files))

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
            output_path = pathlib.Path(temp_output.name)

        with self.assertRaises(PdfMergeFailError):
            merger.merge(output_path)

        output_path.unlink(missing_ok=True)
