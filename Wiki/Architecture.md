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

## Module Interaction Overview
```
label start
   │
   ▼
room_api.play_room(room)
   │        ▲
   │        │ uses
   │   core/config_builders + object_factory
   │        │
   ▼        │ definitions
ui/screens_room            core/rooms/room_config
   │         ▲                   │
   │ calls   │ updates           │ handlers
   ▼         │                   ▼
ui_api  ←→  display_api     interactions_api
   │                           │
   │ toggles                   │ builds menus, routes actions
   ▼                           ▼
shaders (crt/bloom)       overlays (letterbox/info/debug)
```

Summary
- Entry triggers `room_api.play_room`, which reads room/object config via `config_builders` and `object_factory`.
- `screens_room` composes the scene and wires hotspots through `ui_api`; visibility is coordinated via `display_api`.
- `interactions_api` constructs interaction menus and dispatches to room/object handlers defined in `room_config`.
- Effects and overlays are toggled from `room_api` and rendered by `shaders` and overlay screens.
