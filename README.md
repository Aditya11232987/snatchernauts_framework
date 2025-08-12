# Snatchernauts Framework

[![pages](https://img.shields.io/badge/Pages-Live-brightgreen?logo=gitlab)](https://grahfmusic.gitlab.io/snatchernauts_framework/)

A modular Ren'Py 8.4.2 framework for point‑and‑click room exploration, interaction menus, overlays, and retro display effects. Inspired by the cinematic adventure pacing and UI sensibilities of Snatcher and Policenauts.

## Highlights
- Modular rooms: define backgrounds + interactive objects in `ROOM_DEFINITIONS`.
- Interaction menus: keyboard, mouse, and gamepad navigation out of the box.
- Effects: CRT shader toggles and per‑object bloom presets.
- Unified entry: `play_room(room, music=None)` and shorthand `go(room)` simplify flow.
- Cross‑platform: Builds for Windows and Linux.

## Requirements
- Engine: Ren’Py 8.4.2
- SDK: set `RENPY_SDK` to your local SDK path (source `scripts/env.sh` on this machine).

## Quick Start
- Source env (this machine): `. scripts/env.sh`
- Run: `$RENPY_SDK/renpy.sh .`
- Lint: `$RENPY_SDK/renpy.sh . lint`
- Distribute (Win/Linux): `$RENPY_SDK/renpy.sh . distribute`
- Launcher: open the repo root (not `game/`) → Build & Distribute → Windows + Linux.

## Developing
- Entry label: `game/script.rpy` → `label start` → `play_room`.
- Start a specific room: `call play_room("room2", "audio/room2.ogg")` or `call go("room2")`.
- Main composition screen: `game/ui/screens_room.rpy` → `screen room_exploration` (background, objects, hotspots, overlays, inputs).
- Define rooms/objects: `game/core/rooms/room_config.rpy` using `create_room_object(...)`.
- Dev helper: `label dev_start_room(room="room1", music=None)` to jump straight to a room.

## Directory Layout
- `game/api/`: room, display, UI, interactions APIs
- `game/core/`: config builders, room config, bloom utils, common utils
- `game/ui/`: screens, GUI, transforms, exploration composition
- `game/overlays/`: info/debug overlays, letterbox
- `game/shaders/`: CRT + bloom passes

## Mini Tutorial (2‑Room Demo)
1) Add assets under `game/images/` (e.g., `room2.png`, `lamp.png`).
2) In `room_config.rpy`, add a `"room2"` entry with a `create_room_object(...)` lamp (see Wiki).
3) From any label: `call play_room("room2")` to jump into the room.
Full walkthrough: `Wiki/Mini-Tutorial.md`.

## Docs
- Contributor guide: `AGENTS.md`
- Documentation site: https://grahfmusic.gitlab.io/snatchernauts_framework/
- Wiki sources: `Wiki/` (Getting Started, Architecture, Rooms & Objects, UI & Screens, Effects, Interactions, CI, Troubleshooting)

## CI & Pages
- GitLab CI runs syntax checks for Python blocks in `.rpy` and builds the docs site.
- Pages deploys MkDocs output from `Wiki/` to the link above.
- Coverage badge is included; configure coverage reporting later to show a %.

## Credits & Inspiration
- Heavily inspired by the atmosphere and UI flow of Konami’s Snatcher and Policenauts.
- Built on Ren’Py — thank you to the engine and community.
