#!/usr/bin/env python3
"""Re-export the shared legal security manager component."""

from __future__ import annotations

import sys
from pathlib import Path

# Load shared component from templates/components
TEMPLATES_ROOT = Path(__file__).parents[5]
SHARED_SECURITY_PATH = TEMPLATES_ROOT / "components" / "backend" / "legal-ai" / "ethics-manager"
if str(SHARED_SECURITY_PATH) not in sys.path:
    sys.path.insert(0, str(SHARED_SECURITY_PATH))

from LegalSecurityManager import AttorneyClientPrivilegeManager  # type: ignore

__all__ = ["AttorneyClientPrivilegeManager"]
