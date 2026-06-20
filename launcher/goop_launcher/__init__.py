"""Winlator Goop Mod — a Winlator-style launcher for Roblox on Linux.

The package is split so that the GUI layer (``app.py``) is the only module that
imports PyGObject. Everything else (``config``, ``checks``, ``wine``, ``roblox``)
remains importable headless, which keeps the diagnostics flow usable in CI.
"""

from __future__ import annotations

__all__ = ["__version__", "GOOP_APP_NAME"]

__version__ = "0.2.0-winlator-mod"
GOOP_APP_NAME = "Winlator Goop Mod"
