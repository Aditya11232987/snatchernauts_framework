# Logic Hooks

Global hooks (in `game/logic/game_logic.rpy`)
- `on_game_start()` — called once after the startup overlay.
- `on_room_enter(room_id)` — called after `load_room(room)`.
- `on_object_hover(room_id, obj)` — selection or hover changed.
- `on_object_interact(room_id, obj, action) -> bool` — return True if you fully handled the action; the framework will then skip defaults.

Per‑room logic
- Create `game/logic/rooms/<room>_logic.rpy` and register your handler with `register_room_logic('<room>', Handler())`.
- Implement methods matching the global hooks if you want room‑specific logic.

Example
```renpy
init python:
    class Room1Logic:
        def on_room_enter(self, room):
            renpy.notify(f"Entered {room}")
        def on_object_interact(self, room, obj, action):
            if obj == 'poster' and action == 'Examine':
                renpy.say(None, "It's a retro poster.")
                return True  # prevent default
            return False

    register_room_logic('room1', Room1Logic())
```

