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
default previous_hover_action = 0


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
    "background_hover": "#663366dd",  # Dark red-purple
    "background_selected": "#663366dd",  # Dark red-purple for selected
    "text_color": "#ffffff",
    "text_hover_color": "#ffffff",  # White text on hover
    "text_selected_color": "#ffffff",  # White text when selected
    "text_size": 14,
    "padding": (8, 6)
}

init python:
    def get_object_main_color(obj_name):
        """Extract main color from object's image or use fallback"""
        if obj_name not in store.room_objects:
            return "#ffffff"
        
        obj = store.room_objects[obj_name]
        image_path = obj.get("image", "")
        
        if image_path:
            # Use the bloom color extraction system
            return get_bloom_color(image_path, "#ffffff")
        
        return "#ffffff"
    
    def create_gradient_background(base_color, alpha=0.7):
        """Create a gradient background using the base color"""
        try:
            # Convert hex to RGB
            base_color = base_color.lstrip('#')
            if len(base_color) == 6:
                r, g, b = tuple(int(base_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                r, g, b = 255, 255, 255
            
            # Create lighter version for gradient top
            lighter_r = min(255, int(r * 1.3))
            lighter_g = min(255, int(g * 1.3))
            lighter_b = min(255, int(b * 1.3))
            
            # Create darker version for gradient bottom  
            darker_r = max(0, int(r * 0.7))
            darker_g = max(0, int(g * 0.7))
            darker_b = max(0, int(b * 0.7))
            
            # Create gradient displayable
            from renpy.display.im import LinearGradient
            
            top_color = "#{:02x}{:02x}{:02x}{:02x}".format(lighter_r, lighter_g, lighter_b, int(255 * alpha))
            bottom_color = "#{:02x}{:02x}{:02x}{:02x}".format(darker_r, darker_g, darker_b, int(255 * alpha))
            
            return LinearGradient(top_color, bottom_color, 0, 0, 0, INTERACTION_BUTTON_CONFIG["height"])
            
        except:
            # Fallback to solid color
            return base_color + "{:02x}".format(int(255 * alpha))

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
        
        # Force complete screen refresh to fix initial positioning
        renpy.restart_interaction()
    
    def hide_interaction_menu(keep_object_selected=False, target_object=None):
        """Hide the interaction menu and optionally keep object selected"""
        global interaction_menu_active, interaction_target_object, interaction_selected_action
        
        # Store the target object before clearing it
        obj_to_keep = target_object or interaction_target_object
        
        interaction_menu_active = False
        interaction_target_object = None
        interaction_selected_action = 0
        
        if keep_object_selected and obj_to_keep:
            # Keep the object selected and show its description
            store.current_hover_object = obj_to_keep
            store.gamepad_selected_object = obj_to_keep
        else:
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
            renpy.sound.play("audio/ui/up.wav", channel="menu_nav")
            interaction_selected_action = (interaction_selected_action - 1) % len(actions)
        elif direction == "down":
            renpy.sound.play("audio/ui/down.wav", channel="menu_nav")
            interaction_selected_action = (interaction_selected_action + 1) % len(actions)
        
        # Force a complete screen refresh to reset button states
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
        # Store the object name to keep highlighted after action
        previous_object = obj_name
        
        # Hide the interaction menu but keep the object selected to show its description
        hide_interaction_menu(keep_object_selected=True, target_object=obj_name)
        
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
            renpy.sound.play("audio/ui/cancel.wav", channel="menu_nav")
            # For leave, we still want to keep the object selected and show description
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

    def get_menu_base_position(obj_name):
        """Get the base position for the entire interaction menu"""
        if obj_name not in store.room_objects:
            return 0, 0
            
        obj = store.room_objects[obj_name]
        
        # Position menu 10 pixels left of the object's right margin
        menu_x = obj["x"] + obj["width"] - INTERACTION_BUTTON_CONFIG["width"] - 10
        
        # Position menu in the upper middle of the object
        # Upper middle means about 1/3 down from the top of the object
        menu_y = obj["y"] + (obj["height"] // 3)
        
        # Keep menu on screen
        if menu_x < 10:
            menu_x = 10
        elif menu_x > config.screen_width - INTERACTION_BUTTON_CONFIG["width"] - 10:
            menu_x = config.screen_width - INTERACTION_BUTTON_CONFIG["width"] - 10
            
        if menu_y < 10:
            menu_y = 10
            
        return menu_x, menu_y

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
        
        # Get float intensity from the target object
        $ float_intensity = obj.get("float_intensity", 1.0)
        $ should_float = float_intensity > 0.0
        
        # Get base position for the entire menu
        $ menu_x, menu_y = get_menu_base_position(interaction_target_object)
        
        # Create menu container with floating animation
        if should_float:
            vbox at floating_bubble(float_intensity):
                xpos menu_x
                ypos menu_y
                spacing INTERACTION_BUTTON_CONFIG["spacing"]
                
                for i, action_data in enumerate(actions):
                    $ is_selected = (i == interaction_selected_action)
                    
                    frame:
                        xsize INTERACTION_BUTTON_CONFIG["width"]
                        ysize INTERACTION_BUTTON_CONFIG["height"]
                        
                        # Create curved frame background with tint based on state
                        if is_selected:
                            # Use pulsing cyan border as the main background for selected button
                            background Frame(
                                Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix("#00ffff")),
                                INTERACTION_BUTTON_CONFIG["border_size"],
                                INTERACTION_BUTTON_CONFIG["border_size"],
                                tile=False
                            ) at pulsing_border
                        else:
                            # Static background for non-selected buttons
                            background Frame(
                                Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix(INTERACTION_BUTTON_CONFIG["background_normal"])), 
                                INTERACTION_BUTTON_CONFIG["border_size"], 
                                INTERACTION_BUTTON_CONFIG["border_size"], 
                                tile=False
                            )
                            
                            # Hover background for non-selected buttons
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
                            # Use helper function to get appropriate action
                            action get_button_action(interaction_target_object, action_data)
                            
                            # Mouse interaction: update selection on hover with sound feedback
                            hovered [
                                Function(lambda i=i: renpy.sound.play(
                                    "audio/ui/down.wav" if i > previous_hover_action else "audio/ui/up.wav",
                                    channel="menu_nav"
                                )),
                                SetVariable("previous_hover_action", i),
                                SetVariable("interaction_selected_action", i),
                                Function(renpy.restart_interaction)
                            ]
                            unhovered NullAction()
                            
                            if is_selected:
                                text_color INTERACTION_BUTTON_CONFIG["text_selected_color"]
                            else:
                                text_color INTERACTION_BUTTON_CONFIG["text_color"]
                                text_hover_color INTERACTION_BUTTON_CONFIG["text_hover_color"]
                            
                            text_size INTERACTION_BUTTON_CONFIG["text_size"]
                            xalign 0.5
                            yalign 0.5
        else:
            vbox at no_float:
                xpos menu_x
                ypos menu_y
                spacing INTERACTION_BUTTON_CONFIG["spacing"]
                
                for i, action_data in enumerate(actions):
                    $ is_selected = (i == interaction_selected_action)
                    
                    frame:
                        xsize INTERACTION_BUTTON_CONFIG["width"]
                        ysize INTERACTION_BUTTON_CONFIG["height"]
                        
                        # Create curved frame background with tint based on state
                        if is_selected:
                            # Use pulsing cyan border as the main background for selected button
                            background Frame(
                                Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix("#00ffff")),
                                INTERACTION_BUTTON_CONFIG["border_size"],
                                INTERACTION_BUTTON_CONFIG["border_size"],
                                tile=False
                            ) at pulsing_border
                        else:
                            # Static background for non-selected buttons
                            background Frame(
                                Transform(INTERACTION_BUTTON_CONFIG["background_frame"], matrixcolor=TintMatrix(INTERACTION_BUTTON_CONFIG["background_normal"])), 
                                INTERACTION_BUTTON_CONFIG["border_size"], 
                                INTERACTION_BUTTON_CONFIG["border_size"], 
                                tile=False
                            )
                            
                            # Hover background for non-selected buttons
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
                            # Use helper function to get appropriate action
                            action get_button_action(interaction_target_object, action_data)
                            
                            # Mouse interaction: update selection on hover (optimized for responsiveness)
                            hovered [
                            Function(lambda i=i: renpy.sound.play(
                                "audio/ui/down.wav" if i > previous_hover_action else "audio/ui/up.wav",
                                channel="menu_nav"
                            )),
                            SetVariable("previous_hover_action", i),
                            SetVariable("interaction_selected_action", i),
                            Function(renpy.restart_interaction)
                            ]
                            unhovered NullAction()
                            
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
            renpy.sound.play("audio/ui/confirm.wav", channel="menu_nav")
            execute_selected_action()
        else:
            renpy.sound.play("audio/ui/confirm.wav", channel="menu_nav")
            gamepad_activate_object()
    
    def gamepad_cancel_action():
        """Cancel current action (B button)"""
        if interaction_menu_active:
            renpy.sound.play("audio/ui/cancel.wav", channel="menu_nav")
            # Keep the object selected and show its description, same as "Leave" button
            hide_interaction_menu(keep_object_selected=True, target_object=interaction_target_object)
    
    def keyboard_cancel_action():
        """Cancel current action (Escape key)"""
        if interaction_menu_active:
            renpy.sound.play("audio/ui/cancel.wav", channel="menu_nav")
            # Keep the object selected and show its description
            hide_interaction_menu(keep_object_selected=True, target_object=interaction_target_object)
    
    def mouse_leave_action(obj_name, action_type):
        """Handle Leave button click"""
        # Store the object name to keep highlighted after action
        previous_object = obj_name
        
        # Hide the interaction menu but keep the object selected
        hide_interaction_menu(keep_object_selected=True, target_object=obj_name)
        
        # Handle the leave action with sound
        renpy.sound.play("audio/ui/cancel.wav", channel="menu_nav")
    
    def get_button_action(obj_name, action_data):
        """Get the appropriate action function for a button based on action type"""
        if action_data["action"] == "leave":
            return Function(mouse_leave_action, obj_name, action_data["action"])
        else:
            return Function(execute_object_action, obj_name, action_data["action"])

## Initialize interaction menu screen
init python:
    config.overlay_screens.append("interaction_menu")
