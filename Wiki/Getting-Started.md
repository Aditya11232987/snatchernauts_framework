# Getting Started

## Requirements
- Engine: Ren'Py 8.4.2
- SDK: set `RENPY_SDK` to your local SDK path
- Targets: Windows and Linux (x86_64)

## Run, Lint, Build
- Run: `$RENPY_SDK/renpy.sh .`
- Lint: `$RENPY_SDK/renpy.sh . lint`
- Distribute: `$RENPY_SDK/renpy.sh . distribute`
- Launcher: Open the repo root → Build & Distribute → select Windows + Linux.

## Common Tasks
- Start default room: `call play_room`
- Start specific room: `call play_room("room2", "audio/room2.ogg")`
- Shorthand: `call go("room2")`
- Dev jump: `call dev_start_room("room3")`
- Clear cache (if visuals stale): `rm -rf game/cache/`
