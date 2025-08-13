# Display API
# Background, object visibility, and display helpers
#
# Overview
# - Provides helpers to fetch backgrounds and determine object visibility.
# - Consumed by room composition screens and higher-level APIs.
#
# Contracts
# - get_room_background() -> str displayable path or color
# - get_fallback_background() -> color string
# - should_display_object(obj: dict) -> bool
# - get_object_display_properties(obj: dict) -> {image, xpos, ypos, xsize, ysize}
#
# Notes
# - Keep objects as plain dicts; this API translates them for UI screens.

init python:
    def get_room_background():
        """Get the current room background image"""
        if store.room_background:
            return store.room_background
        return ROOM_DISPLAY_CONFIG["default_background"]
    
    def get_fallback_background():
        """Get fallback background color"""
        return ROOM_DISPLAY_CONFIG["fallback_background_color"]
    
    def should_display_object(obj_data):
        """Check if an object should be displayed"""
        return "image" in obj_data
    
    def get_object_display_properties(obj_data):
        """Get display properties for an object"""
        return {
            "image": obj_data["image"],
            "xpos": obj_data["x"],
            "ypos": obj_data["y"],
            "xsize": obj_data["width"],
            "ysize": obj_data["height"]
        }

init python:
    def set_fallback_background_color(color):
        """Set the fallback background color"""
        ROOM_DISPLAY_CONFIG["fallback_background_color"] = color
    
    def set_default_background(image_path):
        """Set the default background image"""
        ROOM_DISPLAY_CONFIG["default_background"] = image_path
    
    def hide_object(obj_name):
        """Temporarily hide an object from display"""
        if obj_name in store.room_objects:
            store.room_objects[obj_name]["_hidden"] = True
    
    def show_object(obj_name):
        """Show a previously hidden object"""
        if obj_name in store.room_objects:
            store.room_objects[obj_name]["_hidden"] = False
    
    def is_object_hidden(obj_data):
        """Check if an object is hidden"""
        return obj_data.get("_hidden", False)
