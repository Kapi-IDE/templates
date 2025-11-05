"""Integration-style tests for the blueprint API (stub mode)."""

from __future__ import annotations

from flask.testing import FlaskClient


def test_health_endpoint(client: FlaskClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] in {"healthy", "degraded"}


def test_research_flow(client: FlaskClient):
    response = client.post(
        "/api/research",
        json={"question": "What is the standard for summary judgment?", "attorneyId": "attorney-1"},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert "analysis" in payload
    assert payload["structured"]["legal_issues"]


def test_case_crud_and_analysis(client: FlaskClient):
    create_response = client.post(
        "/api/cases",
        json={
            "caseTitle": "Acme v. Example",
            "attorneyId": "attorney-1",
            "caseType": "litigation",
            "jurisdiction": "California",
        },
    )
    assert create_response.status_code == 201
    case_payload = create_response.get_json()
    case_id = case_payload["case_id"]

    list_response = client.get("/api/cases", query_string={"attorneyId": "attorney-1"})
    assert list_response.status_code == 200
    assert any(case["case_id"] == case_id for case in list_response.get_json()["cases"])

    analysis_response = client.post(
        f"/api/cases/{case_id}/analysis",
        json={
            "caseOverview": "Breach of contract dispute over software license.",
            "legalIssues": ["breach of contract"],
            "attorneyId": "attorney-1",
            "jurisdiction": "California",
        },
    )
    assert analysis_response.status_code == 200
    assert analysis_response.get_json()["analysis"]


def test_privileged_chat_flow(client: FlaskClient):
    session_response = client.post(
        "/api/privileged-chat/session",
        json={"attorneyId": "attorney-1", "clientId": "client-1"},
    )
    assert session_response.status_code == 201
    session_payload = session_response.get_json()

    chat_response = client.post(
        "/api/privileged-chat",
        json={
            "sessionId": session_payload["session_id"],
            "sessionToken": session_payload["session_token"],
            "attorneyId": "attorney-1",
            "clientId": "client-1",
            "message": "Can you summarise our litigation risk?",
        },
    )
    assert chat_response.status_code == 200
    assert chat_response.get_json()["authorized"]


def test_missing_fields_return_400(client: FlaskClient):
    response = client.post("/api/research", json={"question": "missing attorney"})
    assert response.status_code == 400
    payload = response.get_json()
    assert "Missing required fields" in payload["error"]


def test_privileged_chat_requires_session_token(client: FlaskClient):
    response = client.post(
        "/api/privileged-chat",
        json={
            "sessionId": "fake",
            "sessionToken": "invalid",
            "attorneyId": "attorney-1",
            "message": "hello",
        },
    )
    assert response.status_code == 403
    payload = response.get_json()
    assert payload["authorized"] is False
