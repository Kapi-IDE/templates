#!/usr/bin/env python3
"""Flask API for the Legal Analysis blueprint."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any, Dict

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from agents import (
    CaseAnalysisAgent,
    DocumentReviewAgent,
    LegalResearchAgent,
    PrecedentMiningAgent,
    PrivilegedChatAgent,
)
from database.chromadb_legal_manager import LegalKnowledgeStore
from database.sqlite_legal_manager import LegalDataManager
from utils.legal_ethics import LegalEthicsComplianceManager
from utils.legal_security import AttorneyClientPrivilegeManager

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
CORS(
    app,
    supports_credentials=True,
    origins=[origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin],
)

USE_STUBS = os.getenv("LEGAL_BLUEPRINT_UNIT_TEST", "false").lower() == "true"

if USE_STUBS:
    class _StubKnowledgeStore:
        def health_check(self) -> bool:
            return True

        def search_case_law(self, query: str, jurisdiction: str = None, limit: int = 10):  # noqa: D401 - test stub
            return [
                {
                    "case_name": "Doe v. State",
                    "citation": "123 F.3d 456",
                    "jurisdiction": jurisdiction or "federal",
                    "summary": "Sample case law summary",
                }
            ]

        def search_statutes(self, query: str, jurisdiction: str = None, limit: int = 10):
            return [
                {
                    "title": "Sample Statute",
                    "citation": "42 U.S.C. § 1983",
                    "jurisdiction": jurisdiction or "federal",
                    "summary": "Civil rights statute",
                }
            ]

        def search_precedents(self, query: str, jurisdiction: str = None, limit: int = 15):
            return [
                {
                    "legal_principle": "Precedent principle",
                    "jurisdiction": jurisdiction or "federal",
                    "citation": "456 F. Supp. 789",
                }
            ]

        def search_contract_templates(self, query: str, contract_type: str = None, limit: int = 5):
            return [
                {
                    "template_name": "NDA Template",
                    "contract_type": contract_type or "nda",
                    "summary": "Standard NDA clauses",
                }
            ]

        def search_cases_by_issue(self, legal_issue: str, jurisdiction: str, limit: int = 10):
            return [
                {
                    "case_name": "Smith v. Example",
                    "jurisdiction": jurisdiction,
                    "summary": f"Issue related to {legal_issue}",
                }
            ]

        def search_citation_network(self, cases: list, limit: int = 10):
            return []

        def search_legal_authorities(self, issue: str, jurisdiction: str):
            return {"cases": [], "statutes": []}

        def search_statutes_by_keyword(self, *args, **kwargs):  # pragma: no cover - compatibility shim
            return self.search_statutes(*args, **kwargs)

        def health_check_vectors(self) -> bool:  # pragma: no cover
            return True

    class _StubLegalDB:
        def __init__(self):
            self.cases: Dict[str, Dict[str, Any]] = {}

        def health_check(self) -> bool:
            return True

        def get_database_stats(self) -> Dict[str, int]:
            return {"legal_cases": len(self.cases)}

        def store_legal_research(self, *args, **kwargs):  # pragma: no cover - noop for stubs
            return True

        def store_document_review(self, *args, **kwargs):  # pragma: no cover - noop
            return True

        def store_case_analysis(self, *args, **kwargs):  # pragma: no cover - noop
            return True

        def store_precedent_research(self, *args, **kwargs):  # pragma: no cover - noop
            return True

        def store_privileged_communication(self, *args, **kwargs):
            return "comm-stub"

        def get_ethics_audit_summary(self, attorney_id: str = None, days: int = 30):
            return {"attorneyId": attorney_id, "compliance_score": 95, "periodDays": days}

        def list_legal_cases(self, attorney_id: str = None, client_id: str = None, limit: int = 50):
            results = list(self.cases.values())
            if attorney_id:
                results = [c for c in results if c.get("attorney_id") == attorney_id]
            if client_id:
                results = [c for c in results if c.get("client_id") == client_id]
            return results[:limit]

        def create_legal_case(self, payload: Dict[str, Any]):
            case_id = payload.get("case_id") or f"case-{len(self.cases)+1}"
            payload = {**payload, "case_id": case_id}
            self.cases[case_id] = payload
            return payload

        def update_legal_case(self, case_id: str, updates: Dict[str, Any]):
            current = self.cases.get(case_id, {"case_id": case_id})
            current.update(updates)
            self.cases[case_id] = current
            return current

        def get_legal_case(self, case_id: str):
            return self.cases.get(case_id)

    class _StubResearchAgent:
        def __init__(self, db: _StubLegalDB):
            self.db = db

        def run_research(self, question: str, attorney_id: str, client_id: str = None, jurisdiction: str = None, limit: int = 10):
            packet = {
                "question": question,
                "analysis": "Sample legal research memo",
                "authorities": [
                    {"type": "case_law", "title": "Doe v. State", "jurisdiction": jurisdiction}
                ],
                "structured": {
                    "legal_issues": [question],
                    "case_citations": ["123 F.3d 456"],
                },
            }
            self.db.store_legal_research(attorney_id, client_id, question, packet, jurisdiction or "general")
            return packet

    class _StubDocumentAgent:
        def __init__(self, db: _StubLegalDB):
            self.db = db

        def analyze_document(self, document_text: str, document_type: str, attorney_id: str, client_id: str = None, case_id: str = None):
            result = {
                "analysis": f"Stub analysis for {document_type}",
                "structured": {"legal_issues": ["confidentiality"]},
                "risks": [{"description": "Stub risk", "severity": "low", "mitigation": "Review"}],
                "relatedTemplates": [],
            }
            self.db.store_document_review(attorney_id, client_id, document_text, result)
            return result

    class _StubCaseAgent:
        def __init__(self, db: _StubLegalDB):
            self.db = db

        def list_cases(self, attorney_id: str = None, client_id: str = None):
            return self.db.list_legal_cases(attorney_id=attorney_id, client_id=client_id)

        def create_case(self, payload: Dict[str, Any]):
            return self.db.create_legal_case(payload)

        def update_case(self, case_id: str, updates: Dict[str, Any]):
            return self.db.update_legal_case(case_id, updates)

        def analyze_case(self, case_overview: str, legal_issues: list, attorney_id: str, client_id: str = None, case_id: str = None, jurisdiction: str = None):
            result = {
                "analysis": "Stub case analysis",
                "structured": {"legal_issues": legal_issues},
                "similarCases": [],
            }
            self.db.store_case_analysis(attorney_id, client_id, case_overview, result)
            return result

    class _StubPrecedentAgent:
        def __init__(self, db: _StubLegalDB):
            self.db = db

        def search_precedents(self, legal_issue: str, attorney_id: str, client_id: str = None, jurisdiction: str = None):
            packet = {
                "issue": legal_issue,
                "precedents": [
                    {"legal_principle": "Stub precedent", "jurisdiction": jurisdiction},
                ],
                "citationNetwork": [],
                "authoritySummary": {"cases": []},
            }
            self.db.store_precedent_research(attorney_id, client_id, legal_issue, packet, jurisdiction or "general")
            return packet

    class _StubPrivilegedChatAgent:
        def __init__(self, privilege_mgr: AttorneyClientPrivilegeManager):
            self.privilege_mgr = privilege_mgr

        def start_session(self, attorney_id: str, client_id: str = None, session_context: Dict[str, Any] = None):
            return self.privilege_mgr.create_secure_session(attorney_id, client_id, session_context)

        def handle_message(self, message: str, session_id: str, session_token: str, attorney_id: str, client_id: str = None, case_id: str = None):
            verification = self.privilege_mgr.verify_privileged_access(session_id, session_token, attorney_id, client_id)
            if not verification.get("authorized"):
                return {"authorized": False, "error": verification.get("reason", "unauthorized")}
            return {
                "authorized": True,
                "response": f"Stub response to: {message}",
                "structured": {"legal_issues": ["stub"]},
                "communicationId": "comm-stub",
                "ethics": {"compliance_status": "compliant"},
            }

# ---------------------------------------------------------------------------
# System component initialisation
# ---------------------------------------------------------------------------
try:
    privilege_manager = AttorneyClientPrivilegeManager()
    ethics_manager = LegalEthicsComplianceManager()

    if USE_STUBS:
        knowledge_store = _StubKnowledgeStore()
        legal_db = _StubLegalDB()
        research_agent = _StubResearchAgent(legal_db)
        document_agent = _StubDocumentAgent(legal_db)
        case_agent = _StubCaseAgent(legal_db)
        precedent_agent = _StubPrecedentAgent(legal_db)
        privileged_chat_agent = _StubPrivilegedChatAgent(privilege_manager)
        logger.info("Legal Analysis backend initialised in stub mode for tests")
    else:
        knowledge_store = LegalKnowledgeStore(os.getenv("CHROMADB_PATH", "./legal_chroma_db"))
        legal_db = LegalDataManager(os.getenv("SQLITE_DB_PATH", "./legal_data.db"))
        research_agent = LegalResearchAgent(knowledge_store, legal_db, ethics_manager)
        document_agent = DocumentReviewAgent(knowledge_store, legal_db, ethics_manager)
        case_agent = CaseAnalysisAgent(knowledge_store, legal_db, ethics_manager)
        precedent_agent = PrecedentMiningAgent(knowledge_store, legal_db, ethics_manager)
        privileged_chat_agent = PrivilegedChatAgent(
            knowledge_store, legal_db, privilege_manager, ethics_manager
        )
        logger.info("Legal Analysis backend initialised successfully")
except Exception as exc:  # pragma: no cover - fail fast during boot
    logger.exception("Failed to initialise Legal Analysis backend: %s", exc)
    raise


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _json_error(message: str, status: int = 400):
    return jsonify({"error": message}), status


def _require_fields(payload: Dict[str, Any], *fields: str):
    missing = [field for field in fields if not payload.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------
@app.route("/api/health", methods=["GET"])
def health_check():
    try:
        knowledge_ok = knowledge_store.health_check()
        database_ok = legal_db.health_check()
        return (
            jsonify(
                {
                    "status": "healthy" if (knowledge_ok and database_ok) else "degraded",
                    "timestamp": datetime.utcnow().isoformat(),
                    "components": {
                        "knowledgeStore": knowledge_ok,
                        "database": database_ok,
                    },
                    "metrics": {
                        "database": legal_db.get_database_stats(),
                    },
                }
            ),
            200,
        )
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Health check failed: %s", exc)
        return _json_error("Health check failed", 500)


@app.route("/api/research", methods=["POST"])
def run_research():
    try:
        payload = request.get_json(force=True)
        _require_fields(payload, "question", "attorneyId")

        packet = research_agent.run_research(
            payload["question"],
            attorney_id=payload["attorneyId"],
            client_id=payload.get("clientId"),
            jurisdiction=payload.get("jurisdiction"),
            limit=int(payload.get("limit", 10)),
        )
        return jsonify(packet), 200
    except ValueError as err:
        return _json_error(str(err), 400)
    except Exception as exc:
        logger.exception("Research endpoint failed: %s", exc)
        return _json_error("Failed to execute legal research", 500)


@app.route("/api/analyze-document", methods=["POST"])
def analyze_document():
    try:
        payload = request.get_json(force=True)
        _require_fields(payload, "documentText", "documentType", "attorneyId")

        result = document_agent.analyze_document(
            payload["documentText"],
            document_type=payload["documentType"],
            attorney_id=payload["attorneyId"],
            client_id=payload.get("clientId"),
            case_id=payload.get("caseId"),
        )
        return jsonify(result), 200
    except ValueError as err:
        return _json_error(str(err), 400)
    except Exception as exc:
        logger.exception("Document analysis failed: %s", exc)
        return _json_error("Failed to analyse document", 500)


@app.route("/api/cases", methods=["GET"])
def list_cases():
    try:
        cases = case_agent.list_cases(
            attorney_id=request.args.get("attorneyId"),
            client_id=request.args.get("clientId"),
        )
        return jsonify({"cases": cases}), 200
    except Exception as exc:
        logger.exception("Listing cases failed: %s", exc)
        return _json_error("Failed to list cases", 500)


@app.route("/api/cases", methods=["POST"])
def create_case():
    try:
        payload = request.get_json(force=True)
        _require_fields(payload, "attorneyId", "caseTitle")
        payload.setdefault("case_status", "active")
        payload.setdefault("case_type", "litigation")
        case_record = case_agent.create_case(
            {
                "case_id": payload.get("caseId"),
                "attorney_id": payload["attorneyId"],
                "client_id": payload.get("clientId"),
                "case_number": payload.get("caseNumber"),
                "case_title": payload.get("caseTitle"),
                "case_type": payload.get("caseType"),
                "jurisdiction": payload.get("jurisdiction"),
                "court_name": payload.get("courtName"),
                "case_status": payload.get("case_status"),
                "filed_date": payload.get("filedDate"),
                "statute_of_limitations": payload.get("statuteOfLimitations"),
                "case_summary": payload.get("caseSummary"),
                "practice_area": payload.get("practiceArea"),
                "opposing_party": payload.get("opposingParty"),
                "opposing_counsel": payload.get("opposingCounsel"),
                "estimated_value": payload.get("estimatedValue"),
                "priority_level": payload.get("priorityLevel"),
            }
        )
        return jsonify(case_record), 201
    except ValueError as err:
        return _json_error(str(err), 400)
    except Exception as exc:
        logger.exception("Create case failed: %s", exc)
        return _json_error("Failed to create case", 500)


@app.route("/api/cases/<case_id>", methods=["PUT"])
def update_case(case_id: str):
    try:
        payload = request.get_json(force=True)
        if not payload:
            return _json_error("No updates supplied", 400)
        record = case_agent.update_case(case_id, payload)
        return jsonify(record), 200
    except Exception as exc:
        logger.exception("Update case failed: %s", exc)
        return _json_error("Failed to update case", 500)


@app.route("/api/cases/<case_id>/analysis", methods=["POST"])
def analyse_case(case_id: str):
    try:
        payload = request.get_json(force=True)
        _require_fields(payload, "caseOverview", "legalIssues", "attorneyId")
        result = case_agent.analyze_case(
            payload["caseOverview"],
            legal_issues=payload.get("legalIssues", []),
            attorney_id=payload["attorneyId"],
            client_id=payload.get("clientId"),
            case_id=case_id,
            jurisdiction=payload.get("jurisdiction"),
        )
        return jsonify(result), 200
    except ValueError as err:
        return _json_error(str(err), 400)
    except Exception as exc:
        logger.exception("Case analysis failed: %s", exc)
        return _json_error("Failed to analyse case", 500)


@app.route("/api/precedents/search", methods=["POST"])
def search_precedents():
    try:
        payload = request.get_json(force=True)
        _require_fields(payload, "legalIssue", "attorneyId")
        packet = precedent_agent.search_precedents(
            payload["legalIssue"],
            attorney_id=payload["attorneyId"],
            client_id=payload.get("clientId"),
            jurisdiction=payload.get("jurisdiction"),
        )
        return jsonify(packet), 200
    except ValueError as err:
        return _json_error(str(err), 400)
    except Exception as exc:
        logger.exception("Precedent search failed: %s", exc)
        return _json_error("Failed to search precedents", 500)


@app.route("/api/privileged-chat/session", methods=["POST"])
def start_privileged_session():
    try:
        payload = request.get_json(force=True)
        _require_fields(payload, "attorneyId")
        session = privileged_chat_agent.start_session(
            attorney_id=payload["attorneyId"],
            client_id=payload.get("clientId"),
            session_context=payload.get("context"),
        )
        return jsonify(session), 201
    except ValueError as err:
        return _json_error(str(err), 400)
    except Exception as exc:
        logger.exception("Start privileged session failed: %s", exc)
        return _json_error("Failed to start privileged session", 500)


@app.route("/api/privileged-chat", methods=["POST"])
def privileged_chat():
    try:
        payload = request.get_json(force=True)
        _require_fields(payload, "sessionId", "sessionToken", "attorneyId", "message")
        response = privileged_chat_agent.handle_message(
            payload["message"],
            session_id=payload["sessionId"],
            session_token=payload["sessionToken"],
            attorney_id=payload["attorneyId"],
            client_id=payload.get("clientId"),
            case_id=payload.get("caseId"),
        )
        status = 200 if response.get("authorized") else 403
        return jsonify(response), status
    except ValueError as err:
        return _json_error(str(err), 400)
    except Exception as exc:
        logger.exception("Privileged chat failed: %s", exc)
        return _json_error("Failed to process privileged communication", 500)


@app.route("/api/ethics/audit", methods=["GET"])
def ethics_audit():
    try:
        attorney_id = request.args.get("attorneyId")
        summary = legal_db.get_ethics_audit_summary(attorney_id=attorney_id)
        return jsonify(summary), 200
    except Exception as exc:
        logger.exception("Ethics audit endpoint failed: %s", exc)
        return _json_error("Failed to retrieve ethics audit", 500)


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    app.run(host=os.getenv("FLASK_HOST", "0.0.0.0"), port=int(os.getenv("FLASK_PORT", 5000)), debug=True)
