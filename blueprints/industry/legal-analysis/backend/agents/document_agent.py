#!/usr/bin/env python3
"""Document analysis agent built on shared legal components."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base_legal_agent import BaseLegalAgent


class DocumentReviewAgent(BaseLegalAgent):
    """Reviews legal documents for risk, obligations, and compliance."""

    def __init__(self, knowledge_store: Any, legal_db: Any, ethics_manager: Any):
        super().__init__(knowledge_store, legal_db, "document_review")
        self.ethics_manager = ethics_manager

    def analyze_document(
        self,
        document_text: str,
        *,
        document_type: str,
        attorney_id: str,
        client_id: Optional[str] = None,
        case_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run the review workflow and persist privileged output."""
        prompt = self._create_legal_system_prompt(
            """
            You are a senior associate reviewing a legal document. Identify:
            - Key clauses and their obligations
            - Potential risks or red flags
            - Required follow-up actions or missing terms
            Keep the assessment practical and reference clause headings if available.
            """
        )
        analysis_text = self._generate_legal_response(
            prompt + f"\n\nDOCUMENT TYPE: {document_type}\nDOCUMENT TEXT:\n{document_text[:2000]}",
            case_context={"document_type": document_type, "case_id": case_id},
            attorney_id=attorney_id,
            client_id=client_id,
        )

        structured = self._extract_legal_structured_data(analysis_text, "document_review")
        risks = self._infer_risks(structured)
        related_templates = self.knowledge_store.search_contract_templates(
            document_text, document_type=document_type, limit=5
        )

        review_result = {
            "analysis": analysis_text,
            "structured": structured,
            "risks": risks,
            "relatedTemplates": related_templates,
        }

        self.legal_db.store_document_review(attorney_id, client_id, document_text, review_result)
        return review_result

    # ------------------------------------------------------------------
    def _infer_risks(self, structured_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Derive a simple risk matrix from structured AI output."""
        risks = []
        recommendations = structured_output.get("recommendations") or []
        for rec in recommendations[:5]:
            risks.append(
                {
                    "description": rec,
                    "severity": "high" if "terminate" in rec.lower() else "medium",
                    "mitigation": "Review with client" if "client" in rec.lower() else "Add protective clause",
                }
            )
        if not risks:
            risks.append(
                {
                    "description": "No critical risks detected in automated review",
                    "severity": "low",
                    "mitigation": "Attorney should confirm before relying",
                }
            )
        return risks


__all__ = ["DocumentReviewAgent"]
