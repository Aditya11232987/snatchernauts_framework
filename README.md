# Snatchernauts Framework

[![version](https://img.shields.io/badge/version-0.5.1-blue)](CHANGELOG.md)
[![license: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub mirror](https://img.shields.io/badge/github-mirror-blue?logo=github)](https://github.com/grahfmusic/snatchernauts_framework)
[![gitlab pipeline](https://gitlab.com/grahfmusic/snatchernauts_framework/badges/main/pipeline.svg)](https://gitlab.com/grahfmusic/snatchernauts_framework/-/pipelines)

Modern Ren'Py 8.4.x framework for point‑and‑click room exploration with floating descriptions, interaction menus, and configurable CRT/Bloom effects. Centralized hooks make gameplay logic easy to add and test.

Version: 0.5.1 • License: MIT

## Highlights
- Pixel‑accurate hotspots (click only where the image is opaque)
- Floating description boxes with soft outline
- Interaction menus with keyboard/gamepad
- CRT shader (warp/scan/chroma) + horizontal vignette (live tuning)
- Bloom overlays with presets
- Letterbox overlay
- Debug overlay (FPS/memory) with live logging toggles
- Centralized game logic: global + per‑room hooks

## Quick Start
1) Install Ren'Py 8.4.x and set `RENPY_SDK`.
2) Run: `$RENPY_SDK/renpy.sh .`
3) Lint: `bash scripts/lint.sh`

See Wiki/QuickStart.md for full setup and tutorial.

## Controls
- A/Enter/Space: interact (open menu)
- Arrow keys/WASD: navigate objects
- Esc/B: cancel
- Mouse: hover/click objects
- c: toggle CRT • a: toggle scanline animation
- 1–4: scanline size presets
- [ / ]: vignette strength • - / =: vignette width • 0: reset
- i: toggle info overlay
- Cmd+Shift+F12 / Ctrl+Shift+F12: debug overlay cycle (hidden → compact → verbose → hidden)

## Game Logic Hooks
Write gameplay in `game/logic/game_logic.rpy`:
- `on_game_start()` — once after startup overlay
- `on_room_enter(room_id)` — after `load_room(room)`
- `on_object_hover(room_id, obj)` — when hover changes
- `on_object_interact(room_id, obj, action)` — when an action is executed

Per‑room logic: create `game/logic/rooms/<room>_logic.rpy` and register with `register_room_logic('<room>', Handler())`.

## Structure
- `game/logic/`: hooks + room handlers
- `game/api/`: public helpers (room/display/ui/interactions)
- `game/ui/`: composition screens, transforms
- `game/overlays/`: letterbox, info, debug, fade
- `game/shaders/`: CRT and (optional) bloom shader
- `game/core/`: utilities, builders, room config, options

## Docs
- Wiki/QuickStart.md — running, linting, hooks, controls
- Wiki/DeveloperManual.md — lifecycle, hooks, API contracts
- Wiki/Modules.md — module index
- CHANGELOG.md — release notes

## License
MIT — see LICENSE.
