"""Command-line interface for pdf-watermark."""

import argparse

from . import WATERMARK_TEXT, add_watermark


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pdf-watermark",
        description="Add a diagonal watermark to one or more PDF files.",
    )
    parser.add_argument("files", nargs="+", metavar="FILE", help="Input PDF file(s)")
    parser.add_argument(
        "--text",
        default=WATERMARK_TEXT,
        metavar="TEXT",
        help=f"Watermark text (default: {WATERMARK_TEXT!r})",
    )
    args = parser.parse_args()

    for path in args.files:
        output_path = add_watermark(path, text=args.text)
        print(f"Saved: {output_path}")
