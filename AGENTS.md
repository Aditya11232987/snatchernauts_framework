# Repository Guidelines

## Project Structure & Module Organization
- `game/api/`: Public APIs
  - `room_api.rpy`: room/object lifecycle, CRT toggles, gamepad.
  - `display_api.rpy`: display and visibility helpers.
  - `ui_api.rpy`: hotspots, hover, button customization.
  - `interactions_api.rpy`: interaction menu routines/handlers.
- `game/core/`: Config, factories, utilities
  - `common_utils.rpy`, `room_utils.rpy`: shared helpers.
  - `config_builders.rpy`, `object_factory.rpy`: build configs/instances.
  - `bloom_utils.rpy`, `bloom_colors.rpy`: bloom logic/presets.
  - `font_config.rpy`, `options.rpy`: fonts and Ren’Py options.
  - `rooms/`: `room_config.rpy`, `room_editor.rpy`, `room_main.rpy`.
- `game/ui/`: Screens and composition
  - `screens_room.rpy`, `screens_bloom.rpy`, `screens_interactions.rpy`.
  - `room_ui.rpy`, `room_descriptions.rpy`, `room_transforms.rpy`, `screens.rpy`.
- `game/overlays/`: `letterbox_gui.rpy`, `info_overlay.rpy`, `debug_overlay.rpy`.
- `game/shaders/`: `crt_shader.rpy`, `bloom_shader.rpy`.
- `Wiki/`: MkDocs docs sources; `scripts/`: utility scripts.

## Build, Test, and Development Commands
- Run: `$RENPY_SDK/renpy.sh .` (set `RENPY_SDK` to Ren’Py 8.4.2 SDK path).
- Lint: `$RENPY_SDK/renpy.sh . lint` (validates Ren’Py + embedded Python).
- Distribute: `$RENPY_SDK/renpy.sh . distribute` (Windows/Linux packages).
- Docs: `mkdocs serve` (local) or `mkdocs build`.

## Coding Style & Naming Conventions
- Indentation: 4 spaces for Ren’Py and Python blocks.
- Python style: `snake_case` for functions/vars, `UPPER_CASE` for constants.
- Screens/UI: `screen room_exploration`, `screens_*` files; keep names descriptive.
- Rooms/objects: lowercase IDs (e.g., `room1`, `lamp`); image files under `game/images/` match usage.
- Module layout: public interfaces in `game/api/`; helpers in `game/core/` and `game/ui/`.

## Testing Guidelines
- Static checks: run `$RENPY_SDK/renpy.sh . lint` locally and in CI before PRs.
- Manual verification: launch and use `label dev_start_room(room="room1", music=None)` to jump into a room.
- Regressions: exercise interaction menu, overlays, and CRT/bloom toggles when changing UI/effects.

## Module Interaction Overview
- Entry: `label start` calls `play_room`/`go` in `game/api/room_api.rpy`.
- Config: `room_api` reads room/object definitions from `game/core/rooms/room_config.rpy` via `config_builders` + `object_factory`.
- Composition: `game/ui/screens_room.rpy` assembles background/objects, wires `ui_api` hotspots; `display_api` manages visibility.
- Interactions: `interactions_api` builds menus and routes handlers back to room/object functions defined in room config.
- Effects/Overlays: `room_api` toggles CRT/bloom; `screens_bloom` and `game/shaders/*.rpy` render effects; overlays draw on top.

## Commit & Pull Request Guidelines
- Commit style: short imperative subject; use scopes when helpful (e.g., `feat(ui):`, `fix(core):`, `docs:`). Examples in `git log`.
- PRs must include: clear description, rationale, screenshots/GIFs for UI changes, steps to test, and linked issues.
- Keep changes modular: API changes in `game/api/`, internal helpers in `game/core/` or `game/ui/` with accompanying notes.

## Security & Configuration Tips
- Do not commit SDKs or secrets; set `RENPY_SDK` in your shell profile.
- Large binaries: keep under `game/` (images/audio); avoid unused assets.
- Shaders: test on multiple GPUs if changing CRT/bloom to avoid portability issues.
