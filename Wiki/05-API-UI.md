# API: UI

Module: `game/api/ui_api.rpy`

Responsibilities
- Show floating description boxes
- Drive composition screens for room exploration
- Provide small helpers for tooltips, prompts, confirmations

Examples
```renpy
# Show a confirmation before exiting
$ ui_confirm = True  # or call a helper if provided in this module
```

Notes
- The framework screens are under `game/ui/` — customize styles there.

