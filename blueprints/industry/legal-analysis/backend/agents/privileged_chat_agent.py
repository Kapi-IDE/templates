#!/usr/bin/env python3
"""Attorney-client privileged communication agent."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base_legal_agent import BaseLegalAgent


class PrivilegedChatAgent(BaseLegalAgent):
    """Handles privileged chat flows with encryption and audit logging."""

    def __init__(
        self,
        knowledge_store: Any,
        legal_db: Any,
        privilege_manager: Any,
        ethics_manager: Any,
    ):
        super().__init__(knowledge_store, legal_db, "privileged_chat")
        self.privilege_manager = privilege_manager
        self.ethics_manager = ethics_manager

    def start_session(
        self,
        *,
        attorney_id: str,
        client_id: Optional[str] = None,
        session_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.privilege_manager.create_secure_session(attorney_id, client_id, session_context)

    def handle_message(
        self,
        message: str,
        *,
        session_id: str,
        session_token: str,
        attorney_id: str,
        client_id: Optional[str] = None,
        case_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        verification = self.privilege_manager.verify_privileged_access(
            session_id=session_id,
            session_token=session_token,
            attorney_id=attorney_id,
            client_id=client_id,
        )
        if not verification.get("authorized"):
            return {"authorized": False, "error": verification.get("reason", "unauthorized")}

        prompt = self._create_legal_system_prompt(
            """
            You are in a privileged attorney-client conversation. Respond with empathy,
            summarize next actions, and log key facts that should sync into the case file.
            """
        )
        response_text = self._generate_legal_response(
            prompt + f"\n\nCLIENT MESSAGE:\n{message}",
            attorney_id=attorney_id,
            client_id=client_id,
            case_context={"case_id": case_id},
        )

        structured = self._extract_legal_structured_data(response_text, "privileged_chat")

        communication_id = None
        if client_id:
            communication_payload = {
                "case_id": case_id,
                "communication_type": "privileged_chat",
                "content": response_text,
                "participants": [attorney_id, client_id],
            }
            communication_id = self.legal_db.store_privileged_communication(
                attorney_id,
                client_id,
                communication_payload,
            )

        ethics_entry = self.ethics_manager.monitor_client_communication_compliance(
            attorney_id,
            client_id or "internal",
            {
                "ai_assistance_used": True,
                "ai_mentioned_in_communications": True,
                "response_times": [verification.get("remaining_time_minutes", 0)],
            },
        )

        return {
            "authorized": True,
            "response": response_text,
            "structured": structured,
            "communicationId": communication_id,
            "ethics": ethics_entry,
        }


__all__ = ["PrivilegedChatAgent"]
