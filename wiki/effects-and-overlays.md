# Effects & Overlays

## CRT
- Toggle: press `c`.
- Parameters: set defaults in `game/script.rpy`; adjust live with keys `1–4` (scanline size).
- API: `toggle_crt_effect()`, `set_crt_parameters(warp, scan, chroma, scanline_size)`.

## Bloom
- Included via `room_bloom_effects` in `room_exploration`.
- Per-object bloom with presets (`core/bloom_colors.rpy`) and overrides in object configs.

## Letterbox
- Toggle: press `l`.
- Managed in `overlays/letterbox_gui.rpy`; UI buttons account for bar height.

## Info/Debug Overlays
- Info: press `i` or show `info_overlay_start` at launch.
- Debug: `overlays/debug_overlay.rpy` shows runtime info helpful during layout.
