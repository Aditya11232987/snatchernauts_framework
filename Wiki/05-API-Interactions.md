# API: Interactions

Module: `game/api/interactions_api.rpy`

Responsibilities
- Define the available actions for the selected object
- Present contextual menus (Examine, Use, Talk, etc.)
- Route the chosen action to logic hooks

Behavior
- `on_object_interact` returns bool. If True, defaults are skipped (you handled it).

Menu example
```renpy
# Screen (simplified):
screen object_actions(obj):
    vbox:
        for action in get_actions_for(obj):
            textbutton action action Function(execute_object_action, obj, action)
```

Hook routing
```renpy
init python:
    def execute_object_action(obj, action):
        room = current_room()
        handled = on_object_interact(room, obj, action)
        if not handled:
            default_handle(room, obj, action)
```

