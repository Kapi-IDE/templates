"""Utilities for capturing and persisting agent interactions."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def log_interaction(
    patient_db: Any,
    *,
    agent_type: str,
    patient_id: str,
    interaction_type: str,
    input_data: Dict[str, Any],
    output_data: Dict[str, Any],
    processing_time: Optional[float] = None,
) -> None:
    """Persist an audit-friendly summary of an agent interaction.

    The helper keeps logging concerns out of individual agents while still
    emitting error telemetry if we cannot write to the backing store.
    """
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,
            "patient_id": patient_id,
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

        patient_db.log_audit_event(
            patient_id=patient_id,
            action=f"{agent_type}_interaction",
            details=json.dumps(log_entry),
        )
    except Exception as exc:  # pragma: no cover - best effort logging
        logger.error("Failed to log interaction: %s", exc)
