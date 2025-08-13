# Game Logic Module
# Central place to write high-level game logic with clear hooks and docs.
#
# Overview
# - Provides lifecycle hooks you can implement per-room or globally.
# - Keeps logic in one place (this file) or in room files under game/logic/rooms/.
# - Uses the public APIs in game/api/* so internals stay decoupled.
#
# Quick Start
# 1) Add your logic in the global hooks below, or create a room handler in
#    game/logic/rooms/<room_id>_logic.rpy and register it.
# 2) Hooks currently supported:
#    - on_game_start()
#    - on_room_enter(room_id)
#    - on_object_hover(room_id, obj_name)
#    - on_object_interact(room_id, obj_name, action_id)
# 3) All hooks are optional: no-ops by default. Handlers may implement any.
#

init -1 python:
    # Type aliases for clarity (informal in Ren'Py runtime)
    from typing import Callable, Dict, Any

    # Registry for room-specific handlers.
    GAME_LOGIC_HANDLERS: Dict[str, Any] = {}

    def register_room_logic(room_id: str, handler: Any) -> None:
        """Register a per-room logic handler implementing any subset of hooks.

        A handler is any object with callables named like the hooks below:
        - on_room_enter(room_id)
        - on_object_hover(room_id, obj_name)
        - on_object_interact(room_id, obj_name, action_id)
        """
        GAME_LOGIC_HANDLERS[room_id] = handler

    # -------------------- Global Hooks (override here if desired) --------------------

    def on_game_start() -> None:
        """Called once at game start (after info overlay flow).

        Set global defaults, feature toggles, or analytics/logging here.
        Centralize CRT defaults so script.rpy stays a flow coordinator only.
        """
        try:
            store.crt_enabled = True
            store.crt_warp = 0.2
            store.crt_scan = 0.5
            store.crt_chroma = 0.9
            store.crt_scanline_size = 1.0
            store.crt_animated = True
            store.crt_vignette_strength = 0.95
            store.crt_vignette_width = 0.14
            # Apply parameters once so initial render uses the configured values.
            set_crt_parameters(
                warp=store.crt_warp,
                scan=store.crt_scan,
                chroma=store.crt_chroma,
                scanline_size=store.crt_scanline_size,
            )
        except Exception:
            pass

    def on_room_enter(room_id: str) -> None:
        """Called after a room is loaded (before entering exploration screen).

        Parameters
        - room_id: current room identifier (e.g., "room1").
        """
        handler = GAME_LOGIC_HANDLERS.get(room_id)
        if handler and hasattr(handler, 'on_room_enter'):
            try:
                handler.on_room_enter(room_id)
            except Exception as e:
                print(f"GameLogic error in on_room_enter: {e}")
        # Global cross-room logic can go here as well.
        # Example: auto-enable letterbox or set ambience volume.
        # show_letterbox()
        # EXAMPLE: Set a default hint when entering a specific room
        # if room_id == 'room1':
        #     show_hint("Use WASD/Arrows to navigate objects. Press A/Enter to interact.")

    def on_object_hover(room_id: str, obj_name: str) -> None:
        """Called when the cursor hovers over an object (not every frame).

        Useful for contextual tooltips, sfx, analytics, or dynamic bloom tweaks.
        """
        handler = GAME_LOGIC_HANDLERS.get(room_id)
        if handler and hasattr(handler, 'on_object_hover'):
            try:
                handler.on_object_hover(room_id, obj_name)
            except Exception as e:
                print(f"GameLogic error in on_object_hover: {e}")
        # EXAMPLE: Light reactions on hover (avoid spamming narration)
        # if obj_name == 'detective':
        #     # Subtle hint without blocking flow
        #     show_hint("They've seen things...")

    def on_object_interact(room_id: str, obj_name: str, action_id: str) -> None:
        """Called when the player triggers an interaction for an object.

        Parameters
        - room_id: current room
        - obj_name: object id (e.g., "lamp")
        - action_id: action identifier from your interaction menu (e.g., "look")
        """
        handler = GAME_LOGIC_HANDLERS.get(room_id)
        if handler and hasattr(handler, 'on_object_interact'):
            try:
                handler.on_object_interact(room_id, obj_name, action_id)
            except Exception as e:
                print(f"GameLogic error in on_object_interact: {e}")
        # EXAMPLES: Branch gameplay without touching UI code
        # if room_id == 'room1' and obj_name == 'detective' and action_id == 'examine':
        #     narrate("A seasoned detective with a thousand-yard stare.")
        #
        # if obj_name == 'patreon' and action_id == 'take':
        #     # Update state, change object visibility, etc.
        #     hide_object('patreon')
        #     narrate("You slip the flyer into your coat.")
        #
        # if action_id == 'open':
        #     # Adjust CRT or bloom for a mood change
        #     set_crt_parameters(warp=0.25, scan=0.6, chroma=0.95, scanline_size=1.0)
        #     show_hint("The room hums with electricity.")

    # -------------------- Integration helpers (documentation) --------------------

    # How to invoke hooks from elsewhere:
    # - on_room_enter is wired in script.rpy after calling load_room(room_id).
    # - on_object_hover/on_object_interact: call from existing UI handlers.
    #   For example, in ui_api.handle_object_hover you could add:
    #       on_object_hover(store.current_room_id, obj_name)
    #   And when executing an action in the interaction menu:
    #       on_object_interact(store.current_room_id, target_obj, action_id)
