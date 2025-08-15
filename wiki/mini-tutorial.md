# Mini Tutorial: Two-Room Demo

Goal: create a tiny game with two rooms, a custom exit button, and a simple flow.

## 1) Add assets
- Place images in `game/images/`:
  - `room2.png` (background)
  - `lamp.png` (object)

## 2) Define room2
Edit `game/core/rooms/room_config.rpy` and add under `ROOM_DEFINITIONS`:
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

## 3) Wire simple flow
In `game/script.rpy`, add a tiny story that hops rooms:
```renpy
label story_demo:
    "Welcome to Room 1."
    # Enter room1 and explore; use the Exit button when done
    call play_room("room1", "audio/room1.mp3")

    "Heading to Room 2…"
    # Enter room2; no music this time
    call play_room("room2")

    "Thanks for playing!"
    return
```
Then update `label start` to call it (or just `call story_demo`).

## 4) Customize Exit button (optional)
At the top of `label play_room` call sites or in an init block, customize UI:
```renpy
$ customize_exit_button(text="Leave", xpos=1130, ypos=20)
```

## 5) Run and build
- Run: `$RENPY_SDK/renpy.sh .`
- Distribute (Windows/Linux): `$RENPY_SDK/renpy.sh . distribute`.

Tip: If visuals don’t update, clear `game/cache/` and relaunch.
