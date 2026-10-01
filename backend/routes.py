from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import (
    DocumentRequest,
    DocumentResponse
)
from utils.config import get_settings


router = APIRouter()

settings = get_settings()

generator = GeminiDocumentGenerator(settings)


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(request: DocumentRequest):

    try:

        generated_content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            content=generated_content,
            mode=(
                "demo"
                if settings.demo_mode
                else "gemini"
            ),
            message="Document generated successfully."
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {error}"
        )