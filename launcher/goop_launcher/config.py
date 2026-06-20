"""Version pins, URLs, and resolved paths for the Winlator-style Goop mod.

This module keeps the same core Wine/DXVK/Roblox flow as the original launcher,
but it now targets a Winlator-inspired profile and storage layout so it feels
more like a container-based launcher rather than a bare Linux .deb wrapper.
"""

from __future__ import annotations

import os
from pathlib import Path

# ── Identity / versioning ───────────────────────────────────────────────────
GOOP_VERSION = "0.2.0-winlator-mod"
APP_NAME = "Winlator Goop Mod"
APP_FAMILY = "Winlator-style"
CONTAINER_PROFILE = "winlator-goop"

# ── Versions (pinned) ────────────────────────────────────────────────────────
WINE_VERSION = "11.9"
# DXVK translates D3D9/10/11 → Vulkan. Pinned release; NVIDIA GPUs still like it.
DXVK_VERSION = "2.6.1"
# Microsoft VC++ redistributable staging version (fetched from official MS CDN).
VCREDIST_VERSION = "14.40.33810.0"

# ── Remote artifact URLs ─────────────────────────────────────────────────────
# Wine 11.9 source + detached GPG signature + sha512sums (verified 2026-05-15).
WINE_SOURCE_URL = (
    f"https://dl.winehq.org/wine/source/11.x/wine-{WINE_VERSION}.tar.xz"
)
WINE_SOURCE_SIGN_URL = WINE_SOURCE_URL + ".sign"
WINE_SHA512SUMS_URL = "https://dl.winehq.org/wine/source/11.x/sha512sums.asc"

# DXVK release tarball from GitHub.
DXVK_URL = (
    f"https://github.com/doitsujin/dxvk/releases/download/v{DXVK_VERSION}/"
    f"dxvk-{DXVK_VERSION}.tar.gz"
)

# Roblox is fetched at runtime from the official setup domain.
# We never redistribute Roblox binaries — copyright belongs to Roblox Corp.
ROBLOX_PLAYER_LAUNCHER_URL = "https://roblox.com/download/client"
ROBLOX_SETUP_USER_AGENT = "WinlatorGoop/" + GOOP_VERSION

# ── Resolved paths ──────────────────────────────────────────────────────────
# XDG-aware. This now uses a Winlator-style data root under ~/.local/share/winlator.
def _xdg(env: str, fallback: str) -> Path:
    val = os.environ.get(env)
    return Path(val) if val else Path.home() / fallback

DATA_DIR = _xdg("XDG_DATA_HOME", ".local/share") / "winlator" / "goop"
CONFIG_DIR = _xdg("XDG_CONFIG_HOME", ".config") / "winlator" / "goop"
CACHE_DIR = _xdg("XDG_CACHE_HOME", ".cache") / "winlator" / "goop"

# Staged Wine 11.9 tree. The mod prefers a Winlator-style install root.
SYSTEM_WINE_DIR = Path("/opt/winlator/goop/wine-11.9")
USER_WINE_DIR = DATA_DIR / "wine-11.9"

# The Wine prefix Roblox lives in.
PREFIX_DIR = DATA_DIR / "prefix"

# Staged Roblox assets live inside the prefix's drive_c.
ROBLOX_DRIVE_C = PREFIX_DIR / "drive_c" / "users" / os.environ.get("USER", "winlator")
ROBLOX_INSTALL_DIR = ROBLOX_DRIVE_C / "AppData" / "Local" / "Roblox"

# Downloads/cache for installers.
DOWNLOADS_DIR = CACHE_DIR / "downloads"

# Wine prefix environment. The profile now advertises a Winlator-like runtime setup.
WINE_ENV_BASE: dict[str, str] = {
    "WINEPREFIX": str(PREFIX_DIR),
    "WINEARCH": "win64",
    "WINEDLLOVERRIDES": "d3d9=native; d3d10core=native; d3d11=native; dxgi=native",
    "GOOP_RUNTIME": "winlator-mod",
}

# ── Thresholds for the guards ────────────────────────────────────────────────
MIN_DISK_MB = 5000            # ~5 GB free for prefix + Roblox staging.
MIN_VULKAN_API_VERSION = (1, 3)  # DXVK 2.x wants Vulkan 1.3+.
SUPPORTED_ARCHES = ("x86_64", "amd64")
TARGET_GPU = "NVIDIA dGPU"    # advisory; any recent NVIDIA dGPU is acceptable.
TARGET_DRIVER_MIN = 535       # NVIDIA branch that ships Vulkan 1.3 fully.

# The exact Wine build we will run. Asserted at launch time.
EXPECTED_WINE_VERSION = "wine-" + WINE_VERSION
