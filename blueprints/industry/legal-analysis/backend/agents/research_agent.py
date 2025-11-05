#!/usr/bin/env python3
"""Legal research orchestration agent."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base_legal_agent import BaseLegalAgent


class LegalResearchAgent(BaseLegalAgent):
    """Coordinates legal research across Chroma and the structured DB."""

    def __init__(self, knowledge_store: Any, legal_db: Any, ethics_manager: Any):
        super().__init__(knowledge_store, legal_db, "legal_research")
        self.ethics_manager = ethics_manager

    def run_research(
        self,
        question: str,
        *,
        attorney_id: str,
        client_id: Optional[str] = None,
        jurisdiction: Optional[str] = None,
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Execute a research workflow and persist the privileged result."""
        prompt = self._create_legal_system_prompt(
            """
            You are the research lead on a multi-agent legal team.
            Provide a concise research memorandum that includes:
            - Framing of the legal issues
            - Key authorities with citations
            - Strategic considerations and open questions to confirm with the attorney
            - Ethics or conflict concerns we should flag
            Keep tone professional and cite authorities inline.
            """
        )

        authorities = self._search_authorities(question, jurisdiction, limit)
        analysis_text = self._generate_legal_response(
            prompt + f"\n\nPRIMARY QUESTION: {question}\n",
            case_context={"jurisdiction": jurisdiction, "authorities": authorities[:5]},
            attorney_id=attorney_id,
            client_id=client_id,
        )

        structured = self._extract_legal_structured_data(analysis_text, "legal_research")
        research_packet = {
            "question": question,
            "jurisdiction": jurisdiction,
            "analysis": analysis_text,
            "structured": structured,
            "authorities": authorities,
        }

        # Persist privileged output for auditing and downstream agents
        self.legal_db.store_legal_research(
            attorney_id,
            client_id,
            question,
            research_packet,
            jurisdiction or "general",
        )

        # Run lightweight ethics check (AI disclosure compliance)
        compliance_entry = self.ethics_manager.check_ai_disclosure_compliance(
            attorney_id,
            client_id or "internal-matter",
            {
                "tool": "legal_research_agent",
                "ai_assistance_used": True,
                "disclosure_provided": bool(client_id),
                "question": question,
            },
        )
        research_packet["ethics"] = compliance_entry

        return research_packet

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _search_authorities(
        self, question: str, jurisdiction: Optional[str], limit: int
    ) -> List[Dict[str, Any]]:
        """Search case law, statutes, and precedents to power responses."""
        case_law = self.knowledge_store.search_case_law(question, jurisdiction, limit=limit)
        statutes = self.knowledge_store.search_statutes(question, jurisdiction, limit=max(5, limit // 2))
        precedents = self.knowledge_store.search_precedents(question, jurisdiction, limit=max(5, limit // 2))

        ranked: List[Dict[str, Any]] = []
        ranked.extend(self._decorate_results(case_law, "case_law"))
        ranked.extend(self._decorate_results(statutes, "statute"))
        ranked.extend(self._decorate_results(precedents, "precedent"))
        return ranked

    def _decorate_results(self, items: List[Dict[str, Any]], authority_type: str) -> List[Dict[str, Any]]:
        """Attach consistent metadata to authority search results."""
        decorated: List[Dict[str, Any]] = []
        for item in items[:10]:
            decorated.append(
                {
                    "type": authority_type,
                    "title": item.get("case_name")
                    or item.get("title")
                    or item.get("legal_principle")
                    or "Authority",
                    "citation": item.get("citation"),
                    "summary": item.get("summary") or item.get("holding") or item.get("statute_text"),
                    "jurisdiction": item.get("jurisdiction"),
                    "raw": item,
                }
            )
        return decorated


__all__ = ["LegalResearchAgent"]
