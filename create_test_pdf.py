"""Generate a test PDF with three different page sizes for watermark testing."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, A4, LETTER
from reportlab.pdfgen import canvas

OUTPUT = Path(__file__).parent / "test.pdf"


def _page(c: canvas.Canvas, size, title: str, subtitle: str, title_color) -> None:
    w, h = size
    c.setPageSize(size)

    # Title
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(title_color)
    c.drawCentredString(w / 2, h - 90, title)

    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(w / 2, h - 130, subtitle)

    # Body lines
    c.setFont("Helvetica", 13)
    for i, line in enumerate([
        "This document contains confidential information.",
        "Distribution is restricted to authorised personnel only.",
        "Unauthorised copying or disclosure is prohibited.",
        "",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna.",
    ]):
        c.drawString(72, h / 2 - i * 22, line)

    c.showPage()


def create_test_pdf(output: Path = OUTPUT) -> Path:
    c = canvas.Canvas(str(output))

    _page(c, A4,     "Page 1 — A4",     "210 × 297 mm",         colors.darkblue)
    _page(c, LETTER, "Page 2 — Letter", "8.5 × 11 inch",        colors.darkgreen)
    _page(c, A3,     "Page 3 — A3",     "297 × 420 mm (large)", colors.darkred)

    c.save()
    print(f"Test PDF created: {output}")
    return output


if __name__ == "__main__":
    create_test_pdf()
