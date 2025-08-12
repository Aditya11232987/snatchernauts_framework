# Architecture

## Flow
- `label start` → `play_room(room, music)` in `game/script.rpy`.
- `screen room_exploration` (in `game/ui/screens_room.rpy`) composes background, objects, hotspots, overlays, and input.
- `ROOM_DEFINITIONS` (in `game/core/rooms/room_config.rpy`) defines rooms and objects.

## Modules
- `api/room_api.rpy`: load/swap rooms, move/scale, save/reset, navigation.
- `api/display_api.rpy`: background helpers and visual hooks.
- `api/ui_api.rpy`: exit button, UI customization, hover handlers.
- `api/interactions_api.rpy`: show/hide interaction menu, navigate/execute actions.
- `ui/screens_room.rpy`: background/object drawing and exploration composition.
- `ui/room_ui.rpy`: hotspots + UI buttons.
- `overlays/`: info/debug and letterbox.
- `shaders/`: CRT and bloom passes.
