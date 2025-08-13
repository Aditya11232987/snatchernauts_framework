# Snatchernauts Framework — Developer Manual

This manual gives a high-level map of the codebase, lifecycle, and how to add gameplay using the new Game Logic hooks. It complements inline headers at the top of each module.

Contents
- Directory layout overview
- Load and runtime lifecycle
- Game Logic hooks (global and per-room)
- Public APIs and expected contracts
- UI composition and interactions
- Effects (CRT, Bloom, Letterbox)
- Debugging and logging

## Directory Layout

- `game/script.rpy`: Entry points (`label start`, `label play_room`). Calls `load_room(room)` then `on_room_enter(room)`.
- `game/logic/`
  - `game_logic.rpy`: Global hooks and room handler registry.
  - `rooms/room1_logic.rpy`: Example per-room handler registration and hooks.
- `game/api/`
  - `room_api.rpy`: Room lifecycle (toggle CRT, parameter setters, navigate, etc.).
  - `display_api.rpy`: Background and object visibility helpers.
  - `ui_api.rpy`: Hotspots, hover/unhover, editor/exit button customization.
  - `interactions_api.rpy`: Interaction menu, actions, execution.
- `game/core/`
  - `common_utils.rpy`: Shared helpers (fonts, dev mode checks, mouse position).
  - `common_logging.rpy`: Color-coded, truncating logs; function wrapping; print interception.
  - `config_builders.rpy`, `object_factory.rpy`: Build room/object configs.
  - `bloom_utils.rpy`, `bloom_colors.rpy`: Bloom logic and presets.
  - `room_utils.rpy`: Misc room-related utilities.
  - `rooms/`: `room_config.rpy` & editor.
  - `options.rpy`: Project options and defaults (log toggles).
- `game/ui/`
  - `screens_room.rpy`: Room background + object composition and bloom.
  - `screens_interactions.rpy`: Interaction UI and bindings.
  - `screens_bloom.rpy`: Bloom overlays.
  - `room_descriptions.rpy`: Floating description boxes.
  - `room_ui.rpy`, `room_transforms.rpy`, `screens.rpy`: Additional screens and transforms.
- `game/overlays/`
  - `letterbox_gui.rpy`, `info_overlay.rpy`, `debug_overlay.rpy`, `fade_overlay.rpy`.
- `game/shaders/`
  - `crt_shader.rpy`, `bloom_shader.rpy`.

## Lifecycle

1. `label start` → info overlay flow → `call play_room`.
2. `label play_room(room, music)`:
   - `load_room(room)` → populates `store.room_objects`.
   - Calls `on_room_enter(room)` (global hook + per-room handler) for logic.
   - `call screen room_exploration` for the interactive loop.
3. Hovering objects → `ui_api.handle_object_hover(obj)`:
   - Sets `store.current_hover_object`.
   - Calls `on_object_hover(room_id, obj)` hook.
4. Opening/using interactions → `interactions_api.execute_object_action(obj, action)`:
   - Calls `on_object_interact(room_id, obj, action)` hook before built-in side effects.

## Game Logic Hooks

- `on_game_start()`: One-time init after overlays (optional, call from script if used).
- `on_room_enter(room_id)`: Called after `load_room`; initialize per-room state.
- `on_object_hover(room_id, obj_name)`: Lightweight reactions to hover changes.
- `on_object_interact(room_id, obj_name, action_id)`: Central place to branch gameplay.

Room-specific logic
- Create `game/logic/rooms/<room_id>_logic.rpy` with a handler class and register via `register_room_logic('<room_id>', Handler())`.
- Only implement the hooks you need; the global hooks still run.

## Public API Contracts

- room_api:
  - `toggle_crt_effect()`, `set_crt_parameters(warp, scan, chroma, scanline_size)`
  - `move_object(name, dx, dy)`, `scale_object(name, scale_change)`
  - `get_object_list_for_navigation()`, `gamepad_navigate(dir)`
- display_api:
  - `get_room_background()`, `get_fallback_background()`
  - `should_display_object(obj)`, `is_object_hidden(obj)`
- ui_api:
  - `handle_object_hover(name)`, `handle_object_unhover()`
- interactions_api:
  - `show_interaction_menu(name)`, `execute_object_action(name, action_id)`

All APIs return simple values or update `store` and will log ENTER/EXIT with truncated arguments by default.

## UI & Interactions

- Screen `room_exploration` composes background, objects, bloom, hotspots, overlays, and input handlers.
- Interaction flow:
  - `show_interaction_menu(obj)` sets menu state and selection.
  - Input navigates via `navigate_interaction_menu` and executes via `execute_selected_action()` → `execute_object_action(obj, action_id)`.
  - Before executing the built-in action, the logic hook `on_object_interact(room, obj, action_id)` is called for custom behavior.

## Effects

- CRT: `crt_shader.rpy` with scanlines, chromatic aberration, and horizontal vignette; toggles/params in `room_api`.
- Bloom: `screens_bloom.rpy` and `bloom_utils.rpy`; applied to hovered objects.
- Letterbox: `letterbox_gui.rpy` overlay.

## Debugging & Logging

- Debug overlay (Cmd+Shift+F12 / Ctrl+Shift+F12): hidden → compact → verbose → hidden.
- Logging:
  - `sn_log_enabled`, `sn_log_color`, `sn_log_intercept_prints` toggles (Shift+O to set at runtime).
  - Built-in `print` is intercepted; logs are color-coded, prefixed with `::`, and truncated.

## Conventions & Best Practices

- Only call `game/api/*` from logic.
- Keep UI screens “dumb” — emit events to hooks and render state.
- Add doc headers to new modules with Overview, Contracts, and Examples.
- Keep room assets under `game/images/` matching object ids.
- Run `renpy.sh . lint` before PRs.

