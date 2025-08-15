# Release 0.5.1 — 2025-08-13

This is a maintenance and polish release focusing on safer logging, clearer interaction flow, and small UI improvements.

Highlights
- Logging: guard ORIG_PRINT resolution on reload using fallback `_get_orig_print` to avoid `NameError`.
- Interactions: `on_object_interact` now returns `bool`; default handlers short‑circuit when handled.
- UI: confirmations for Exit/Main Menu; accidental game_menu disabled during exploration.
- Room1: custom examines and patreon take handling; return `True` when handled.
- Minor: tooltip tweaks and logging cosmetics.

Chore
- Save local edits; add `game/core/common_init.rpy`.

Upgrade Notes
- No breaking API changes.
- Recommended to review your room interaction handlers to optionally return `True` when an action is fully handled to prevent default fallbacks.

Links
- Tag: 0.5.1
- Changelog: ../CHANGELOG.md
- GitLab Release: https://gitlab.com/grahfmusic/snatchernauts_framework/-/releases/0.5.1
