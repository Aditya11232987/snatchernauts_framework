# Room1 Logic (example)
# Demonstrates how to keep per-room logic separate while calling public APIs.

init -1 python:
    class Room1Logic:
        """Room-specific logic for room1.

        Implement any subset of hooks used by game/logic/game_logic.rpy.
        """

        def on_room_enter(self, room_id: str) -> None:
            # Example: tweak CRT vignette for this room only.
            try:
                store.crt_vignette_strength = 0.95
                store.crt_vignette_width = 0.14
            except Exception:
                pass

            # If 'patreon' was already taken, keep it hidden when re-entering.
            try:
                if getattr(persistent, 'room1_patreon_taken', False):
                    hide_object('patreon')
            except Exception:
                pass

        def on_object_hover(self, room_id: str, obj_name: str) -> None:
            # Keep hover side effects light to avoid spam.
            return

        def on_object_interact(self, room_id: str, obj_name: str, action_id: str) -> bool:
            """Handle per-object actions for room1.

            Called BEFORE built-in side-effects in the interaction system.
            Return True to indicate the action was handled and defaults should be skipped.
            """
            # Handle taking the 'patreon' item.
            if obj_name == 'patreon' and action_id == 'take':
                try:
                    # Persist and hide the object so it won't reappear.
                    persistent.room1_patreon_taken = True
                    hide_object('patreon')
                    narrate("You take the flyer and slip it into your coat.")
                    # Optional: give a quick toast to confirm hook fired.
                    show_hint(f"{room_id}: took 'patreon'")
                    try:
                        renpy.restart_interaction()
                    except Exception:
                        pass
                except Exception:
                    pass
                return True

            # Custom examine for the detective character.
            if obj_name == 'detective' and action_id == 'examine':
                try:
                    narrate("A seasoned detective with a thousand-yard stare.")
                except Exception:
                    pass
                return True

            # Generic room1 examine fallback (optional):
            if action_id == 'examine':
                try:
                    narrate("You take a closer look.")
                except Exception:
                    pass
                return True

            return False

    # Register the handler for room1 (fail fast if registration has issues)
    register_room_logic('room1', Room1Logic())
