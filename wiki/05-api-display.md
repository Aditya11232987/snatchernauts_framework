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
$ crt_warp = 0.2
$ crt_scan = 0.5
$ crt_chroma = 0.9
$ crt_scanline_size = 2.0
$ crt_animated = True
```

Bloom fade
```renpy
$ bloom_fade_in(room='room1', duration=1.0)
$ bloom_fade_out(duration=1.0)
```

Notes
- Defaults are set in `on_game_start()` to keep startup consistent.

