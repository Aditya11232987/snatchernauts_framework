# Build & CI

## Local Builds
- Lint: `$RENPY_SDK/renpy.sh . lint`
- Distribute (Windows/Linux): `$RENPY_SDK/renpy.sh . distribute`
- Outputs: `dist/` contains Windows and Linux packages.
- Launcher: Build via Ren'Py Launcher → Build & Distribute.

## CI
- Lint gates distribute jobs.
- Artifacts published from `dist/<project>-*-win/` and `dist/<project>-*-linux/`.
- Clear cached `game/cache/` if assets move or paths change.
