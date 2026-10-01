import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv

from services.document_service import (
    format_docx,
    format_pdf,
    format_txt
)

from utils.text_utils import (
    format_html_preview
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 1.5rem;
    }

    .preview {
        background: #151922;
        color: #f2f4f8;
        border-radius: 12px;
        padding: 24px;
        max-height: 600px;
        overflow-y: auto;
        line-height: 1.65;
    }

    .notice {
        background: #fff8e1;
        border-left: 5px solid #d99b00;
        padding: 12px;
        border-radius: 6px;
        color: #4b3a00;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="notice">

    <b>Important:</b>

    LegalEase provides drafting assistance
    and legal information.

    It is not a substitute for advice from
    a qualified legal professional.

    </div>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "generated_text" not in st.session_state:

    st.session_state.generated_text = ""


if "mode" not in st.session_state:

    st.session_state.mode = ""


# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------

st.subheader(
    "Document Details"
)


column1, column2 = st.columns(2)


with column1:

    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Lease Agreement",
            "Non-Disclosure Agreement",
            "Employment Offer Letter",
            "Service Agreement",
            "Freelance Work Contract",
            "Authorization Letter",
            "Affidavit",
            "Other"
        ]
    )

    if document_type == "Other":

        document_type = st.text_input(
            "Specify document type"
        )


    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=120
    )


with column2:

    dates = st.date_input(
        "Effective Date",
        value=date.today()
    )


    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=120,
        help=(
            "Separate each clause using semicolons."
        )
    )


# -------------------------------------------------
# GENERATE BUTTON
# -------------------------------------------------

generate_button = st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
)


if generate_button:

    # Validation

    if (
        not document_type.strip()
        or not parties.strip()
        or not terms.strip()
    ):

        st.error(
            "Please fill all required fields."
        )

    else:

        payload = {

            "document_type":
                document_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                terms.strip(),

            "dates":
                dates.isoformat()
        }


        try:

            with st.spinner(
                "Generating your document..."
            ):

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=120
                )


            if response.ok:

                data = response.json()


                st.session_state.generated_text = (
                    data["content"]
                )


                st.session_state.mode = (
                    data.get(
                        "mode",
                        "unknown"
                    )
                )


                st.success(
                    "Document generated successfully "
                    f"({st.session_state.mode.upper()} mode)."
                )


            else:

                try:

                    error_message = (
                        response.json()
                        .get(
                            "detail",
                            response.text
                        )
                    )

                except Exception:

                    error_message = response.text


                st.error(
                    f"Backend error: {error_message}"
                )


        except requests.RequestException as error:

            st.error(
                "Could not connect to FastAPI backend."
            )

            st.info(
                "Start the backend using:"
            )

            st.code(
                "uvicorn backend.main:app --reload"
            )

            st.caption(
                str(error)
            )


# -------------------------------------------------
# GENERATED DOCUMENT
# -------------------------------------------------

if st.session_state.generated_text:

    st.divider()


    st.subheader(
        "Document Preview"
    )


    if st.session_state.mode == "demo":

        st.info(
            "Demo mode is active because "
            "GEMINI_API_KEY is not configured."
        )


    # Preview

    preview_html = format_html_preview(
        st.session_state.generated_text
    )


    st.markdown(
        f"""
        <div class="preview">
            {preview_html}
        </div>
        """,
        unsafe_allow_html=True
    )


    # -------------------------------------------------
    # EDIT DOCUMENT
    # -------------------------------------------------

    st.subheader(
        "Edit Document"
    )


    edited_text = st.text_area(
        "Modify the generated document "
        "before exporting.",
        value=st.session_state.generated_text,
        height=500,
        label_visibility="collapsed"
    )


    st.session_state.generated_text = (
                edited_text
    )


    # -------------------------------------------------
    # DOWNLOAD
    # -------------------------------------------------

    st.subheader(
        "Download Document"
    )


    download1, download2, download3 = (
        st.columns(3)
    )


    with download1:

        txt_file = format_txt(
            edited_text
        )


        st.download_button(
            label="⬇️ Download TXT",
            data=txt_file,
            file_name="legalese_document.txt",
            mime="text/plain",
            use_container_width=True
        )


    with download2:

        docx_file = format_docx(
            edited_text,
            document_type
        )


        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_file,
            file_name="legalese_document.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )


    with download3:

        pdf_file = format_pdf(
            edited_text,
            document_type
        )


        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_file,
            file_name="legalese_document.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()


st.caption(
    "LegalEase • FastAPI + Streamlit + Gemini"
)