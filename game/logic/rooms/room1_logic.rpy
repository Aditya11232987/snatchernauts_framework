# Room1 Logic (example)
# Demonstrates how to keep per-room logic separate while calling public APIs.

init -1 python:
    class Room1Logic:
        """Example room-specific logic.

        Implement any subset of hooks used by game/logic/game_logic.rpy.
        """

        def on_room_enter(self, room_id: str) -> None:
            # Example: tweak CRT vignette for this room only.
            try:
                store.crt_vignette_strength = 0.95
                store.crt_vignette_width = 0.14
            except Exception:
                pass

        def on_object_hover(self, room_id: str, obj_name: str) -> None:
            # Example: could play a subtle sfx or adjust bloom when hovering.
            # Keep it very light to avoid spam during frequent hovers.
            pass

        def on_object_interact(self, room_id: str, obj_name: str, action_id: str) -> None:
            # Example: simple interaction branching
            if action_id == 'look':
                # Could trigger narration, change state, etc.
                pass

    # Register the handler for room1
    try:
        register_room_logic('room1', Room1Logic())
    except Exception:
        pass

