# Winlator Goop Mod

This repository has been reworked as a Winlator-style mod: a lightweight launcher that stages Wine + DXVK, prepares a Roblox prefix, and launches Roblox from a container-like profile that feels closer to Winlator than to a bare Linux desktop wrapper.

## What changed

- The launcher now advertises itself as a Winlator-style mod rather than a generic Linux Wine launcher.
- The default data paths live under `~/.local/share/winlator/goop` and `~/.config/winlator/goop`.
- The GTK UI uses Winlator-like wording: “Prepare Prefix” and “Launch Roblox”.
- The runtime profile is now identified as `winlator-goop` so it is easier to distinguish from the original Goop Launcher flow.

## How it works

1. Run the GUI or CLI diagnostics to validate the host.
2. Prepare a Wine prefix and stage DXVK inside it.
3. Download the official Roblox launcher from Roblox and stage it into the Wine prefix.
4. Launch Roblox under the prepared Wine/DXVK environment.

## Architecture

- `launcher/goop_launcher/` — Python launcher modules
- `scripts/` — shell helpers for building and staging Wine/DXVK assets
- `package/` — Debian packaging and desktop entry

## Status

This is a proof-of-concept adaptation rather than a full Android port of Winlator. The core launcher logic remains intact, but the identity, storage layout, and UI now reflect a Winlator-inspired mod experience.
