#!/usr/bin/env python3
"""Case management and strategy agent."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base_legal_agent import BaseLegalAgent


class CaseAnalysisAgent(BaseLegalAgent):
    """Analyzes cases, drafts strategies, and manages matter metadata."""

    def __init__(self, knowledge_store: Any, legal_db: Any, ethics_manager: Any):
        super().__init__(knowledge_store, legal_db, "case_analysis")
        self.ethics_manager = ethics_manager

    def analyze_case(
        self,
        case_overview: str,
        *,
        legal_issues: List[str],
        attorney_id: str,
        client_id: Optional[str] = None,
        case_id: Optional[str] = None,
        jurisdiction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform a case strength assessment leveraging precedent mining."""
        prompt = self._create_legal_system_prompt(
            """
            You are leading case strategy. Provide:
            - Strength assessment (strong / moderate / weak) with rationale
            - Recommended legal theories or causes of action
            - Key precedent themes to investigate
            - Tactical next steps for the legal team
            Keep tone strategic and reference jurisdictional nuances.
            """
        )
        context = {
            "case_id": case_id,
            "issues": legal_issues,
            "jurisdiction": jurisdiction,
        }
        analysis_text = self._generate_legal_response(
            prompt + f"\n\nCASE OVERVIEW:\n{case_overview}\nISSUES: {', '.join(legal_issues)}",
            case_context=context,
            attorney_id=attorney_id,
            client_id=client_id,
        )
        structured = self._extract_legal_structured_data(analysis_text, "case_analysis")
        similar_cases = self.knowledge_store.search_cases_by_issue(
            legal_issues[0] if legal_issues else "general", jurisdiction or "general", limit=10
        )

        result = {
            "analysis": analysis_text,
            "structured": structured,
            "similarCases": similar_cases,
        }

        self.legal_db.store_case_analysis(attorney_id, client_id, case_overview, result)
        return result

    # ------------------------------------------------------------------
    # Case management helpers delegated to the data manager
    # ------------------------------------------------------------------
    def create_case(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.legal_db.create_legal_case(payload)

    def update_case(self, case_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        return self.legal_db.update_legal_case(case_id, updates)

    def list_cases(
        self, *, attorney_id: Optional[str] = None, client_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        return self.legal_db.list_legal_cases(attorney_id=attorney_id, client_id=client_id)

    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        return self.legal_db.get_legal_case(case_id)


__all__ = ["CaseAnalysisAgent"]
