#!/usr/bin/env python3
"""Re-export the shared legal ethics compliance manager component."""

from __future__ import annotations

import sys
from pathlib import Path

TEMPLATES_ROOT = Path(__file__).parents[5]
SHARED_ETHICS_PATH = TEMPLATES_ROOT / "components" / "backend" / "legal-ai" / "ethics-manager"
if str(SHARED_ETHICS_PATH) not in sys.path:
    sys.path.insert(0, str(SHARED_ETHICS_PATH))

from LegalEthicsManager import LegalEthicsComplianceManager, EthicsRuleCategory  # type: ignore

__all__ = ["LegalEthicsComplianceManager", "EthicsRuleCategory"]
