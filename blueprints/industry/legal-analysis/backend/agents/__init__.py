#!/usr/bin/env python3
"""Legal AI agents exposed to the Flask service layer."""

from .base_legal_agent import BaseLegalAgent
from .research_agent import LegalResearchAgent
from .case_agent import CaseAnalysisAgent
from .document_agent import DocumentReviewAgent
from .precedent_agent import PrecedentMiningAgent
from .privileged_chat_agent import PrivilegedChatAgent

__all__ = [
    "BaseLegalAgent",
    "LegalResearchAgent",
    "CaseAnalysisAgent",
    "DocumentReviewAgent",
    "PrecedentMiningAgent",
    "PrivilegedChatAgent",
]
