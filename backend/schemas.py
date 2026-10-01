from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "dates"
    )
    @classmethod
    def validate_fields(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value


class DocumentResponse(BaseModel):
    success: bool
    document_type: str
    content: str
    mode: str
    message: str