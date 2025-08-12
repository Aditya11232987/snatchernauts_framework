# UI API
# Hotspot creation, hover handling, and button customization

init python:
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

