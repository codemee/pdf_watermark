# pdf-watermark implementation details

English | [繁體中文](implementation.zh-TW.md)

## Project layout

| Path | Purpose |
|---|---|
| `src/pdf_watermark/__init__.py` | Core watermark generation and PDF merging |
| `src/pdf_watermark/cli.py` | Command-line parsing and multi-file processing |
| `src/pdf_watermark/__main__.py` | Support for `python -m pdf_watermark` |
| `create_test_pdf.py` | Generate a manual test document with mixed page sizes |

## Processing flow

1. `cli.main()` uses `argparse` to parse input files and `--text`.
2. Each input path is passed to `add_watermark()` in sequence.
3. `pypdf.PdfReader` reads the source PDF and obtains each page's `mediabox` width and height.
4. `_create_watermark_page()` uses ReportLab to generate an equally sized, single-page PDF in memory.
5. The source page is added to `PdfWriter`, then `merge_page()` overlays the watermark on the writer-owned page.
6. After all pages are processed, the result is written as `<original-name>_wm.pdf`.

The watermark page uses `io.BytesIO`, so the merge does not require temporary PDF files.

## Watermark layout

- Font size is one fifth of the shorter page dimension: `min(width, height) / 5`.
- The canvas origin is translated to the page center and then rotated 45 degrees.
- `drawCentredString()` centers the text along the rotated horizontal axis.
- The fill is black at 15% opacity.
- A separate watermark is generated for every page, allowing A4, Letter, A3, and other sizes in one document.

## Font handling

All watermark text uses the bundled `NotoSansTC-Regular.ttf`. `importlib.resources` locates the font as a package resource, while `TTFont` embeds a subset containing the glyphs used by the watermark PDF. The merged page therefore does not depend on the rendering environment having the same font installed.

The font is registered only once per process to avoid repeated parsing across pages and files. It is distributed under the SIL Open Font License 1.1, included at `src/pdf_watermark/fonts/OFL.txt`.

## Output and error behavior

- Without an explicit output path, the result is placed next to the input with an `_wm` suffix.
- The public Python API, `add_watermark()`, accepts `output_path` for a custom destination.
- The CLI processes multiple files sequentially. A read, merge, or write exception stops execution and is displayed by the shell.
- The core function does not modify the source file.

## Known limitations

- The CLI does not yet expose output path, angle, opacity, color, or font options.
- Layout uses the page `mediabox`; unusual `cropbox` or page rotation settings may require additional handling.
- Font embedding removes the system-font dependency but makes output files somewhat larger.
- Encrypted, damaged, or permission-restricted PDFs may not be processable.

## Verification

```powershell
uv build
uv run python -m unittest discover -s tests
uv run create_test_pdf.py
uv run pdf-watermark --text "Confidential" test.pdf
```

The unit test checks that the output page's Noto Sans TC font resource contains an embedded `/FontFile2`. The build should create both a wheel and a source distribution. The functional check should produce `test_wm.pdf` while preserving its three different page sizes.
