# Overview

Snatchernauts extends Ren'Py with a structured, room‑based exploration layer inspired by classic adventures (Snatcher, Policenauts). You write gameplay through simple hooks and APIs; the framework handles UI composition, object navigation, and effects.

Core pillars:
- Interactivity first: hover/selection/menus for in‑room objects
- Clean separation: gameplay logic in .rpy hooks, UI via screens, helpers via API modules
- Cinematic presentation: CRT/Bloom/Letterbox and info/debug overlays
- Friendly defaults: sensible behaviors but easy to override

What this adds beyond generic Ren'Py:
- Pixel‑accurate hotspots and object navigation out‑of‑the‑box
- Centralized lifecycle hooks for gameplay
- Public APIs (room/display/ui/interactions) to avoid screen spaghetti
- Built‑in debug tooling with runtime logging toggles
