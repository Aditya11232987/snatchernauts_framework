# Examples

Minimal per‑room logic
```renpy
init python:
    class Room1Logic:
        def on_room_enter(self, room):
            renpy.notify("Welcome to Room 1")
        def on_object_interact(self, room, obj, action):
            if obj == 'door' and action == 'Examine':
                renpy.say(None, "A heavy steel door.")
                return True
            return False

    register_room_logic('room1', Room1Logic())
```

Programmatic effects
```renpy
$ show_letterbox(True)
$ crt_enabled = True
$ crt_scanline_size = 1.5
```

