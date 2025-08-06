# Room UI Controls System
# Buttons, hotspots, and interactive elements

# UI button configuration
define ROOM_BUTTON_CONFIG = {
    "exit": {
        "text": "Exit Room",
        "xpos": 1130,
        "ypos": 20,
        "text_color": "#ffffff",
        "text_hover_color": "#ffff00",
        "background": "#333333aa",
        "padding": {"horizontal": 15, "vertical": 8},
        "text_size": 16
    },
    "editor": {
        "text": "Editor Mode",
        "xpos": 950,
        "ypos": 20,
        "text_color": "#ffffff",
        "text_hover_color": "#00ff00",
        "background": "#333333aa",
        "padding": {"horizontal": 15, "vertical": 8},
        "text_size": 16
    }
}

init python:
    import time
    def create_object_hotspot(obj_name, obj_data):
        """Create hotspot configuration for an object"""
        return {
            "xpos": obj_data["x"],
            "ypos": obj_data["y"],
            "xsize": obj_data["width"],
            "ysize": obj_data["height"],
            "obj_name": obj_name
        }
    
    def get_all_object_hotspots():
        """Get hotspot configurations for all room objects"""
        hotspots = []
        for obj_name, obj_data in store.room_objects.items():
            hotspots.append(create_object_hotspot(obj_name, obj_data))
        return hotspots
    
    def get_room_exit_action():
        """Get the action for exiting the room"""
        return Return()
    
    def get_editor_mode_action():
        """Get the action for entering editor mode"""
        return [SetVariable("editor_mode", True), ShowMenu("object_editor")]
    
    def handle_object_hover(obj_name):
        """Handle object hover - only update if interaction menu is not active"""
        if not interaction_menu_active:
            store.current_hover_object = obj_name
            renpy.restart_interaction()
    
    def handle_object_unhover():
        """Handle object unhover - only update if interaction menu is not active"""
        if not interaction_menu_active:
            store.current_hover_object = None
            renpy.restart_interaction()

# Screen fragment for object hotspots
screen object_hotspots():
    # Interactive hotspots for objects
    for obj_name, obj_data in room_objects.items():
        button:
            xpos obj_data["x"]
            ypos obj_data["y"]
            xsize obj_data["width"]
            ysize obj_data["height"]
            background None
            action Function(show_interaction_menu, obj_name)
            hovered Function(handle_object_hover, obj_name)
            unhovered Function(handle_object_unhover)

# Screen fragment for UI buttons
screen room_ui_buttons():
    # Calculate letterbox offset for UI positioning
    $ letterbox_offset = 0
    if letterbox_active:
        $ letterbox_offset = letterbox_bar_height
    
    # Exit button in top right
    textbutton ROOM_BUTTON_CONFIG["exit"]["text"]:
        xpos ROOM_BUTTON_CONFIG["exit"]["xpos"]
        ypos letterbox_offset + ROOM_BUTTON_CONFIG["exit"]["ypos"]
        action get_room_exit_action()
        text_color ROOM_BUTTON_CONFIG["exit"]["text_color"]
        text_hover_color ROOM_BUTTON_CONFIG["exit"]["text_hover_color"]
        background ROOM_BUTTON_CONFIG["exit"]["background"]
        padding (
            ROOM_BUTTON_CONFIG["exit"]["padding"]["horizontal"],
            ROOM_BUTTON_CONFIG["exit"]["padding"]["vertical"]
        )
        text_size ROOM_BUTTON_CONFIG["exit"]["text_size"]
    
    # Editor mode button
    textbutton ROOM_BUTTON_CONFIG["editor"]["text"]:
        xpos ROOM_BUTTON_CONFIG["editor"]["xpos"]
        ypos letterbox_offset + ROOM_BUTTON_CONFIG["editor"]["ypos"]
        action get_editor_mode_action()
        text_color ROOM_BUTTON_CONFIG["editor"]["text_color"]
        text_hover_color ROOM_BUTTON_CONFIG["editor"]["text_hover_color"]
        background ROOM_BUTTON_CONFIG["editor"]["background"]
        padding (
            ROOM_BUTTON_CONFIG["editor"]["padding"]["horizontal"],
            ROOM_BUTTON_CONFIG["editor"]["padding"]["vertical"]
        )
        text_size ROOM_BUTTON_CONFIG["editor"]["text_size"]
    

# Utility functions for button customization
init python:
    def customize_exit_button(text=None, xpos=None, ypos=None, action=None):
        """Customize the exit button properties"""
        if text:
            ROOM_BUTTON_CONFIG["exit"]["text"] = text
        if xpos is not None:
            ROOM_BUTTON_CONFIG["exit"]["xpos"] = xpos
        if ypos is not None:
            ROOM_BUTTON_CONFIG["exit"]["ypos"] = ypos
        # Action can be customized via get_room_exit_action override
    
    def customize_editor_button(text=None, xpos=None, ypos=None, enabled=True):
        """Customize the editor button properties"""
        if text:
            ROOM_BUTTON_CONFIG["editor"]["text"] = text
        if xpos is not None:
            ROOM_BUTTON_CONFIG["editor"]["xpos"] = xpos
        if ypos is not None:
            ROOM_BUTTON_CONFIG["editor"]["ypos"] = ypos
        # Can be extended to disable editor button
    
    def add_custom_button(button_id, config):
        """Add a custom button to the room UI"""
        ROOM_BUTTON_CONFIG[button_id] = config
