from io import BytesIO

from docx import Document

from services.document_service import (
    format_docx,
    format_pdf,
    format_txt
)


def test_txt_export():

    result = format_txt(
        "TEST DOCUMENT"
    )

    assert result.startswith(
        b"TEST DOCUMENT"
    )


def test_docx_export():

    data = format_docx(
        "TEST DOCUMENT\n\nPARTIES\nJane Doe",
        "Agreement"
    )


    assert data[:2] == b"PK"


    document = Document(
        BytesIO(data)
    )


    assert (
        "LegalEase"
        in document.paragraphs[0].text
    )


def test_pdf_export():

    data = format_pdf(
        "TEST DOCUMENT\n\nPARTIES\nJane Doe",
        "Agreement"
    )


    assert data.startswith(
        b"%PDF"
    )