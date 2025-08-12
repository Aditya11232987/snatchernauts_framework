# Snatchernauts Framework

A Ren'Py 8.4.2 point‑and‑click room exploration framework. It provides a modular room system, interaction menus, UI overlays, and CRT/bloom effects to build adventure scenes quickly.

## Quick Start
- For this machine: `. scripts/env.sh` to set `RENPY_SDK`.
- Otherwise, set `RENPY_SDK` to your Ren’Py 8.4.2 SDK path.
- Run: `$RENPY_SDK/renpy.sh .`
- Lint: `$RENPY_SDK/renpy.sh . lint`
- Distribute (Win/Linux): `$RENPY_SDK/renpy.sh . distribute`
- Launcher: Open the repo root in the Ren’Py Launcher → Build & Distribute → select Windows + Linux.

## Develop
- Entry point: `game/script.rpy` → `label start` → `play_room`.
- Start a room: `call play_room("room2", "audio/room2.ogg")` or `call go("room2")`.
- Edit the exploration screen: `game/ui/screens_room.rpy` → `screen room_exploration`.
- Add rooms/objects: `game/core/rooms/room_config.rpy` via `ROOM_DEFINITIONS` and `create_room_object(...)`.

## Repo Structure
- `game/api/`: Room, display, UI, and interactions APIs.
- `game/core/`: Config builders, room config, bloom utils, shared utils.
- `game/ui/`: Screens, GUI, transforms, and composition.
- `game/overlays/`: Info/debug overlays and letterbox.
- `game/shaders/`: Bloom and CRT passes.

## Docs
- Contributor guide: `AGENTS.md`
- Full wiki: `Wiki/README.md`
  - Getting Started, Architecture, Rooms & Objects, UI & Screens
  - Mini Tutorial (two-room demo): `Wiki/Mini-Tutorial.md`
  - Build & CI and CI Examples: `Wiki/Build-and-CI.md`, `Wiki/CI-Examples.md`
  - Troubleshooting

## Targets & Version
- Engine: Ren’Py 8.4.2
- Platforms: Windows and Linux (x86_64)
