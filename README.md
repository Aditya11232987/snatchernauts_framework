# Snatchernauts Framework

[![version](https://img.shields.io/badge/version-0.5.1-blue)](CHANGELOG.md)
[![license: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![GitHub mirror](https://img.shields.io/badge/github-mirror-blue?logo=github)](https://github.com/grahfmusic/snatchernauts_framework)
[![gitlab pipeline](https://gitlab.com/grahfmusic/snatchernauts_framework/badges/main/pipeline.svg)](https://gitlab.com/grahfmusic/snatchernauts_framework/-/pipelines)

A modern Ren'Py 8.4.x framework for interactive point‑and‑click exploration that brings the energy of Kojima‑era adventures (Snatcher, Policenauts) to contemporary visual novels. Snatchernauts focuses on tactile room interaction, floating descriptions, rich action menus, and cinematic CRT/Bloom overlays — all driven by a clean API and centralized gameplay hooks.

— Designed to make visual novels feel more like games, without fighting the engine.


## Why Snatchernauts?
Visual novels are great at storytelling, but many lack the interactive texture that made classics like Snatcher and Policenauts so engaging. Snatchernauts was built to bridge that gap — keeping Ren'Py’s strengths (scriptability, portability) while layering on:
- Room‑based exploration with pixel‑accurate hotspots
- Contextual interaction menus and hover descriptions
- Game‑like lifecycle hooks for writing logic in one place
- Tasteful CRT/Bloom/Letterbox effects for retro‑cinematic feel

Result: a VN that plays and feels like a classic adventure, with modern ergonomics.


## Features at a Glance
- Pixel‑accurate hotspots and hover descriptions
- Keyboard/gamepad navigation across in‑room objects
- Contextual interaction menus (Examine, Talk, Use, etc.)
- Centralized logic hooks: on_game_start, on_room_enter, on_object_* events
- Debug overlay with live logging controls and performance stats
- CRT shader (warp/scan/chroma) + horizontal vignette (live tuning)
- Optional bloom overlays (fade in/out) and letterbox
- Clean public API modules: room/display/ui/interactions
- Sensible defaults with easy overrides


## How It Works (Architecture)
- Coordinator: `game/script.rpy` starts the info overlay, then calls `on_game_start()` and enters the exploration loop via `play_room()`.
- Public APIs: `game/api/*.rpy` expose helpers for rooms, display/effects, UI, and interactions.
- Logic Layer: put your gameplay in `game/logic/game_logic.rpy` and optional `game/logic/rooms/<room>_logic.rpy` files. Register per‑room handlers.
- UI Layer: screens under `game/ui/` compose descriptions, menus, and overlays.
- Effects: `game/shaders/` and `game/overlays/` provide CRT/Bloom/Letterbox and startup/debug overlays.
- Core Config: `game/core/` contains options, logging, and room configuration helpers.

See the Wiki for a deep dive, code walkthroughs, and examples.


## Quick Start
1) Install Ren'Py 8.4.x and set your SDK path. Example:
   - export RENPY_SDK=~/renpy-8.4.1-sdk
2) Run the project:
   - $RENPY_SDK/renpy.sh .
3) Lint (optional):
   - make lint  or  $RENPY_SDK/renpy.sh . lint
4) Build distributions via Ren’Py Launcher → Build & Distribute.


## Controls (Default)
- A/Enter/Space: interact (open action menu)
- Arrow keys / WASD: navigate objects
- Esc/B: cancel
- Mouse: hover/click objects
- c: toggle CRT • a: toggle scanline animation
- 1–4: scanline size presets
- [ / ]: vignette strength • - / =: vignette width • 0: reset
- i: toggle info overlay
- Cmd+Shift+F12 / Ctrl+Shift+F12: cycle debug overlay


## Core Concepts
- Hooks: write gameplay as Python/renpy functions responding to events:
  - on_game_start() — run once after startup overlay
  - on_room_enter(room_id) — after load_room(room)
  - on_object_hover(room_id, obj)
  - on_object_interact(room_id, obj, action) → bool to mark handled
- Per‑room Logic: implement `register_room_logic('<room>', Handler())` with your own methods.
- APIs: use `room_api`, `ui_api`, `interactions_api`, `display_api` instead of scattering logic in screens.
- Logging: centralized logging interception with color and truncation; toggles available at runtime.


## Project Layout
- game/logic/ — global and per‑room gameplay hooks
- game/api/ — public helper APIs (room/display/ui/interactions)
- game/ui/ — composition screens, transforms
- game/overlays/ — letterbox, info, debug, fades
- game/shaders/ — CRT and bloom shader code
- game/core/ — options, logging, room config, utilities
- scripts/ — helper scripts (push mirroring, wiki sync)
- Wiki/ — documentation


## Documentation
The Wiki covers everything from getting started to APIs and internals:
- Wiki/index.md — table of contents
- Architecture, Hooks, APIs, Screens, Effects, Examples

If you’re new, start with:
- Wiki/01-Overview.md
- Wiki/02-Getting-Started.md


## Roadmap (Short‑term)
- More built‑in actions (Use item, Combine)
- Optional inventory system module
- Room scripting examples beyond room1
- CI recipes for packaging on multiple platforms


## Contributing
Pull requests and suggestions welcome. Please lint before submitting and include a brief rationale in your PR.


## License
MIT — see LICENSE.
