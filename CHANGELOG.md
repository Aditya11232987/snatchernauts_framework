# Changelog

## 0.5 — 2025-08-13

### Added
- Centralized game logic hooks in `game/logic/game_logic.rpy` with per-room registry.
- Example room handler in `game/logic/rooms/room1_logic.rpy`.
- Hook wiring: `on_room_enter`, `on_object_hover`, `on_object_interact`.
- Color-coded, truncating logging with print interception and runtime toggles.
- Developer docs: `Wiki/DeveloperManual.md` and `Wiki/Modules.md`.
- Standardized module headers (Overview/Contracts/Integration) across major files.

### Changed
- `script.rpy`: calls `on_game_start()` after info overlay; calls `on_room_enter(room)` after `load_room`.
- `ui_api.handle_object_hover`: emits hook into logic.
- `interactions_api.execute_object_action`: emits hook before built-in effects.

### Removed
- `game/script.rpy.bak` backup file.

### Notes
- Legacy files moved to `game/legacy/` and marked as legacy.
