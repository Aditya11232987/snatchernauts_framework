# API: Interactions

Module: `game/api/interactions_api.rpy`

Responsibilities
- Define the available actions for the selected object
- Present contextual menus (Examine, Use, Talk, etc.)
- Route the chosen action to logic hooks

Behavior
- `on_object_interact` returns bool. If True, defaults are skipped (you handled it).

Example
```renpy
# In per-room logic
if obj == 'terminal' and action == 'Use':
    renpy.say(None, "You access the terminal.")
    return True
```

