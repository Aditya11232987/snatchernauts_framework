# Room2 Logic Template
# Customize this template for room2-specific interactions and behavior

# Room2 state tracking variables
default room2_visited = False
default room2_objects_discovered = 0
default room2_puzzle_solved = False

init -1 python:
    class Room2Logic:
        """Room-specific logic for room2.
        
        Template class - customize with your room2 specific logic.
        """

        def on_room_enter(self, room_id: str) -> None:
            # Room2 specific setup when entering
            try:
                # Example: Set specific CRT effects for room2
                store.crt_vignette_strength = 0.8
                store.crt_vignette_width = 0.2
                
                # Per-room shader defaults (Room2): evidence-room grade + window blinds lighting + subtle grain
                try:
                    from renpy.store import shader_states
                    def _set(shader_name: str, preset_id: str):
                        state = shader_states.get(shader_name)
                        if not state:
                            return
                        presets = state.get("presets", [])
                        if preset_id in presets:
                            state["current"] = presets.index(preset_id)
                    _set('color_grading', 'evidence_room')
                    _set('lighting', 'window_blinds')
                    _set('film_grain', 'subtle')
                    store.suppress_room_fade_once = True
                    renpy.restart_interaction()
                except Exception:
                    pass
                
                # Mark room as visited
                store.room2_visited = True
                
                # Room2 specific audio
                if hasattr(store, 'setup_room2_audio'):
                    setup_room2_audio()
                
                print(f"[Room2Logic] Entered {room_id}")
                
            except Exception as e:
                print(f"[Room2Logic] Error on room enter: {e}")

        def on_object_hover(self, room_id: str, obj_name: str) -> None:
            # Room2 specific hover effects
            return

        def on_object_interact(self, room_id: str, obj_name: str, action_id: str) -> bool:
            """Handle per-object actions for room2.

            Return True to indicate the action was handled and defaults should be skipped.
            """
            
            # Example room2 specific interactions
            if obj_name == 'example_object' and action_id == 'investigate':
                try:
                    narrate("You examine the mysterious object in room2...")
                    store.room2_objects_discovered += 1
                    return True
                except Exception:
                    pass
            
            # Add more room2 specific interactions here
            
            return False

    # Register the handler for room2
    register_room_logic('room2', Room2Logic())
