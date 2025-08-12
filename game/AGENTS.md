# Repository Guidelines

## Project Structure & Module Organization
- Entry: `script.rpy` (root), `core/rooms/room_main.rpy` (runtime aggregator).
- Core API: `api/` (room/display/ui/interactions).
- Core helpers: `core/` (utils, configs, object factory); `core/rooms/` (room config, editor, runtime).
- UI: `ui/` (room screens, interactions, transforms, global screens, GUI).
- Overlays: `overlays/` (letterbox, info/debug overlays).
- Shaders: `shaders/` (bloom and CRT code).
- Debug: `debug/` (reserved).
- Assets: `images/`, `audio/`, `fonts/`, GUI art under `gui/`; translations in `tl/`; support in `libs/`.

## Architecture Overview
- Room system: `room_config.rpy`, `room_descriptions.rpy`, and `room_functions.rpy` define data + logic; `room_display.rpy`, `room_ui.rpy`, and `room_transforms.rpy` render and animate.
- Object system: `object_factory.rpy` creates entities; `object_interactions.rpy` handles interaction rules and events.
- Rendering/UI: `screens.rpy` and `gui.rpy` compose screens and theme; `bloom_*` provide post‑processing shaders; `letterbox_gui.rpy` manages aspect fit.
- Debug/dev: `room_debug.rpy` and `info_overlay.rpy` expose helpers to jump and inspect state.

## Framework API (Drop‑in)
- Location: `api/room_api.rpy`, `api/ui_api.rpy`, `api/display_api.rpy`, `api/interactions_api.rpy`.
- Rooms: `load_room("room1")`, `save_room_changes()`, `move_object("lamp", 10, 0)`, `scale_object("lamp", 10)`.
- Display: `hide_object("door")`, `show_object("door")`, `set_default_background("images/room1.png")`.
- UI: `customize_exit_button(text="Back")`, `add_custom_button("help", {"text": "Help", "xpos": 40, "ypos": 20})`.
- Interactions: `show_interaction_menu("detective")`, `navigate_interaction_menu("down")`, `get_button_action(obj, data)`.
- Effects: `toggle_crt_effect()`, `set_crt_parameters(warp=.25, scan=.6)`.

## Quick Start Example
```renpy
label start:
    # Load a room and tweak UI
    $ load_room("room1")
    $ customize_exit_button(text="Back")

    # Show core screens
    show screen room_background_and_objects
    show screen room_ui_buttons
    show screen object_hotspots

    "Explore with mouse or gamepad."
```

## Interaction Menu Example
```renpy
label inspect_object:
    $ load_room("room1")
    show screen room_background_and_objects
    $ store.current_hover_object = "detective"
    $ show_interaction_menu("detective")
    "Use arrows/enter to navigate the menu."
```

## Build, Test, and Development Commands
- Set `RENPY_SDK` to your local SDK path (Ren'Py 8.4.2).
- Run (CLI from repo root): `$RENPY_SDK/renpy.sh .`
- Lint: `$RENPY_SDK/renpy.sh . lint` — static checks for script/style issues.
- Distribute: `$RENPY_SDK/renpy.sh . distribute` — build platform bundles.
- Launcher: Use the Ren'Py Launcher and open the project root (not `game/`).

## Coding Style & Naming Conventions
- Indentation: 4 spaces; no tabs. Keep lines reasonably short (~100 cols).
- Python: snake_case for variables/functions, UPPER_SNAKE for constants, CamelCase for classes.
- Ren'Py: label and screen names in snake_case; keep UI in `screens.rpy` and theme work in `gui.rpy`/`gui/`.
- File naming: group by feature (`room_*.rpy`, `bloom_*.rpy`, `*_config.rpy`). Prefer small, focused modules.
- Translations: wrap user‑visible strings for translation and update `tl/` accordingly.

## Testing Guidelines
- Static checks: run `./renpy.sh . lint` and fix all findings before PR.
- Manual flows: add a temporary jump in `script.rpy` or use helpers in `room_debug.rpy` to reach scenarios quickly. Do not commit temporary test labels.
- Visual/UI changes: attach screenshots or short clips to PRs.

## Commit & Pull Request Guidelines
- Commits: use imperative mood; Conventional Commits style is preferred.
  - Examples: `feat(room): add tile picker`, `fix(gui): correct textbox padding`, `refactor(bloom): simplify kernel setup`.
- PRs: include a clear description, linked issues, reproduction steps, and before/after visuals for UI changes. List any new assets and their licenses. Ensure `lint` passes and the project runs from the Launcher.

## Security & Configuration Tips
- Configuration lives in `options.rpy`, `config_builders.rpy`, and `*_config.rpy`. Avoid hard‑coding paths or secrets.
- Only include licensed assets; keep large unused binaries out of the repo.

## Assets & Licensing
- Location: art in `images/` and `gui/`, audio in `audio/`, fonts in `fonts/`.
- Naming: lowercase_with_underscores; avoid spaces and mixed case for portability.
- Formats: prefer PNG/WebP for images, OGG/MP3 for audio, TTF/OTF for fonts.
- Attribution: include license/attribution notes in PRs and, if applicable, reference in `libs/libs.txt`.
- Size control: avoid committing assets >10MB without prior discussion; remove unused files.

## Troubleshooting
- SDK not executable: `chmod +x "$RENPY_SDK/renpy.sh"`.
- Correct project path: run commands from the project root (not the `game/` folder).
- Clear caches: remove `game/cache/` and the project’s persistent data in `~/.renpy/<project_name>/` (close the game first).
- Lint failures: run the lint command above. Common issues are missing labels or asset paths; verify files exist under `images/`, `audio/`, and `gui/` with correct case.
- Assets not loading: paths are case‑sensitive on Linux; match file names exactly and prefer lowercase with underscores.
