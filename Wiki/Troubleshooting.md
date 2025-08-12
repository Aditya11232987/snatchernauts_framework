# Troubleshooting

- SDK script not executable: `chmod +x "$RENPY_SDK/renpy.sh"`.
- Wrong project opened: choose the repo root, not `game/`.
- Visuals not updating: clear `game/cache/` and relaunch.
- Paths case-sensitive on Linux: ensure filenames match exactly.
- Interaction menu missing: verify `object_type` has actions and `show_interaction_menu(obj)` is called by the hotspot.
