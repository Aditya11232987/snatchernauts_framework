# Getting Started

## Requirements
- Engine: Ren'Py 8.4.1 (framework tested with 8.4.1)
- SDK: set `RENPY_SDK` to your local SDK path (defaults to `~/renpy-8.4.1-sdk`)
- Targets: Windows and Linux (x86_64)

## Run, Lint, Build
- Run: `$RENPY_SDK/renpy.sh .`
- Lint: `bash scripts/lint.sh` (uses RENPY_SDK or defaults to `~/renpy-8.4.1-sdk`)
- Distribute: `$RENPY_SDK/renpy.sh . distribute`
- Launcher: Open the repo root → Build & Distribute → select Windows + Linux.

## Common Tasks
- Start default room: `call play_room`
- Start specific room: `call play_room("room2", "audio/room2.ogg")`
- Shorthand: `call go("room2")`
- Dev jump: `call dev_start_room("room3")`
- Clear cache (if visuals stale): `rm -rf game/cache/`
