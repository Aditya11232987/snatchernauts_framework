# Game Logic Architecture

This project centralizes high-level logic into a dedicated module while keeping room logic optional and focused.

Goals
- Keep logic in one place (or one file per room) with clear hooks.
- Call only public APIs (`game/api/*`) from logic to avoid coupling.
- Make it trivial to add/factor behaviors without touching UI internals.

Where to write logic
- Global module: `game/logic/game_logic.rpy`
  - Hooks you can implement globally:
    - `on_game_start()` – called once after the start overlay flow.
    - `on_room_enter(room_id)` – after `load_room(room_id)`.
    - `on_object_hover(room_id, obj_name)` – when hover changes.
    - `on_object_interact(room_id, obj_name, action_id)` – on interaction.
- Room modules: `game/logic/rooms/<room_id>_logic.rpy`
  - Implement any subset of the same hooks and register:
    ```python
    register_room_logic('room1', Room1Logic())
    ```

How hooks are invoked
- `on_room_enter(room_id)` is called from `label play_room` in `game/script.rpy` immediately after `load_room(room)`.
- `on_object_hover/on_object_interact` can be invoked from existing handlers (e.g., `ui_api.handle_object_hover`, interaction execution) by calling the hook with the current `store.current_room_id`.

Examples
- Set defaults on room entry:
  ```python
  def on_room_enter(room_id):
      store.crt_enabled = True
      store.crt_vignette_strength = 0.95
      store.crt_vignette_width = 0.14
  ```
- Per-room handler (see `game/logic/rooms/room1_logic.rpy`):
  ```python
  class Room1Logic:
      def on_room_enter(self, room_id):
          store.crt_vignette_strength = 0.95
          store.crt_vignette_width = 0.14
  register_room_logic('room1', Room1Logic())
  ```

API usage
- Public APIs are under `game/api/`. Useful calls include:
  - `room_api.toggle_crt_effect()`, `room_api.set_crt_parameters(...)`
  - `room_api.move_object(obj, dx, dy)`, `room_api.scale_object(obj, delta)`
  - `display_api.hide_object(obj)`, `display_api.show_object(obj)`
  - `ui_api.handle_object_hover(obj)` (already integrated by UI)

Best practices
- Do not import or mutate UI internals from logic modules; call APIs only.
- Keep per-room logic minimal; use global hooks for cross-room behavior.
- Log sparingly; the project includes a truncating, color-coded logger with toggles:
  - `sn_log_enabled`, `sn_log_color`, `sn_log_intercept_prints`

Migration tips
- If you have ad-hoc logic in room config or UI files, progressively move it into hooks here.
- Start by wiring `on_object_interact` when executing an action from the interaction menu; you can branch behavior here without touching the UI layer.

