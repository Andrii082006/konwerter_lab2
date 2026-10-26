
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from converter import (
    available_targets,
    convert,
    find_libreoffice,
)


class TestLab3(unittest.TestCase):

    def test_available_targets(self):
        self.assertEqual(
            available_targets(Path("plik.txt")),
            [".docx"]
        )
        self.assertEqual(
            available_targets(Path("plik.docx")),
            [".pdf"]
        )
        self.assertEqual(
            available_targets(Path("plik.odt")),
            [".pdf"]
        )

    def test_txt_to_docx(self):
        from docx import Document

        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "tekst.txt"
            source.write_text(
                "Zażółć gęślą jaźń\nDrugi akapit",
                encoding="utf-8"
            )

            result = convert(source, "docx", folder)
            document = Document(result)

            self.assertEqual(
                [p.text for p in document.paragraphs],
                ["Zażółć gęślą jaźń", "Drugi akapit"]
            )

    def test_missing_libreoffice(self):
        with patch("converter.shutil.which", return_value=None):
            with patch("converter.Path.is_file", return_value=False):
                with self.assertRaisesRegex(
                    RuntimeError, "LibreOffice"
                ):
                    find_libreoffice()

    def test_unsupported_conversion(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source = folder / "tekst.txt"
            source.write_text("Test", encoding="utf-8")

            with self.assertRaisesRegex(
                ValueError, "Nieobsługiwana"
            ):
                convert(source, "pdf", folder)


if __name__ == "__main__":
    unittest.main()
