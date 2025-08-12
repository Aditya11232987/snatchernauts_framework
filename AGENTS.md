# Repository Guidelines

## Targets & Version
- Engine: Ren'Py 8.4.2.
- Platforms: Windows and Linux (x86_64) are required.

## Project Structure & Module Organization
- Root project opened by Ren'Py; main code under `game/`.
- Entry points: `game/script.rpy` (boot), `game/core/rooms/` (room runtime + config).
- Framework APIs: `game/api/` (room, UI, display, interactions).
- UI and assets: `game/ui/`, `game/gui/`, `game/images/`, `game/audio/`, `game/fonts/`.
- Effects and helpers: `game/shaders/`, `game/overlays/`, `game/debug/`, `game/libs/`.

## Build, Test, and Development Commands
- Set `RENPY_SDK` to your local Ren'Py 8.4.2 SDK path.
- Run game (from repo root): `$RENPY_SDK/renpy.sh .`
- Lint scripts: `$RENPY_SDK/renpy.sh . lint`
- Distribute builds (Win/Linux): `$RENPY_SDK/renpy.sh . distribute`
Notes: Outputs go to `dist/` with Windows and Linux packages.
Launcher build steps: Open project in Ren'Py Launcher → Build & Distribute → select Windows and Linux → Build; results appear in `dist/`.

## CI Builds & Artifacts
- CI builds Windows and Linux via Ren'Py distribute; lint must pass first.
- Artifacts: `dist/<project>-*-win/` and `dist/<project>-*-linux/` (zips/executables included).

## Room Startup Helpers
- `play_room(room, music=None)`: Unified entry. Example: `call play_room("room2", "audio/room2.ogg")`.
- `go(room, music=None)`: Shorthand alias. Example: `call go("room2")`.
- `dev_start_room(room="room1", music=None)`: Local testing helper. Example: `call dev_start_room("room3")`.

See also: `Wiki/Getting-Started.md` for newcomer-friendly steps, examples, and screenshot guidance.

## Coding Style & Naming Conventions
- Indentation: 4 spaces, no tabs; keep lines ≲100 chars.
- Python/Ren'Py: snake_case for functions/vars and labels; CamelCase for classes; UPPER_SNAKE for constants.
- Files: group by feature and role (e.g., `room_*.rpy`, `*_config.rpy`, `bloom_*.rpy`).
- Assets: lowercase_with_underscores; avoid spaces and case mismatches.

## Testing Guidelines
- Static checks: run lint before every PR and fix all findings.
- Manual flows: temporarily jump from `game/script.rpy` to target labels for verification; do not commit temporary test labels.
- Visual changes: attach screenshots or short clips to PRs; verify on a clean cache.
Example: clear cache with `rm -rf game/cache/` and relaunch.

## Commit & Pull Request Guidelines
- Commits: imperative mood; Conventional Commits preferred.
  - Examples: `feat(room): add tile picker`, `fix(gui): correct textbox padding)`.
- PRs: include purpose, linked issues, reproduction steps, and before/after visuals for UI changes. Note added assets and licenses. Ensure lint passes and the project runs.

## Security & Configuration Tips
- Keep configuration in `options.rpy`, `config_builders.rpy`, and `*_config.rpy`; avoid hard‑coded paths or secrets.
- Only include licensed assets; avoid committing binaries >10MB without discussion.
- If the SDK script isn’t executable: `chmod +x "$RENPY_SDK/renpy.sh"`.
