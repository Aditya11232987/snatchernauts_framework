# API: Room

Module: `game/api/room_api.rpy`

Responsibilities
- Load rooms and maintain current room id
- Register in‑room objects and their properties
- Provide navigation helpers for keyboard/gamepad selection

Common usage
```renpy
$ load_room('room1')
$ on_room_enter('room1')  # usually called by play_room()
```

Register objects (pattern)
```renpy
# Typically defined in room config or on room load
$ register_object('poster', hotspot=(x, y, w, h), actions=['Examine'])
$ register_object('door', hotspot=(... ), actions=['Examine', 'Open'])
```

Query selection
```renpy
$ obj = get_selected_object()
$ actions = get_actions_for(obj)
```

Tips
- Keep room ids simple (e.g., `room1`, `lobby`, `office`)
- Use per‑room logic to customize behavior without branching everywhere

