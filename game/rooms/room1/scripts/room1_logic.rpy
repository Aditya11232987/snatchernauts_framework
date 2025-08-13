# Room1 Logic (enhanced)
# Demonstrates detective interaction system with dialogue cutscenes

# Detective conversation state tracking
default detective_talked_to = False
default detective_ask_about_available = False
default detective_conversation_stage = 0

# Character definitions for dialogue
define detective_char = Character("Detective Blake", color="#4a90e2")
define player_char = Character("You", color="#e2a04a")

init -1 python:
    class Room1Logic:
        """Room-specific logic for room1.

        Enhanced with detective dialogue system and dynamic interaction options.
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

            # Update detective interaction options based on conversation progress
            self.update_detective_interactions()

        def on_object_hover(self, room_id: str, obj_name: str) -> None:
            # Keep hover side effects light to avoid spam.
            return

        def update_detective_interactions(self):
            """Dynamically update detective interaction options based on story progress"""
            try:
                # Get current detective actions
                current_actions = INTERACTION_ACTIONS.get("character", [])
                new_actions = []
                
                # Always include Talk option
                new_actions.append({"label": "Talk", "action": "talk"})
                
                # Add Ask About option only after first conversation
                if store.detective_ask_about_available:
                    new_actions.append({"label": "Ask About", "action": "ask_about"})
                
                # Always include Leave
                new_actions.append({"label": "Leave", "action": "leave"})
                
                # Update the global interaction actions
                INTERACTION_ACTIONS["character"] = new_actions
            except Exception as e:
                # Fallback to default if there's an error
                pass

        def on_object_interact(self, room_id: str, obj_name: str, action_id: str) -> bool:
            """Handle per-object actions for room1.

            Called BEFORE built-in side-effects in the interaction system.
            Return True to indicate the action was handled and defaults should be skipped.
            """
            print(f"[Room1Logic] on_object_interact called: room={room_id}, obj={obj_name}, action={action_id}")
            # Handle detective interactions
            if obj_name == 'detective':
                if action_id == 'talk':
                    log_debug("Room1Logic", "Talk action selected; starting detective dialogue directly")
                    # Clear UI state first to prevent stack conflicts
                    renpy.scene(layer="transient")
                    renpy.hide_screen("interaction_menu")
                    store.interaction_menu_active = False
                    store.interaction_target_object = None
                    store.current_hover_object = None
                    # Call dialogue scene directly after UI is cleared
                    renpy.call_in_new_context("detective_talk_scene")
                    return True
                elif action_id == 'ask_about':
                    if store.detective_ask_about_available:
                        log_debug("Room1Logic", "Ask About selected; calling detective_ask_about_scene")
                        renpy.call("detective_ask_about_scene")
                    else:
                        narrate("You should talk to the detective first.")
                    return True
            
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

            return False

    # Register the handler for room1 (fail fast if registration has issues)
    try:
        room1_handler = Room1Logic()
        register_room_logic('room1', room1_handler)
        print(f"[Room1Logic] Successfully registered Room1Logic handler")
    except Exception as e:
        print(f"[Room1Logic] Failed to register Room1Logic handler: {e}")
