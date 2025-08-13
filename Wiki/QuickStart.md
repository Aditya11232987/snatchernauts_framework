# Quick Start

This guide helps you run, lint, and extend the project with centralized game logic.

## Prerequisites
- Ren'Py 8.4.x SDK installed (path example: `/home/grahf/renpy-8.4.1-sdk`).
- Environment variable `RENPY_SDK` pointing to your SDK.

```bash
export RENPY_SDK=/path/to/renpy-8.4.x-sdk
$RENPY_SDK/renpy.sh .
```

## Run the Game
- Launch via Ren'Py Launcher or the SDK script:
  - `$RENPY_SDK/renpy.sh .`
- Developer Mode (recommended): enable in Launcher Preferences, or set `config.developer = True` while testing.

## Lint
- Run from the project root:
```bash
bash scripts/lint.sh
```

## Centralized Game Logic
- Write high-level behavior in `game/logic/game_logic.rpy`.
- Hooks available:
  - `on_game_start()` – once after the info overlay.
  - `on_room_enter(room_id)` – after `load_room(room)` and before exploration.
  - `on_object_hover(room_id, obj)` – when hover changes.
  - `on_object_interact(room_id, obj, action)` – when an interaction is executed.

### Examples
- Open `game/logic/game_logic.rpy` and see the commented examples inside the hooks:
  - Show a hint on entering `room1`.
  - Branch interaction behavior (e.g., `detective + examine`).
  - Change CRT parameters on `open`.

### Per-Room Logic
- Create a handler: `game/logic/rooms/<room_id>_logic.rpy`.
- Register it: `register_room_logic('room1', Room1Logic())`.
- Implement any subset of hooks.

## Public APIs (use from logic)
- Room: `toggle_crt_effect()`, `set_crt_parameters(...)`, `move_object(...)`, `scale_object(...)`.
- Display: `hide_object(name)`, `show_object(name)`, `is_object_hidden(obj)`.
- Interactions: Actions are executed via `execute_object_action` (already wired to `on_object_interact`).

## Debug Overlay
- Toggle visibility/verbosity: Cmd+Shift+F12 (mac) / Ctrl+Shift+F12 (others): hidden → compact → verbose → hidden.
- Shows FPS/memory, room/object/CRT state, and now includes logging toggles:
  - `sn_log_enabled`, `sn_log_color`, `sn_log_intercept_prints`.
- Drag to move; F1–F4 snap corners.

## Logging
- Default: color-coded, `::`-prefixed, and truncated for readability.
- Runtime toggles (Shift+O console):
```python
sn_log_enabled = True  # or False
sn_log_color = True
sn_log_intercept_prints = True
```

## Adding a New Object (example)
1) Add an image to `game/images/`.
2) In `game/core/rooms/room_config.rpy`, add to `ROOM_DEFINITIONS['roomX']['objects']` using `merge_configs(...)` and `create_bloom_config(...)`.
3) Restart the game; hover to see the description, press A/Enter to interact.
4) Handle behavior in `on_object_interact` or a room handler.

## Troubleshooting
- Shader changes require a full restart (for recompilation).
- If labels appear duplicated, remove old `.rpyc` files after moving scripts.
- Use the lint script before commits.
