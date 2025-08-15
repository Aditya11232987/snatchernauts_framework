# Interactions API
# Object color, gradient backgrounds, and interaction/menu routines
#
# Overview
# - Builds and shows object interaction menus; executes selected actions.
# - Provides color extraction and gradient backgrounds for UI styling.
#
# Contracts
# - show_interaction_menu(obj_name)
# - hide_interaction_menu(...)
# - navigate_interaction_menu(direction)
# - execute_selected_action() -> calls execute_object_action
# - execute_object_action(obj_name, action_type)
#
# Integration
# - Before executing built-in side effects, emits on_object_interact(room,obj,action)

init python:
    def get_object_main_color(obj_name):
        """Extract main color from object's image or use fallback"""
        if obj_name not in store.room_objects:
            return "#ffffff"
        obj = store.room_objects[obj_name]
        image_path = obj.get("image", "")
        if image_path:
            # Since bloom is deprecated, use a simple color based on object type
            obj_type = obj.get("object_type", "item")
            if obj_type == "character":
                return "#4a90e2"  # Blue for characters
            elif obj_type == "item":
                return "#e2a04a"  # Orange for items
            else:
                return "#ffffff"  # White fallback
        return "#ffffff"
    
    def create_gradient_background(base_color, alpha=0.7):
        """Create a gradient background using the base color"""
        try:
            base_color = base_color.lstrip('#')
            if len(base_color) == 6:
                r, g, b = tuple(int(base_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                r, g, b = 255, 255, 255
            lighter_r = min(255, int(r * 1.3))
            lighter_g = min(255, int(g * 1.3))
            lighter_b = min(255, int(b * 1.3))
            darker_r = max(0, int(r * 0.7))
            darker_g = max(0, int(g * 0.7))
            darker_b = max(0, int(b * 0.7))
            from renpy.display.im import LinearGradient
            top_color = "#{:02x}{:02x}{:02x}{:02x}".format(lighter_r, lighter_g, lighter_b, int(255 * alpha))
            bottom_color = "#{:02x}{:02x}{:02x}{:02x}".format(darker_r, darker_g, darker_b, int(255 * alpha))
            return LinearGradient(top_color, bottom_color, 0, 0, 0, INTERACTION_BUTTON_CONFIG["height"])
        except:
            return base_color + "{:02x}".format(int(255 * alpha))

# Framework dialogue system - handles scene transitions from interaction hooks
default pending_dialogue_scene = None
default pending_dialogue_args = None

init python:
    def trigger_dialogue_scene(scene_label, args=None):
        """Framework function to safely trigger dialogue scenes from interaction hooks.
        
        This handles the complexity of transitioning from Python interaction context
        to Ren'Py script context for developers.
        
        Args:
            scene_label: The label name to call (e.g. "detective_talk_scene")
            args: Optional arguments to pass to the scene
        """
        store.pending_dialogue_scene = scene_label
        store.pending_dialogue_args = args
        log_debug("InteractionAPI", f"Dialogue scene '{scene_label}' queued for execution")
    
    def show_interaction_menu(obj_name):
        """Show interaction menu for the specified object"""
        global interaction_menu_active, interaction_target_object, interaction_selected_action
        if obj_name not in store.room_objects:
            return
        obj = store.room_objects[obj_name]
        obj_type = obj.get("object_type", "item")
        if obj_type not in INTERACTION_ACTIONS:
            renpy.notify(f"No interactions defined for {obj_type}")
            return
        interaction_menu_active = True
        interaction_target_object = obj_name
        interaction_selected_action = 0
        store.current_hover_object = obj_name
        try:
            actions = INTERACTION_ACTIONS.get(obj_type, [])
            labels = ", ".join(a.get("label", "?") for a in actions)
            log_main_event("INTERACTION", f"show defs for {obj_name} type={obj_type} actions=[{labels}]", scope="global")
        except Exception:
            pass
        renpy.restart_interaction()
    
    def hide_interaction_menu(keep_object_selected=False, target_object=None):
        """Hide the interaction menu and optionally keep object selected"""
        global interaction_menu_active, interaction_target_object, interaction_selected_action
        obj_to_keep = target_object or interaction_target_object
        interaction_menu_active = False
        interaction_target_object = None
        interaction_selected_action = 0
        if keep_object_selected and obj_to_keep:
            store.current_hover_object = obj_to_keep
            store.gamepad_selected_object = obj_to_keep
        else:
            store.current_hover_object = None
            store.gamepad_selected_object = None
        renpy.restart_interaction()
    
    def navigate_interaction_menu(direction):
        """Navigate through interaction menu options with gamepad"""
        global interaction_selected_action
        if not interaction_menu_active or not interaction_target_object:
            return
        obj = store.room_objects[interaction_target_object]
        obj_type = obj.get("object_type", "item")
        actions = INTERACTION_ACTIONS.get(obj_type, [])
        if direction == "up":
            renpy.sound.play("audio/ui/up.wav", channel="menu_nav")
            interaction_selected_action = (interaction_selected_action - 1) % len(actions)
        elif direction == "down":
            renpy.sound.play("audio/ui/down.wav", channel="menu_nav")
            interaction_selected_action = (interaction_selected_action + 1) % len(actions)
        renpy.restart_interaction()
    
    def execute_selected_action():
        """Execute the currently selected action"""
        if not interaction_menu_active or not interaction_target_object:
            return
        obj = store.room_objects[interaction_target_object]
        obj_type = obj.get("object_type", "item") 
        actions = INTERACTION_ACTIONS.get(obj_type, [])
        if interaction_selected_action < len(actions):
            action = actions[interaction_selected_action]
            try:
                log_main_event("INPUT", f"execute action {action['action']} on {interaction_target_object}", scope="keyboard")
            except Exception:
                pass
            execute_object_action(interaction_target_object, action["action"])
    def execute_object_action(obj_name, action_type):
        """Execute a specific action on an object"""
        previous_object = obj_name
        
        # For the "leave" action, keep object selected to maintain description box
        # For other actions, clear the hover object to hide description box after execution
        if action_type == "leave":
            hide_interaction_menu(keep_object_selected=True, target_object=obj_name)
        else:
            hide_interaction_menu(keep_object_selected=False, target_object=None)
        
        obj = store.room_objects[obj_name]
        obj_type = obj.get("object_type", "item") 
        # Notify game logic hooks before executing side effects
        handled = False
        try:
            result = on_object_interact(store.current_room_id, obj_name, action_type)
            handled = bool(result)
        except Exception:
            handled = False
        if handled:
            try:
                log_main_event("INTERACT", f"{action_type} on {obj_name} handled by room logic", scope="local")
            except Exception:
                pass
            return
        if action_type == "talk":
            handle_talk_action(obj_name)
        elif action_type == "ask_about":
            handle_ask_about_action(obj_name)
        elif action_type == "take":
            handle_take_action(obj_name)
        elif action_type == "investigate":
            handle_investigate_action(obj_name)
        elif action_type == "open":
            handle_open_action(obj_name)
        elif action_type == "knock":
            handle_knock_action(obj_name)
        elif action_type == "search":
            handle_search_action(obj_name)
        elif action_type == "leave":
            renpy.sound.play("audio/ui/cancel.wav", channel="menu_nav")
            try:
                log_main_event("INTERACT", f"leave menu on {obj_name}")
            except Exception:
                pass
        else:
            renpy.notify(f"Unknown action: {action_type}")
    
    def handle_talk_action(obj_name):
        obj = store.room_objects[obj_name]
        character_name = obj_name.replace("_", " ").title()
        narrate(f"You strike up a conversation with {character_name}.")
    
    def handle_ask_about_action(obj_name):
        obj = store.room_objects[obj_name]
        character_name = obj_name.replace("_", " ").title()
        narrate(f"What would you like to ask {character_name} about?")
    
    def handle_take_action(obj_name):
        narrate(f"You take the {obj_name.replace('_', ' ')}")
    
    def handle_investigate_action(obj_name):
        obj = store.room_objects[obj_name]
        narrate(f"You carefully investigate the {obj_name.replace('_', ' ')}: {obj.get('description', 'Nothing of interest.')}")
    
    def handle_open_action(obj_name):
        narrate(f"You open the {obj_name.replace('_', ' ')}")
    
    def handle_knock_action(obj_name):
        narrate(f"You knock on the {obj_name.replace('_', ' ')}")
    
    def handle_search_action(obj_name):
        narrate(f"You search the {obj_name.replace('_', ' ')}")
    
    def get_menu_base_position(obj_name):
        if obj_name not in store.room_objects:
            return 0, 0
        obj = store.room_objects[obj_name]
        menu_x = obj["x"] + obj["width"] - INTERACTION_BUTTON_CONFIG["width"] - 10
        menu_y = obj["y"] + (obj["height"] // 3)
        if menu_x < 10:
            menu_x = 10
        elif menu_x > config.screen_width - INTERACTION_BUTTON_CONFIG["width"] - 10:
            menu_x = config.screen_width - INTERACTION_BUTTON_CONFIG["width"] - 10
        if menu_y < 10:
            menu_y = 10
        return menu_x, menu_y

init python:
    def gamepad_activate_object():
        """Activate interaction menu for currently selected object (A button)"""
        if store.gamepad_selected_object and store.gamepad_selected_object in store.room_objects:
            show_interaction_menu(store.gamepad_selected_object)
    
    def gamepad_confirm_action():
        """Confirm selected action (A button when menu is active)"""
        if interaction_menu_active:
            renpy.sound.play("audio/ui/confirm.wav", channel="menu_nav")
            try:
                if interaction_target_object:
                    actions = INTERACTION_ACTIONS.get(store.room_objects[interaction_target_object].get("object_type", "item"), [])
                    if actions and 0 <= interaction_selected_action < len(actions):
                        log_main_event("INPUT", f"execute action {actions[interaction_selected_action]['action']} on {interaction_target_object}", scope="controller")
            except Exception:
                pass
            execute_selected_action()
        else:
            renpy.sound.play("audio/ui/confirm.wav", channel="menu_nav")
            try:
                if store.gamepad_selected_object:
                    log_main_event("INPUT", f"select {store.gamepad_selected_object}", scope="controller")
            except Exception:
                pass
            gamepad_activate_object()
    
    def gamepad_cancel_action():
        """Cancel current action (B button)"""
        if interaction_menu_active:
            renpy.sound.play("audio/ui/cancel.wav", channel="menu_nav")
            hide_interaction_menu(keep_object_selected=True, target_object=interaction_target_object)
    
    def keyboard_cancel_action():
        """Cancel current action (Escape key)"""
        if interaction_menu_active:
            renpy.sound.play("audio/ui/cancel.wav", channel="menu_nav")
            hide_interaction_menu(keep_object_selected=True, target_object=interaction_target_object)
    
    def mouse_leave_action(obj_name, action_type):
        """Handle Leave button click"""
        previous_object = obj_name
        hide_interaction_menu(keep_object_selected=True, target_object=obj_name)
        renpy.sound.play("audio/ui/cancel.wav", channel="menu_nav")
        try:
            log_main_event("INTERACT", f"leave menu on {obj_name}", scope="mouse")
        except Exception:
            pass
    
    def execute_object_action_from_mouse(obj_name, action_type):
        """Mouse-initiated action execution wrapper to tag input source"""
        try:
            log_main_event("INPUT", f"execute action {action_type} on {obj_name}", scope="mouse")
        except Exception:
            pass
        execute_object_action(obj_name, action_type)

    def get_button_action(obj_name, action_data):
        """Get the appropriate action function for a button based on action type"""
        if action_data["action"] == "leave":
            return Function(mouse_leave_action, obj_name, action_data["action"])
        else:
            return Function(execute_object_action_from_mouse, obj_name, action_data["action"])
