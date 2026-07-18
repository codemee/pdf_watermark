"""Tests for bundled watermark font embedding."""

import tempfile
import unittest
from pathlib import Path

import pypdf
from reportlab.pdfgen import canvas

from pdf_watermark import add_watermark


class FontEmbeddingTest(unittest.TestCase):
    def test_watermark_font_is_embedded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.pdf"
            output_path = Path(directory) / "output.pdf"

            source = canvas.Canvas(str(input_path))
            source.drawString(72, 720, "Source document")
            source.save()

            add_watermark(input_path, text="機密 Confidential", output_path=output_path)

            page = pypdf.PdfReader(output_path).pages[0]
            fonts = page["/Resources"]["/Font"]
            watermark_fonts = [
                font_reference.get_object()
                for font_reference in fonts.values()
                if "NotoSansTC" in str(font_reference.get_object().get("/BaseFont", ""))
            ]

            self.assertTrue(watermark_fonts, "Noto Sans TC font resource is missing")
            for font in watermark_fonts:
                descriptor = font["/FontDescriptor"].get_object()
                self.assertIn("/FontFile2", descriptor)


if __name__ == "__main__":
    unittest.main()
