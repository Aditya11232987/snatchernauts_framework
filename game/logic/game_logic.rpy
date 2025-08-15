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

init -2 python:
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
    
    def get_room_logic(room_id: str):
        """Get the room logic handler for a specific room.
        
        Returns the handler if found, None otherwise.
        """
        return GAME_LOGIC_HANDLERS.get(room_id)

    # -------------------- Global Hooks (override here if desired) --------------------
    def on_game_start() -> None:
        # Suppress CRT boot logs until we enter the first room
        try:
            store._suppress_crt_boot_logs = True
        except Exception:
            pass
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
            # Letterbox is now disabled by default and only shown during dialogue/cutscenes
            # No need to show letterbox during normal gameplay
        except Exception:
            pass

        # Log registered room handlers at startup for visibility
        try:
            keys = sorted(list(GAME_LOGIC_HANDLERS.keys()))
            msg = "Registered room handlers: " + (", ".join(keys) if keys else "(none)")
            print("[GameLogic] " + msg)
            try:
                renpy.notify(msg)
            except Exception:
                pass
        except Exception as e:
            print(f"[GameLogic] Error listing handlers: {e}")
            pass

    def on_room_enter(room_id: str) -> None:
        # Prepare initial frame suppression and enable CRT logs after first room enter
        try:
            store._initial_room_frame = True
        except Exception:
            pass
        # Enable CRT logs after first room enter to suppress noisy boot flips
        try:
            store._suppress_crt_boot_logs = False
        except Exception:
            pass
        
        # Ensure CRT is always enabled and animated during gameplay
        try:
            if not hasattr(store, '_crt_game_initialized'):
                store.crt_enabled = True
                store.crt_animated = True
                store._crt_game_initialized = True
                # Re-apply parameters so the shader picks up the state immediately
                set_crt_parameters(
                    warp=getattr(store, 'crt_warp', 0.2),
                    scan=getattr(store, 'crt_scan', 0.5),
                    chroma=getattr(store, 'crt_chroma', 0.9),
                    scanline_size=getattr(store, 'crt_scanline_size', 1.0),
                )
        except Exception:
            pass
        
        """Called after a room is loaded (before entering exploration screen).

        Parameters
        - room_id: current room identifier (e.g., "room1").
        """
        # Reset shaders before applying per-room defaults
        try:
            reset_all_shaders()
            store.suppress_room_fade_once = True
        except Exception as e:
            print(f"[GameLogic] Shader reset failed: {e}")
        
        handler = GAME_LOGIC_HANDLERS.get(room_id)
        if handler and hasattr(handler, 'on_room_enter'):
            try:
                handler.on_room_enter(room_id)
            except Exception as e:
                print(f"GameLogic error in on_room_enter: {e}")
        # Apply per-room default shader presets after reset
        try:
            from renpy.store import shader_states
            def _set(shader_name: str, preset_id: str):
                state = shader_states.get(shader_name)
                if not state:
                    return
                presets = state.get("presets", [])
                if preset_id in presets:
                    state["current"] = presets.index(preset_id)
            
            # Room-specific defaults with lighting parameters
            if room_id == 'room1':
                _set('color_grading', 'detective_office')
                _set('lighting', 'car_headlights')
                store.lighting_strength = 1.2
                store.lighting_animated = True
                store.lighting_anim_speed = 0.8
                store.lighting_anim_strength = 0.2
            elif room_id == 'room2':
                _set('color_grading', 'evidence_room')
                _set('lighting', 'window_blinds')
                store.lighting_strength = 0.9
                store.lighting_animated = False
                store.lighting_anim_speed = 0.3
                store.lighting_anim_strength = 0.1
            elif room_id == 'room3':
                _set('color_grading', 'midnight_chase')
                _set('lighting', 'car_headlights')
                store.lighting_strength = 1.5
                store.lighting_animated = True
                store.lighting_anim_speed = 1.2
                store.lighting_anim_strength = 0.25
        except Exception as e:
            print(f"[GameLogic] Shader preset apply failed: {e}")
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

    def on_object_interact(room_id: str, obj_name: str, action_id: str) -> bool:
        """Called when the player triggers an interaction for an object.

        Parameters
        - room_id: current room
        - obj_name: object id (e.g., "lamp")
        - action_id: action identifier from your interaction menu (e.g., "examine")

        Returns True if the interaction was fully handled and default behavior
        should be skipped; otherwise returns False.
        """
        handler = GAME_LOGIC_HANDLERS.get(room_id)
        if handler and hasattr(handler, 'on_object_interact'):
            try:
                rv = handler.on_object_interact(room_id, obj_name, action_id)
                return bool(rv)
            except Exception as e:
                print(f"GameLogic error in on_object_interact: {e}")
        # Not handled by room-specific logic
        return False
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
