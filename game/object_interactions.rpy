################################################################################
## Object Interaction System
################################################################################
##
## This file contains the interaction system for objects in the room.
## When A is pressed on an object, context-sensitive action buttons appear.
##

init offset = -1

## Interaction Configuration
################################################################################

## Whether interaction menu is currently active
default interaction_menu_active = False
default interaction_target_object = None
default interaction_selected_action = 0

## Action definitions by object type
define INTERACTION_ACTIONS = {
    "character": [
        {"label": "Talk", "action": "talk"},
        {"label": "Ask About", "action": "ask_about"}, 
        {"label": "Leave", "action": "leave"}
    ],
    "item": [
        {"label": "Examine", "action": "examine"},
        {"label": "Take", "action": "take"},
        {"label": "Use", "action": "use"},
        {"label": "Leave", "action": "leave"}
    ],
    "door": [
        {"label": "Open", "action": "open"},
        {"label": "Knock", "action": "knock"},
        {"label": "Leave", "action": "leave"}
    ],
    "container": [
        {"label": "Open", "action": "open"},
        {"label": "Search", "action": "search"},
        {"label": "Leave", "action": "leave"}
    ]
}

## Button styling with curved frames
define INTERACTION_BUTTON_CONFIG = {
    "width": 120,
    "height": 35,
    "spacing": 5,
    "background_frame": "curved_box_small.png",
    "border_size": 15,
    "background_normal": "#333333dd",
    "background_hover": "#555555dd", 
    "background_selected": "#777777dd",
    "text_color": "#ffffff",
    "text_hover_color": "#ffff00",
    "text_selected_color": "#00ff00",
    "text_size": 14,
    "padding": (8, 6)
}

################################################################################
## Interaction Functions
################################################################################

init python:
    def show_interaction_menu(obj_name):
        """Show interaction menu for the specified object"""
        global interaction_menu_active, interaction_target_object, interaction_selected_action
        
        if obj_name not in store.room_objects:
            return
            
        obj = store.room_objects[obj_name]
        obj_type = obj.get("object_type", "item")
        
        # Check if this object type has interactions defined
        if obj_type not in INTERACTION_ACTIONS:
            renpy.notify(f"No interactions defined for {obj_type}")
            return
            
        interaction_menu_active = True
        interaction_target_object = obj_name
        interaction_selected_action = 0  # Select first action
        
        # Keep the object hovered to maintain bloom effect
        store.current_hover_object = obj_name
        
        renpy.restart_interaction()
    
    def hide_interaction_menu():
        """Hide the interaction menu and reset all object states"""
        global interaction_menu_active, interaction_target_object, interaction_selected_action
        interaction_menu_active = False
        interaction_target_object = None
        interaction_selected_action = 0
        
        # Clear hover object to stop bloom effect when menu closes
        store.current_hover_object = None
        
        # Clear gamepad selection to reset hotspot selection
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
            interaction_selected_action = (interaction_selected_action - 1) % len(actions)
        elif direction == "down":
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
            execute_object_action(interaction_target_object, action["action"])
    
    def execute_object_action(obj_name, action_type):
        """Execute a specific action on an object"""
        hide_interaction_menu()
        
        obj = store.room_objects[obj_name]
        obj_type = obj.get("object_type", "item")
        
        # Handle different action types
        if action_type == "talk":
            handle_talk_action(obj_name)
        elif action_type == "ask_about":
            handle_ask_about_action(obj_name)
        elif action_type == "examine":
            handle_examine_action(obj_name)
        elif action_type == "take":
            handle_take_action(obj_name)
        elif action_type == "use":
            handle_use_action(obj_name)
        elif action_type == "open":
            handle_open_action(obj_name)
        elif action_type == "knock":
            handle_knock_action(obj_name)
        elif action_type == "search":
            handle_search_action(obj_name)
        elif action_type == "leave":
            # Just close the menu, already handled above
            pass
        else:
            renpy.notify(f"Unknown action: {action_type}")
    
    def handle_talk_action(obj_name):
        """Handle talking to a character"""
        obj = store.room_objects[obj_name]
        character_name = obj_name.replace("_", " ").title()
        renpy.notify(f"Starting conversation with {character_name}")
        # Here you would typically start a dialogue tree
        # For now, just show a message
        
    def handle_ask_about_action(obj_name):
        """Handle asking character about something"""
        obj = store.room_objects[obj_name]
        character_name = obj_name.replace("_", " ").title()
        renpy.notify(f"What would you like to ask {character_name} about?")
        # Here you would show a menu of topics to ask about
        
    def handle_examine_action(obj_name):
        """Handle examining an object"""
        obj = store.room_objects[obj_name]
        renpy.notify(f"Examining {obj_name.replace('_', ' ')}: {obj.get('description', 'Nothing special.')}")
        
    def handle_take_action(obj_name):
        """Handle taking an item"""
        renpy.notify(f"You take the {obj_name.replace('_', ' ')}")
        # Here you might add to inventory, remove from room, etc.
        
    def handle_use_action(obj_name):
        """Handle using an item"""
        renpy.notify(f"How would you like to use the {obj_name.replace('_', ' ')}?")
        
    def handle_open_action(obj_name):
        """Handle opening something"""
        renpy.notify(f"You open the {obj_name.replace('_', ' ')}")
        
    def handle_knock_action(obj_name):
        """Handle knocking on something"""
        renpy.notify(f"You knock on the {obj_name.replace('_', ' ')}")
        
    def handle_search_action(obj_name):
        """Handle searching something"""
        renpy.notify(f"You search the {obj_name.replace('_', ' ')}")

    def get_interaction_button_position(obj_name, button_index):
        """Calculate position for interaction buttons next to object"""
        if obj_name not in store.room_objects:
            return 0, 0
            
        obj = store.room_objects[obj_name]
        
        # Position buttons to the right of the object
        base_x = obj["x"] + obj["width"] + 20
        base_y = obj["y"] + (button_index * (INTERACTION_BUTTON_CONFIG["height"] + INTERACTION_BUTTON_CONFIG["spacing"]))
        
        # Make sure buttons don't go off screen
        max_x = config.screen_width - INTERACTION_BUTTON_CONFIG["width"] - 50
        max_y = config.screen_height - INTERACTION_BUTTON_CONFIG["height"] - 50
        
        # Adjust for letterbox if active
        if letterbox_active:
            max_y = max_y - letterbox_bar_height
            if base_y < letterbox_bar_height:
                base_y = letterbox_bar_height + 10
        
        button_x = min(base_x, max_x)
        button_y = min(base_y, max_y)
        
        return button_x, button_y

