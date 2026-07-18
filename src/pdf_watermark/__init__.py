"""Add diagonal watermark text to PDF files."""

import io
from importlib.resources import as_file, files
from pathlib import Path

import pypdf
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics as _pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as _TTFont
from reportlab.pdfgen import canvas as rl_canvas

WATERMARK_TEXT = "Confidential"
_WATERMARK_FONT = "NotoSansTC"
_FONT_RESOURCE = "fonts/NotoSansTC-Regular.ttf"
_font_registered = False


def _ensure_watermark_font() -> None:
    """Register the bundled font so ReportLab embeds it in generated PDFs."""
    global _font_registered
    if not _font_registered:
        font_resource = files(__package__).joinpath(_FONT_RESOURCE)
        with as_file(font_resource) as font_path:
            _pdfmetrics.registerFont(_TTFont(_WATERMARK_FONT, font_path))
        _font_registered = True


def _create_watermark_page(width: float, height: float, text: str) -> io.BytesIO:
    """Return an in-memory single-page PDF containing only the watermark."""
    packet = io.BytesIO()
    canvas = rl_canvas.Canvas(packet, pagesize=(width, height))

    canvas.saveState()
    canvas.setFillColor(Color(0, 0, 0, alpha=0.15))

    font_size = min(width, height) / 5
    _ensure_watermark_font()
    canvas.setFont(_WATERMARK_FONT, font_size)

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

        writer.add_page(page)
        writer.pages[-1].merge_page(watermark_page)

    with output_path.open("wb") as output_file:
        writer.write(output_file)

    return output_path


__all__ = ["WATERMARK_TEXT", "add_watermark"]
