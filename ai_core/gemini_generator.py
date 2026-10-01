from google import genai
from google.genai import types

from utils.config import Settings
from utils.text_utils import sanitize_text


class GeminiDocumentGenerator:
    """
    Generates legal-information drafts using Gemini.

    If GEMINI_API_KEY is not configured,
    the application automatically uses demo mode.
    """

    def __init__(self, settings: Settings):

        self.settings = settings

        self.client = None

        if not settings.demo_mode:

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    def create_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        prompt = f"""
You are LegalEase, an AI assistant for drafting
legal-information documents.

Create a professional draft based only on
the information provided by the user.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{dates}

TERMS AND CONDITIONS:
{terms}

IMPORTANT REQUIREMENTS:

1. Use clear formal language.

2. Include a document title.

3. Include suitable sections for the
   requested document type.

4. Use the supplied party names and terms.

5. Do not invent personal information.

6. If important information is missing,
   use placeholders such as:

   [INSERT ADDRESS]

   [INSERT PAYMENT AMOUNT]

   [INSERT JURISDICTION]

7. Do not invent laws, case numbers,
   registration numbers or legal authorities.

8. Do not claim that the generated
   document is guaranteed legally valid.

9. End with a short Review Notice.

10. Return plain text only.

Do not use Markdown code fences.
"""

        return prompt.strip()

    def create_demo_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        term_list = [
            item.strip()
            for item in terms.split(";")
            if item.strip()
        ]

        bullet_terms = "\n".join(
            f"- {term}"
            for term in term_list
        )

        document = f"""
{document_type.upper()}

Effective Date: {dates}

PARTIES

{parties}


PURPOSE

This document is a draft prepared from
the information supplied by the user.


TERMS AND CONDITIONS

{bullet_terms}


GENERAL PROVISIONS

1. The parties should confirm that all
names, dates, addresses, amounts and
obligations are accurate.

2. Jurisdiction-specific provisions should
be added after appropriate legal review.

3. Any changes should be agreed upon by
the relevant parties and recorded in
writing where appropriate.


SIGNATURES

Party 1:

Signature: ______________________________

Name: __________________________________

Date: __________________________________


Party 2:

Signature: ______________________________

Name: __________________________________

Date: __________________________________


REVIEW NOTICE

This is a generated draft for informational
and drafting purposes.

It is not legal advice and should be
reviewed by a qualified legal professional
before important use.
"""

        return sanitize_text(document)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        # Local testing mode
        if self.settings.demo_mode:

            return self.create_demo_document(
                document_type,
                parties,
                terms,
                dates
            )

        # Gemini generation
        prompt = self.create_prompt(
            document_type,
            parties,
            terms,
            dates
        )

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.25,
                max_output_tokens=8000
            )
        )

        generated_text = getattr(
            response,
            "text",
            None
        )

        if not generated_text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return sanitize_text(
            generated_text
        )