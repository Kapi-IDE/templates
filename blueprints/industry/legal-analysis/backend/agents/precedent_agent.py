#!/usr/bin/env python3
"""Precedent discovery agent."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base_legal_agent import BaseLegalAgent


class PrecedentMiningAgent(BaseLegalAgent):
    """Discovers and analyzes legal precedents relevant to a matter."""

    def __init__(self, knowledge_store: Any, legal_db: Any, ethics_manager: Any):
        super().__init__(knowledge_store, legal_db, "precedent_mining")
        self.ethics_manager = ethics_manager

    def search_precedents(
        self,
        legal_issue: str,
        *,
        attorney_id: str,
        client_id: Optional[str] = None,
        jurisdiction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Return precedent packet enriched with citation network data."""
        precedents = self.knowledge_store.search_precedents(legal_issue, jurisdiction, limit=12)
        citation_network = self.knowledge_store.search_citation_network(precedents[:5], limit=8)
        authority_summary = self.knowledge_store.search_legal_authorities(legal_issue, jurisdiction or "general")

        packet = {
            "issue": legal_issue,
            "jurisdiction": jurisdiction,
            "precedents": precedents,
            "citationNetwork": citation_network,
            "authoritySummary": authority_summary,
        }

        self.legal_db.store_precedent_research(attorney_id, client_id, legal_issue, packet, jurisdiction or "general")
        return packet


__all__ = ["PrecedentMiningAgent"]
