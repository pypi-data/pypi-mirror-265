from dataclasses import dataclass
from mimetypes import guess_type
import json
import os
import click
import fitz


@dataclass
class PdfQuality:
    is_pdf: bool | None = None
    can_open: bool | None = None
    password_protected: bool | None = None
    has_toc: bool | None = None
    size_bytes: int = -1
    size_pages: int = -1


def results(quality: PdfQuality, verbose: bool, error: Exception | None) -> str:
    """Prepares the results for the user."""
    res = quality.__dict__
    if verbose and error is not None:
        res.setdefault("error", str(error))
    return json.dumps(res, indent=4, sort_keys=True)


def is_pdf_by_binary(pdf_path: str) -> bool:
    """Checks if the file is a binary file."""
    with open(pdf_path, "rb") as f:
        return bool(f.read(4) == b"%PDF")


def is_pdf_by_mime(pdf_path: str) -> bool:
    """Checks if the file is a PDF by MIME type."""
    mime = guess_type(pdf_path)
    return mime[0] == "application/pdf"


def is_pdf(pdf_path: str) -> bool:
    """Checks if the file is a PDF."""

    # Check if binary file says it is a PDF
    try:
        valid = is_pdf_by_binary(pdf_path)
        if valid:
            return True
    except Exception:
        pass

    # Check if MIME type says it is a PDF
    if is_pdf_by_mime(pdf_path):
        return True

    return False


def get_file_size(file_path) -> int | None:
    """Returns the size of the file in bytes."""
    try:
        # Use os.stat() to get a variety of statistics about the file,
        # including its size, which is accessible via the .st_size attribute.
        return os.stat(file_path).st_size
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred while trying to get the file size: {e}")
        return None


@click.command()
@click.option("--verbose", is_flag=True, help="Prints more information.")
@click.argument("pdf_path", type=click.Path(exists=True))
def main(verbose, pdf_path):
    """Analyzes a PDF file and reports values around quality."""

    # Setup quality with default values
    quality = PdfQuality()

    # Check if file is a PDF
    if not is_pdf(pdf_path):
        quality.is_pdf = False
        click.echo(results(quality, verbose, None))
        return
    quality.is_pdf = True

    try:
        # Try to open
        doc = fitz.open(pdf_path)

        quality.can_open = True
        quality.is_pdf = doc.is_pdf
        if not quality.is_pdf:
            click.echo(results(quality, verbose, None))
            return
    except Exception as e:
        quality.can_open = False
        click.echo(results(quality, verbose, e))
        return

    # Check if the PDF is password protected
    quality.password_protected = bool(doc.is_encrypted or doc.needs_pass)

    # Size of the PDF & number of pages
    quality.size_pages = doc.page_count
    quality.size_bytes = get_file_size(pdf_path)

    # Get the TOC
    toc = doc.get_toc()
    quality.has_toc = len(toc) > 0

    # Return results
    click.echo(results(quality, verbose, None))


if __name__ == "__main__":
    main()
