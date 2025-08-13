# Architecture

Flow
1) Launcher → `script.rpy` shows an info overlay, then calls `on_game_start()`.
2) Entry → `play_room()` loads the default room and starts the exploration screen.
3) Logic → Hooks in `game/logic/game_logic.rpy` (and per‑room handlers) respond to events.
4) UI → Screens in `game/ui/` render descriptions, object lists, and interaction menus.
5) Effects → `game/overlays/` and `game/shaders/` apply CRT/Bloom/Letterbox.

Key modules
- `game/api/room_api.rpy` — room loading, object registration, navigation
- `game/api/ui_api.rpy` — description boxes, tooltips, screens helpers
- `game/api/interactions_api.rpy` — actions, menus, and interaction flow
- `game/api/display_api.rpy` — effects toggles (CRT, letterbox, bloom)
- `game/core/options.rpy` — versioning and defaults
- `game/core/common_logging.rpy` — logging, print interception
- `game/core/rooms/room_config.rpy` — room configuration helper(s)

Data flow
- The exploration screen queries the current room, selection, and actions via APIs.
- Hover/selection changes trigger hooks; handlers may override default behavior.
- on_object_interact returns bool: True to signal the action has been fully handled.

## Sequence (Mermaid)
```mermaid
sequenceDiagram
  participant Launcher as Ren'Py Launcher
  participant Script as script.rpy
  participant Logic as game_logic.rpy
  participant Screen as room_exploration
  participant APIs as api/*.rpy

  Launcher->>Script: run project
  Script->>Script: show info overlay
  Script->>Logic: on_game_start()
  Script->>APIs: load_room(default_room)
  Script->>Screen: call screen room_exploration
  Screen->>APIs: query objects/actions
  Screen->>Logic: on_object_hover(room, obj)
  Screen->>Logic: on_object_interact(room, obj, action)
  Logic-->>Screen: bool (handled?)
```

## Components (Mermaid)
```mermaid
flowchart LR
  subgraph Core
    Options[core/options.rpy]
    Logging[core/common_logging.rpy]
  end
  subgraph APIs
    RoomAPI[api/room_api.rpy]
    UIAPI[api/ui_api.rpy]
    InteractAPI[api/interactions_api.rpy]
    DisplayAPI[api/display_api.rpy]
  end
  subgraph UI
    Screens[game/ui/*]
    Overlays[game/overlays/*]
    Shaders[game/shaders/*]
  end
  Logic[logic/game_logic.rpy]
  Rooms[logic/rooms/*]

  Options --> Logging
  Core --> APIs
  RoomAPI --> Screens
  UIAPI --> Screens
  InteractAPI --> Screens
  DisplayAPI --> Overlays
  Logic --> APIs
  Rooms --> Logic
```

