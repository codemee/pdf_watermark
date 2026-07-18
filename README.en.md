# pdf-watermark

Add centered, semi-transparent diagonal text watermarks to every page of a PDF.

English | [繁體中文](README.md)

## Features

- Process one or more PDF files in a single command.
- Generate each watermark using the original page dimensions.
- Customize the watermark text, including Chinese text.
- Embed a Noto Sans TC font subset instead of relying on fonts installed on the viewer.
- Preserve the original files.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)

## Run from a local checkout

No installation is required when running from the project directory:

```powershell
uvx . input.pdf
uvx . --text "Top Secret" input.pdf
```

## Install the latest version

```powershell
uv tool install git+https://github.com/codemee/pdf_watermark.git@latest
pdf-watermark input.pdf
```

The floating `latest` tag is updated for each release. To refresh an existing installation:

```powershell
uv tool install --force git+https://github.com/codemee/pdf_watermark.git@latest
```

When this repository is private, the installer needs GitHub access and working Git credentials.

## Usage

Use the default `Confidential` text:

```powershell
pdf-watermark input.pdf
```

Set custom text:

```powershell
pdf-watermark --text "Top Secret" input.pdf
```

Process multiple files:

```powershell
pdf-watermark file1.pdf file2.pdf
```

Each output is written next to its input as `<original-name>_wm.pdf`. The input file is not overwritten.

## Development and verification

```powershell
uv sync
uv run create_test_pdf.py
uv run pdf-watermark --text "Confidential" test.pdf
```

`test.pdf` contains A4, Letter, and A3 pages. Inspect the generated `test_wm.pdf` to verify the result visually.

## Implementation details

See the [implementation guide](docs/implementation.en.md).

## Font license

The bundled Noto Sans TC font is provided by Google Fonts under the SIL Open Font License 1.1. The full license is in `src/pdf_watermark/fonts/OFL.txt`.
