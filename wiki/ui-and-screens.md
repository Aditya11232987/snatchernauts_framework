# UI & Screens

## Main Composition
- `screen room_exploration` in `game/ui/screens_room.rpy` wires everything:
  - Background/objects: `use room_background_and_objects`
  - Hotspots: `use object_hotspots`
  - UI buttons: `use room_ui_buttons`
  - Overlays: `use debug_overlay`, `use info_overlay`
  - Inputs: keyboard/gamepad keys defined inline

Edit this screen to change layout, bindings, or overlays.

## Background & Objects
- `screen room_background_and_objects` renders the current background and all `room_objects` with optional CRT effect and fade.
- Customize default fade/CRT in `script.rpy` defaults.

## UI Buttons & Hotspots
- Hotspots in `game/ui/room_ui.rpy` loop over `room_objects` and call `show_interaction_menu(obj)`.
- Buttons use `get_room_exit_action()` and `get_editor_mode_action()` from `api/ui_api.rpy`.
