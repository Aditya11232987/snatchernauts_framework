# API: Display / Effects

Module: `game/api/display_api.rpy`

Responsibilities
- Toggle letterbox overlay during exploration
- Toggle/configure CRT effect (warp/scan/chroma)
- Coordinate bloom fade in/out

Examples
```renpy
# Enable letterbox
$ show_letterbox(True)

# Tweak CRT at runtime
$ crt_enabled = True
$ crt_scanline_size = 2.0
```

Notes
- Defaults are set in `on_game_start()` to keep startup consistent.

