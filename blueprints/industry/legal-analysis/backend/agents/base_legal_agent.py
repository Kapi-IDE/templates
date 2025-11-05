#!/usr/bin/env python3
"""Expose the shared legal BaseAgent component for blueprint agents."""

from __future__ import annotations

import sys
from pathlib import Path

# Reuse the shared legal AI base agent component to keep implementation aligned
# with the rest of the blueprint catalog. This mirrors how the healthcare
# blueprint loads its base agent from the shared components workspace.
templates_dir = Path(__file__).parents[5]
shared_component_path = templates_dir / "components" / "backend" / "legal-ai" / "base-agent"
if str(shared_component_path) not in sys.path:
    sys.path.insert(0, str(shared_component_path))

from BaseLegalAgent import BaseLegalAgent as SharedBaseLegalAgent  # type: ignore


class BaseLegalAgent(SharedBaseLegalAgent):
    """Thin wrapper that keeps backwards-compatible import paths for agents."""

    pass


__all__ = ["BaseLegalAgent"]
