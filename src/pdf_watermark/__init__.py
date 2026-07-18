"""Add diagonal watermark text to PDF files."""

import io
from pathlib import Path

import pypdf
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics as _pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont as _UnicodeCIDFont
from reportlab.pdfgen import canvas as rl_canvas

WATERMARK_TEXT = "Confidential"
_CJK_FONT = "STSong-Light"
_cjk_font_registered = False


def _ensure_cjk_font() -> None:
    global _cjk_font_registered
    if not _cjk_font_registered:
        _pdfmetrics.registerFont(_UnicodeCIDFont(_CJK_FONT))
        _cjk_font_registered = True


def _create_watermark_page(width: float, height: float, text: str) -> io.BytesIO:
    """Return an in-memory single-page PDF containing only the watermark."""
    packet = io.BytesIO()
    canvas = rl_canvas.Canvas(packet, pagesize=(width, height))

    canvas.saveState()
    canvas.setFillColor(Color(0, 0, 0, alpha=0.15))

    font_size = min(width, height) / 5
    if any(ord(character) > 127 for character in text):
        _ensure_cjk_font()
        font_name = _CJK_FONT
    else:
        font_name = "Helvetica-Bold"
    canvas.setFont(font_name, font_size)

    canvas.translate(width / 2, height / 2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, text)

    canvas.restoreState()
    canvas.save()

    packet.seek(0)
    return packet


def add_watermark(
    input_path: str | Path,
    text: str = WATERMARK_TEXT,
    output_path: str | Path | None = None,
) -> Path:
    """Stamp text as a diagonal watermark on every page of a PDF."""
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_wm{input_path.suffix}"
    else:
        output_path = Path(output_path)

    reader = pypdf.PdfReader(input_path)
    writer = pypdf.PdfWriter()

    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        watermark = _create_watermark_page(width, height, text)
        watermark_page = pypdf.PdfReader(watermark).pages[0]

        page.merge_page(watermark_page)
        writer.add_page(page)

    with output_path.open("wb") as output_file:
        writer.write(output_file)

    return output_path


__all__ = ["WATERMARK_TEXT", "add_watermark"]