################################################################################
## Interaction Menu Screen
################################################################################

screen interaction_menu():
    # Put interaction menu above letterbox
    zorder 160
    
    if interaction_menu_active and interaction_target_object:
        $ obj = room_objects[interaction_target_object]
        $ obj_type = obj.get("object_type", "item")
        $ actions = INTERACTION_ACTIONS.get(obj_type, [])
        
        # Get float intensity from the target object (same as description boxes)
        $ float_intensity = obj.get("float_intensity", 1.0)
        
        for i, action_data in enumerate(actions):
            $ button_x, button_y = get_interaction_button_position(interaction_target_object, i)
            $ is_selected = (i == interaction_selected_action)
            
            # Use frame with curved background and floating animation
            if float_intensity > 0.0:
                frame at floating_bubble(float_intensity):
                    xpos button_x
                    ypos button_y
                    xsize INTERACTION_BUTTON_CONFIG["width"]
                    ysize INTERACTION_BUTTON_CONFIG["height"]
                    
                    # Create curved frame background with tint based on state
                    if is_selected:
                        background Frame(
                            Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix(INTERACTION_BUTTON_CONFIG["background_selected"])), 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            tile=False
                        )
                    else:
                        background Frame(
                            Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix(INTERACTION_BUTTON_CONFIG["background_normal"])), 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            tile=False
                        )
                        
                        hover_background Frame(
                            Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix(INTERACTION_BUTTON_CONFIG["background_hover"])), 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            tile=False
                        )
                    
                    padding INTERACTION_BUTTON_CONFIG["padding"]
                    
                    # Button with transparent background since frame handles the visuals
                    textbutton action_data["label"]:
                        background None
                        hover_background None
                        action Function(execute_object_action, interaction_target_object, action_data["action"])
                        
                        if is_selected:
                            text_color INTERACTION_BUTTON_CONFIG["text_selected_color"]
                        else:
                            text_color INTERACTION_BUTTON_CONFIG["text_color"]
                            text_hover_color INTERACTION_BUTTON_CONFIG["text_hover_color"]
                        
                        text_size INTERACTION_BUTTON_CONFIG["text_size"]
                        xalign 0.5
                        yalign 0.5
            else:
                # Static version (no floating) for objects with 0 float intensity
                frame at no_float:
                    xpos button_x
                    ypos button_y
                    xsize INTERACTION_BUTTON_CONFIG["width"]
                    ysize INTERACTION_BUTTON_CONFIG["height"]
                    
                    # Create curved frame background with tint based on state
                    if is_selected:
                        background Frame(
                            Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix(INTERACTION_BUTTON_CONFIG["background_selected"])), 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            tile=False
                        )
                    else:
                        background Frame(
                            Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix(INTERACTION_BUTTON_CONFIG["background_normal"])), 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            tile=False
                        )
                        
                        hover_background Frame(
                            Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix(INTERACTION_BUTTON_CONFIG["background_hover"])), 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            INTERACTION_BUTTON_CONFIG["border_size"], 
                            tile=False
                        )
                    
                    padding INTERACTION_BUTTON_CONFIG["padding"]
                    
                    # Button with transparent background since frame handles the visuals
                    textbutton action_data["label"]:
                        background None
                        hover_background None
                        action Function(execute_object_action, interaction_target_object, action_data["action"])
                        
                        if is_selected:
                            text_color INTERACTION_BUTTON_CONFIG["text_selected_color"]
                        else:
                            text_color INTERACTION_BUTTON_CONFIG["text_color"]
                            text_hover_color INTERACTION_BUTTON_CONFIG["text_hover_color"]
                        
                        text_size INTERACTION_BUTTON_CONFIG["text_size"]
                        xalign 0.5
                        yalign 0.5

################################################################################
## Enhanced Gamepad Functions
################################################################################

init python:
    def gamepad_activate_object():
        """Activate interaction menu for currently selected object (A button)"""
        if store.gamepad_selected_object and store.gamepad_selected_object in store.room_objects:
            show_interaction_menu(store.gamepad_selected_object)
    
    def gamepad_confirm_action():
        """Confirm selected action (A button when menu is active)"""
        if interaction_menu_active:
            execute_selected_action()
        else:
            gamepad_activate_object()
    
    def gamepad_cancel_action():
        """Cancel current action (B button)"""
        if interaction_menu_active:
            hide_interaction_menu()

## Initialize interaction menu screen
init python:
    config.overlay_screens.append("interaction_menu")
