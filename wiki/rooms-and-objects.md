# Rooms & Objects

## Define Rooms
Rooms live in `game/core/rooms/room_config.rpy` under `ROOM_DEFINITIONS`.

Minimal example:
```renpy
"room2": {
    "background": "images/room2.png",
    "objects": {
        "lamp": create_room_object(
            x=480, y=300,
            image="images/lamp.png",
            description="A rusty lamp.",
            scale_percent=100,
            box_position="right",
            bloom_overrides={"bloom_intensity": 0.6},
            animation_overrides={"hover_scale_boost": 1.03}
        )
    }
}
```

## Object Fields
- Position/size: `x`, `y`, `width`, `height`, `scale_percent`
- Visuals: `image`, `float_intensity`, `box_position`
- Effects: bloom config via `bloom_overrides` (see presets in `core/bloom_colors.rpy`)
- Animation: `animation_overrides` for hover scale/brightness
- Type: `object_type` (`character`, `item`, etc.) controls interactions

## Runtime Helpers (api/room_api.rpy)
- `load_room("room2")` — swap active room
- `move_object("lamp", 10, 0)` — nudge object
- `scale_object("lamp", +10)` — increase scale; use `"reset"` to restore
- `save_room_changes()` / `reset_room_changes()` — persist/revert layout tweaks
