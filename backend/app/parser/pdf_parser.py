"""
pdf_parser.py

Job of this file: take a PDF file and turn it into plain text.
That's it. It does NOT touch the database, the AI, or the API.
This "one file, one job" rule makes the codebase easy to debug and explain.

We use PyMuPDF (imported as 'fitz') because it's fast, has no external
system dependencies (unlike some PDF libraries that need poppler installed),
and handles most resume PDF layouts well.
"""

import fitz  # this is the PyMuPDF library


def extract_text_from_pdf(file_path: str) -> str:
    """
    Opens a PDF file and pulls out all the readable text.

    Args:
        file_path: full path to the PDF file saved on disk
                    e.g. "data/uploads/john_resume.pdf"

    Returns:
        A single string containing all text from every page,
        with pages separated by a newline for readability.
    """
    extracted_text = ""

    # "with" automatically closes the file when we're done, even if an error happens
    with fitz.open(file_path) as pdf_document:
        for page in pdf_document:
            # get_text() pulls plain text out of the page, ignoring images/graphics
            extracted_text += page.get_text()
            extracted_text += "\n"

    # Basic cleanup: PDFs often add extra blank lines and spaces
    cleaned_text = clean_text(extracted_text)

    return cleaned_text


def clean_text(raw_text: str) -> str:
    """
    Removes extra blank lines and trailing whitespace so the text we
    store in the vector database is compact and easier to embed.
    """
    lines = raw_text.split("\n")

    # Keep only lines that have actual content after trimming spaces
    non_empty_lines = [line.strip() for line in lines if line.strip() != ""]

    return "\n".join(non_empty_lines)
