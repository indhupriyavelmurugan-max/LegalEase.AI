from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_generate_document():

    response = client.post(
        "/generate",
        json={
            "document_type":
                "Non-Disclosure Agreement",

            "parties":
                "Jane Doe (Disclosing Party), "
                "TechNova Inc. (Receiving Party)",

            "terms":
                "Confidentiality for 2 years;"
                "Return materials on request",

            "dates":
                "2026-09-29"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["success"] is True


    assert (
        "NON-DISCLOSURE AGREEMENT"
        in data["content"]
    )