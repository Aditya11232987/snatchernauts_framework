# Getting Started

Requirements
- Ren'Py 8.4.x installed
- RENPY_SDK environment variable set (e.g., `export RENPY_SDK=~/renpy-8.4.1-sdk`)

Run
- `$RENPY_SDK/renpy.sh .`

Lint
- `make lint` or `$RENPY_SDK/renpy.sh . lint`

Build
- Use Ren’Py Launcher → Build & Distribute

Project layout (high level)
- `game/logic/` — your gameplay hooks
- `game/api/` — helper APIs (room, display, ui, interactions)
- `game/ui/` — composition screens
- `game/overlays/` — letterbox/info/debug overlays
- `game/shaders/` — CRT/Bloom
- `game/core/` — options, logging, room config

Next: read 03-Architecture and 04-Logic-Hooks.

