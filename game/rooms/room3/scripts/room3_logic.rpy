# Room3 Logic Template
# Customize this template for room3-specific interactions and behavior

# Room3 state tracking variables
default room3_visited = False
default room3_mystery_level = 0

init -1 python:
    class Room3Logic:
        """Room-specific logic for room3.
        
        Template class - customize with your room3 specific logic.
        """

        def on_room_enter(self, room_id: str) -> None:
            # Room3 specific setup when entering
            try:
                # Example: Darker, more mysterious atmosphere
                store.crt_vignette_strength = 1.0
                store.crt_vignette_width = 0.1
                
                # Per-room shader defaults (Room3): midnight chase grade + car headlights lighting + subtle grain
                try:
                    from renpy.store import shader_states
                    def _set(shader_name: str, preset_id: str):
                        state = shader_states.get(shader_name)
                        if not state:
                            return
                        presets = state.get("presets", [])
                        if preset_id in presets:
                            state["current"] = presets.index(preset_id)
                    _set('color_grading', 'midnight_chase')
                    _set('lighting', 'car_headlights')
                    _set('film_grain', 'subtle')
                    store.suppress_room_fade_once = True
                    renpy.restart_interaction()
                except Exception:
                    pass
                
                # Mark room as visited
                store.room3_visited = True
                
                print(f"[Room3Logic] Entered {room_id}")
                
            except Exception as e:
                print(f"[Room3Logic] Error on room enter: {e}")

        def on_object_hover(self, room_id: str, obj_name: str) -> None:
            # Room3 specific hover effects
            return

        def on_object_interact(self, room_id: str, obj_name: str, action_id: str) -> bool:
            """Handle per-object actions for room3."""
            
            # Add room3 specific interactions here
            
            return False

    # Register the handler for room3
    register_room_logic('room3', Room3Logic())
