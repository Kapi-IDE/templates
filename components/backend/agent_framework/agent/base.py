"""Framework-agnostic agent foundation for building AI agents across any domain."""
from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from ..llm.gemini_client import GeminiClient
from ..logging.interaction_logger import log_interaction

logger = logging.getLogger(__name__)


class AgentFoundation:
    """Provides shared behaviour for conversational AI agents across any domain.

    This base class can be extended for healthcare, finance, legal, or any other domain.
    Override BASE_PROMPT and customize methods for domain-specific behavior.
    """

    BASE_PROMPT = """
You are a professional AI assistant designed to provide accurate, helpful information.

IMPORTANT GUIDELINES:
- Provide accurate, factual information based on available data
- Be empathetic and professional in all interactions
- Ask clarifying questions to better understand user needs
- Acknowledge limitations and uncertainties
- Prioritize user safety and well-being
- Maintain ethical standards appropriate to your domain

CONTEXT:
- You are part of a multi-agent system
- Your responses may be used by other agents for decision-making
- Maintain data privacy and confidentiality
- Document all interactions for continuity and audit trails
"""

    def __init__(
        self,
        *,
        knowledge_store: Any,
        data_store: Any,
        agent_type: str,
        llm_client: Optional[GeminiClient] = None,
    ) -> None:
        """Initialize agent with required dependencies.

        Args:
            knowledge_store: Vector store or knowledge base for RAG
            data_store: Database for storing interactions and audit logs
            agent_type: Identifier for this agent type (e.g., 'triage', 'risk_analysis')
            llm_client: Optional LLM client (defaults to GeminiClient)
        """
        self.knowledge_store = knowledge_store
        self.data_store = data_store  # Renamed from patient_db for generality
        self.agent_type = agent_type
        self.llm_client = llm_client or GeminiClient()

    # ------------------------------------------------------------------
    # Prompt helpers
    # ------------------------------------------------------------------
    def build_system_prompt(self, specific_instructions: str) -> str:
        return f"{self.BASE_PROMPT}\n{specific_instructions.strip()}"

    # ------------------------------------------------------------------
    # LLM helpers
    # ------------------------------------------------------------------
    def generate_response(
        self, prompt: str, *, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate AI response with optional context.

        Args:
            prompt: The prompt to send to the LLM
            context: Optional context dictionary (user profile, session data, etc.)

        Returns:
            AI-generated response text
        """
        try:
            return self.llm_client.generate_text(prompt, context=context)
        except Exception as exc:  # pragma: no cover - fallback important
            logger.error("Failed to generate AI response: %s", exc)
            return self.fallback_response()

    def fallback_response(self) -> str:
        """Override this method for domain-specific fallback messages."""
        return (
            "I apologize, but I'm experiencing technical difficulties. "
            "Please try again or contact support if the issue persists."
        )

    def extract_structured_data(
        self,
        *,
        text: str,
        structure_type: str,
        fallback_keywords: Optional[Iterable[str]] = None,
    ) -> Dict[str, Any]:
        fallback_keywords = tuple(fallback_keywords or ())
        prompt = f"""
Extract the following information from the text and return as JSON:
Text: {text}

For {structure_type}, extract:
- symptoms: list of symptoms mentioned
- severity_indicators: list of severity markers
- questions: list of follow-up questions
- recommendations: list of recommendations
- confidence_level: confidence in assessment (1-10)

Return only valid JSON:
"""
        try:
            return self.llm_client.generate_json(prompt)
        except json.JSONDecodeError:
            logger.warning("Gemini returned invalid JSON, using manual parser")
            return self._manual_parse_response(text, fallback_keywords)
        except Exception as exc:  # pragma: no cover
            logger.error("Failed to extract structured data: %s", exc)
            return self.default_structure()

    def _manual_parse_response(
        self, text: str, fallback_keywords: Iterable[str]
    ) -> Dict[str, Any]:
        symptoms: List[str] = []
        questions: List[str] = []
        recommendations: List[str] = []
        severity_markers: List[str] = []

        lines = (line.strip() for line in text.split("\n") if line.strip())
        for line in lines:
            lowered = line.lower()
            if "?" in line:
                questions.append(line)
            elif any(word in lowered for word in ("recommend", "suggest", "should")):
                recommendations.append(line)
            elif any(word in lowered for word in fallback_keywords or ("pain", "ache", "hurt")):
                symptoms.append(line)
            elif "urgent" in lowered or "emergency" in lowered:
                severity_markers.append(line)

        return {
            "symptoms": symptoms[:5],
            "severity_indicators": severity_markers[:5],
            "questions": questions[:3],
            "recommendations": recommendations[:3],
            "confidence_level": 5,
        }

    @staticmethod
    def default_structure() -> Dict[str, Any]:
        """Override this for domain-specific default structures."""
        return {
            "extracted_items": [],
            "key_indicators": [],
            "questions": ["Can you provide more details?"],
            "recommendations": ["Please consult with a professional"],
            "confidence_level": 1,
        }

    # ------------------------------------------------------------------
    # Logging + validation helpers
    # ------------------------------------------------------------------
    def log_interaction(
        self,
        *,
        user_id: str,
        interaction_type: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        processing_time: Optional[float] = None,
    ) -> None:
        """Log agent interaction to data store.

        Args:
            user_id: Identifier for the user/client/patient
            interaction_type: Type of interaction (e.g., 'analysis', 'query')
            input_data: Input data dictionary
            output_data: Output data dictionary
            processing_time: Optional processing time in seconds
        """
        log_interaction(
            self.data_store,
            agent_type=self.agent_type,
            user_id=user_id,
            interaction_type=interaction_type,
            input_data=input_data,
            output_data=output_data,
            processing_time=processing_time,
        )

    @staticmethod
    def validate_input(required_fields: Iterable[str], data: Dict[str, Any]) -> bool:
        missing = [field for field in required_fields if field not in data]
        if missing:
            logger.error("Missing required fields: %s", missing)
            return False
        return True

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
    def create_conversation_id(self) -> str:
        return f"{self.agent_type}_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}"

    def assess_urgency_indicators(self, text: str) -> Dict[str, Any]:
        high_keywords = (
            "severe",
            "intense",
            "excruciating",
            "unbearable",
            "can't breathe",
            "chest pain",
            "crushing",
            "radiating",
            "sudden",
            "worst ever",
            "emergency",
            "911",
            "help",
        )
        medium_keywords = (
            "moderate",
            "concerning",
            "worsening",
            "spreading",
            "nausea",
            "vomiting",
            "fever",
            "difficulty",
        )
        text_lower = text.lower()
        high_count = sum(1 for keyword in high_keywords if keyword in text_lower)
        medium_count = sum(1 for keyword in medium_keywords if keyword in text_lower)

        urgency = "low"
        if high_count:
            urgency = "high"
        elif medium_count:
            urgency = "medium"

        return {
            "urgency_level": urgency,
            "high_urgency_indicators": high_count,
            "medium_urgency_indicators": medium_count,
            "keywords_found": [
                kw
                for kw in list(high_keywords) + list(medium_keywords)
                if kw in text_lower
            ],
        }

    def format_response(
        self,
        *,
        response_text: str,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "response": response_text,
            "agent_type": self.agent_type,
            "timestamp": datetime.now().isoformat(),
            "conversation_id": self.create_conversation_id(),
            "confidence_score": 7,
            "requires_followup": True,
        }
        if additional_data:
            payload.update(additional_data)
        return payload

    # ------------------------------------------------------------------
    # Health / info helpers
    # ------------------------------------------------------------------
    def health_check(self) -> bool:
        if not self.llm_client.health_check():
            return False

        if hasattr(self.knowledge_store, "health_check"):
            if not self.knowledge_store.health_check():
                return False

        if hasattr(self.patient_db, "health_check"):
            if not self.patient_db.health_check():
                return False

        return True

    def agent_info(self) -> Dict[str, Any]:
        return {
            "agent_type": self.agent_type,
            "model": self.llm_client._model_name,  # noqa: SLF001 - small metadata leak accepted
            "initialized_at": datetime.now().isoformat(),
            "capabilities": [
                "text_generation",
                "symptom_analysis",
                "medical_guidance",
            ],
            "status": "active",
        }
