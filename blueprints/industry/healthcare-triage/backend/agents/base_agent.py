#!/usr/bin/env python3
"""Base agent leveraging reusable components for the healthcare blueprint."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add components directory to path for imports
# Path structure: healthcare-triage/backend/agents/base_agent.py
# Navigate: agents -> backend -> healthcare-triage -> industry -> blueprints -> templates -> components
templates_dir = Path(__file__).parents[5]  # Get to templates/
components_path = templates_dir / "components" / "backend"
if str(components_path) not in sys.path:
    sys.path.insert(0, str(components_path))

from agent_framework.agent.base import AgentFoundation

logger = logging.getLogger(__name__)


class BaseAgent(AgentFoundation):
    """Extends the shared foundation with healthcare-specific behaviour."""

    # Override BASE_PROMPT with healthcare-specific guidelines
    BASE_PROMPT = """
You are a healthcare AI assistant designed to help with patient triage and care.

IMPORTANT GUIDELINES:
- You are NOT a replacement for professional medical advice
- Always recommend seeking professional medical care for serious symptoms
- Be empathetic and professional in all interactions
- Ask clarifying questions to better understand patient symptoms
- Focus on gathering information for proper triage
- Never provide specific diagnoses - only general information
- Always prioritize patient safety

CONTEXT:
- You are part of a multi-agent healthcare system
- Your responses will be used by other agents for triage decisions
- Maintain patient privacy and confidentiality
- Document all interactions for continuity of care
"""

    def __init__(self, knowledge_store: Any, patient_db: Any, agent_type: str = "base"):
        super().__init__(
            knowledge_store=knowledge_store,
            data_store=patient_db,  # Map to generic parameter name
            agent_type=agent_type,
        )
        self.patient_db = patient_db  # Keep for backward compatibility
        logger.info("%s agent initialised", agent_type.title())

    def create_system_prompt(self, instructions: str) -> str:
        """Expose a semantic helper for specialised agents."""
        return self.build_system_prompt(instructions)

    # ------------------------------------------------------------------
    # Convenience wrappers kept for backward compatibility with
    # specialised agents already using these method names.
    # ------------------------------------------------------------------
    def _create_system_prompt(self, specific_instructions: str) -> str:  # pragma: no cover - legacy alias
        return self.create_system_prompt(specific_instructions)

    def _generate_response(
        self, prompt: str, patient_context: Optional[Dict[str, Any]] = None
    ) -> str:  # pragma: no cover - legacy alias
        return self.generate_response(prompt, context=patient_context)

    def fallback_response(self) -> str:
        """Healthcare-specific fallback message."""
        return (
            "I apologize, but I'm experiencing technical difficulties. "
            "Please contact a healthcare professional directly if you have urgent medical concerns."
        )

    def _get_fallback_response(self) -> str:  # pragma: no cover - legacy alias
        return self.fallback_response()

    def _extract_structured_data(self, text: str, structure_type: str) -> Dict[str, Any]:  # pragma: no cover - legacy alias
        return self.extract_structured_data(text=text, structure_type=structure_type)

    def _log_interaction(  # pragma: no cover - legacy alias
        self,
        patient_id: str,
        interaction_type: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        processing_time: Optional[float] = None,
    ) -> None:
        self.log_interaction(
            user_id=patient_id,  # Map to generic parameter
            interaction_type=interaction_type,
            input_data=input_data,
            output_data=output_data,
            processing_time=processing_time,
        )

    def _validate_input(self, required_fields, data):  # pragma: no cover - legacy alias
        return self.validate_input(required_fields, data)

    def _create_conversation_id(self) -> str:  # pragma: no cover - legacy alias
        return self.create_conversation_id()

    def _assess_urgency_indicators(self, text: str) -> Dict[str, Any]:  # pragma: no cover - legacy alias
        return self.assess_urgency_indicators(text)

    def _format_medical_response(self, response_text: str, additional_data: Dict[str, Any] = None) -> Dict[str, Any]:  # pragma: no cover - legacy alias
        return self.format_response(response_text=response_text, additional_data=additional_data)

    def health_check(self) -> bool:  # noqa: D401 - docstring inherited
        return super().health_check()

    def get_agent_info(self) -> Dict[str, Any]:  # noqa: D401 - docstring inherited
        return super().agent_info()
