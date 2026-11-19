"""Tests for page-aware watermark font sizing."""

import math
import unittest

from reportlab.pdfbase import pdfmetrics

from pdf_watermark import _WATERMARK_FONT, _calculate_font_size


class FontSizingTest(unittest.TestCase):
    def test_short_text_uses_page_relative_maximum(self) -> None:
        self.assertEqual(_calculate_font_size(595, 842, "機密"), 595 / 5)

    def test_long_text_is_scaled_to_fit_diagonal_span(self) -> None:
        width = 595
        height = 842
        text = "這是一段很長的機密浮水印文字 Confidential — Internal Use Only"

        font_size = _calculate_font_size(width, height, text)
        rendered_width = pdfmetrics.stringWidth(text, _WATERMARK_FONT, font_size)
        available_width = min(width, height) * math.sqrt(2) * 0.9

        self.assertLess(font_size, min(width, height) / 5)
        self.assertAlmostEqual(rendered_width, available_width)


if __name__ == "__main__":
    unittest.main()
