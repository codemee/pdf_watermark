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
5. `page.merge_page()` overlays the watermark page, and the result is added to `PdfWriter`.
6. After all pages are processed, the result is written as `<original-name>_wm.pdf`.

The watermark page uses `io.BytesIO`, so the merge does not require temporary PDF files.

## Watermark layout

- Font size is one fifth of the shorter page dimension: `min(width, height) / 5`.
- The canvas origin is translated to the page center and then rotated 45 degrees.
- `drawCentredString()` centers the text along the rotated horizontal axis.
- The fill is black at 15% opacity.
- A separate watermark is generated for every page, allowing A4, Letter, A3, and other sizes in one document.

## Font handling

ASCII-only text uses the built-in `Helvetica-Bold` font. Text containing any non-ASCII character triggers registration of ReportLab's `STSong-Light` CID font. The registration state is cached to avoid repeated work across pages.

`STSong-Light` is primarily intended for Chinese content and does not cover every Unicode character. Configurable embedded fonts would be needed for broad multilingual support.

## Output and error behavior

- Without an explicit output path, the result is placed next to the input with an `_wm` suffix.
- The public Python API, `add_watermark()`, accepts `output_path` for a custom destination.
- The CLI processes multiple files sequentially. A read, merge, or write exception stops execution and is displayed by the shell.
- The core function does not modify the source file.

## Known limitations

- The CLI does not yet expose output path, angle, opacity, color, or font options.
- Layout uses the page `mediabox`; unusual `cropbox` or page rotation settings may require additional handling.
- Encrypted, damaged, or permission-restricted PDFs may not be processable.

## Verification

```powershell
uv build
uv run create_test_pdf.py
uv run pdf-watermark --text "Confidential" test.pdf
```

The build should create both a wheel and a source distribution. The functional check should produce `test_wm.pdf` while preserving its three different page sizes.
