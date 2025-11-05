"""Utilities for capturing and persisting agent interactions across any domain."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def log_interaction(
    data_store: Any,
    *,
    agent_type: str,
    user_id: str,
    interaction_type: str,
    input_data: Dict[str, Any],
    output_data: Dict[str, Any],
    processing_time: Optional[float] = None,
) -> None:
    """Persist an audit-friendly summary of an agent interaction.

    The helper keeps logging concerns out of individual agents while still
    emitting error telemetry if we cannot write to the backing store.

    Args:
        data_store: Database/store with log_audit_event method
        agent_type: Type of agent (e.g., 'triage', 'risk_analysis')
        user_id: Identifier for user/client/patient
        interaction_type: Type of interaction (e.g., 'query', 'analysis')
        input_data: Input data dictionary
        output_data: Output data dictionary
        processing_time: Optional processing time in seconds
    """
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,
            "user_id": user_id,
            "interaction_type": interaction_type,
            "processing_time_seconds": processing_time,
            "input_summary": {
                "keys": list(input_data.keys()),
                "message_length": len(str(input_data.get("message", ""))),
            },
            "output_summary": {
                "keys": list(output_data.keys()),
                "response_length": len(str(output_data.get("response", ""))),
            },
            "success": True,
        }

        # Try domain-specific logging method first, fall back to generic
        if hasattr(data_store, 'log_audit_event'):
            data_store.log_audit_event(
                user_id=user_id,
                action=f"{agent_type}_interaction",
                details=json.dumps(log_entry),
            )
        elif hasattr(data_store, 'log'):
            data_store.log(log_entry)
        else:
            logger.warning("No logging method found on data_store, skipping")

    except Exception as exc:  # pragma: no cover - best effort logging
        logger.error("Failed to log interaction: %s", exc)
