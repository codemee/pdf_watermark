"""Smoke-test an installed wheel or source distribution."""

import tempfile
from pathlib import Path

import pypdf
from reportlab.pdfgen import canvas

from pdf_watermark import add_watermark


with tempfile.TemporaryDirectory() as directory:
    input_path = Path(directory) / "input.pdf"
    output_path = Path(directory) / "output.pdf"

    source = canvas.Canvas(str(input_path))
    source.drawString(72, 720, "Source document")
    source.save()

    add_watermark(
        input_path,
        text="機密 Confidential",
        output_path=output_path,
    )

    page = pypdf.PdfReader(output_path).pages[0]
    fonts = page["/Resources"]["/Font"]
    assert any(
        "NotoSansTC" in str(reference.get_object().get("/BaseFont", ""))
        for reference in fonts.values()
    ), "embedded Noto Sans TC font was not found"
