# pdf-watermark

Add centered, semi-transparent diagonal text watermarks to every page of a PDF.

English | [繁體中文](https://github.com/codemee/pdf_watermark/blob/main/README.md)

## Features

- Process one or more PDF files in a single command.
- Generate each watermark using the original page dimensions.
- Customize the watermark text, including Chinese text.
- Automatically scale down long text to fit the page's available diagonal width.
- Embed a Noto Sans TC font subset instead of relying on fonts installed on the viewer.
- Preserve the original files.

## Requirements

- Windows, macOS, or Linux
- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

## Install from PyPI (recommended)

This project is published on PyPI as [`pdfcwm`](https://pypi.org/project/pdfcwm/), while the installed command remains `pdf-watermark`. Without a version specifier, uv installs the latest release:

```console
uv tool install pdfcwm
pdf-watermark input.pdf
```

Run without installing:

```console
uvx --from pdfcwm pdf-watermark input.pdf
```

Upgrade to the latest release:

```console
uv tool upgrade pdfcwm
```

### Install a specific version (optional)

For example, to install `0.0.5`:

```console
uv tool install pdfcwm@0.0.5
```

## Run the latest release from a ZIP without Git

This repository is public. The URL below follows the [GitHub Latest Release](https://github.com/codemee/pdf_watermark/releases/latest) automatically and does not require Git.

Windows PowerShell:

```powershell
Invoke-WebRequest `
  https://github.com/codemee/pdf_watermark/releases/latest/download/pdf-watermark-source.zip `
  -OutFile pdf-watermark-source.zip
Expand-Archive pdf-watermark-source.zip -DestinationPath pdf-watermark-source
Set-Location pdf-watermark-source\pdf_watermark
```

macOS or Linux:

```sh
curl -L https://github.com/codemee/pdf_watermark/releases/latest/download/pdf-watermark-source.zip \
  -o pdf-watermark-source.zip
unzip pdf-watermark-source.zip -d pdf-watermark-source
cd pdf-watermark-source/pdf_watermark
```

On any platform, you can instead select **Code > Download ZIP** on GitHub, extract the archive, and enter the project directory.

Run the tool without installing it:

```console
uvx --from . pdf-watermark input.pdf
uvx --from . pdf-watermark --text "Top Secret" input.pdf
```

To install the `pdf-watermark` command persistently:

```console
uv tool install .
pdf-watermark input.pdf
```

You can also install directly from the ZIP URL without downloading or extracting it manually:

```console
uv tool install "pdfcwm @ https://github.com/codemee/pdf_watermark/releases/latest/download/pdf-watermark-source.zip"
pdf-watermark input.pdf
```

None of these methods require Git. uv will still download Python and Python package dependencies over HTTPS.

To upgrade an existing installation to the latest release using the same URL:

```console
uv tool install --force "pdfcwm @ https://github.com/codemee/pdf_watermark/releases/latest/download/pdf-watermark-source.zip"
```

## Install the latest default-branch revision with Git

```console
uv tool install git+https://github.com/codemee/pdf_watermark.git
pdf-watermark input.pdf
```

This method installs the latest default-branch revision, which may include changes that have not been formally released. To refresh an existing installation:

```console
uv tool install --force git+https://github.com/codemee/pdf_watermark.git
```

This installation method requires Git. To refresh an installation made from the ZIP URL instead, rerun its `uv tool install` command with `--force`.

## Usage

Use the default `Confidential` text:

```console
pdf-watermark input.pdf
```

Set custom text:

```console
pdf-watermark --text "Top Secret" input.pdf
```

Process multiple files:

```console
pdf-watermark file1.pdf file2.pdf
```

Each output is written next to its input as `<original-name>_wm.pdf`. The input file is not overwritten.

## Development and verification

```console
uv sync
uv run create_test_pdf.py
uv run pdf-watermark --text "Confidential" test.pdf
```

`test.pdf` contains A4, Letter, and A3 pages. Inspect the generated `test_wm.pdf` to verify the result visually.

## Implementation details

See the [implementation guide](https://github.com/codemee/pdf_watermark/blob/main/docs/implementation.en.md).

## Font license

The bundled Noto Sans TC font is provided by Google Fonts under the SIL Open Font License 1.1. The full license is in `src/pdf_watermark/fonts/OFL.txt`.
