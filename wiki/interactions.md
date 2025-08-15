# Interactions

## Showing Menus
- Hover and click a hotspot to call `show_interaction_menu(obj_name)`.
- The menu options are determined by `object_type` (e.g., `character`, `item`).

## Navigation & Actions
- Keyboard: Up/Down to move, Enter to confirm, Esc to cancel.
- Gamepad: D‑pad/left stick, A to confirm, B to cancel.
- API (`api/interactions_api.rpy`):
  - `navigate_interaction_menu("up"|"down")`
  - `execute_selected_action()`
  - `get_button_action(obj, data)` for screen buttons

## Extend Interactions
- Add or adjust available actions per `object_type` in the interactions configuration (see `ui/screens_interactions.rpy`).
- Implement handlers in `api/interactions_api.rpy` (e.g., `handle_talk_action`, `handle_examine_action`).
