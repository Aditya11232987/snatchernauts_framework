# Room Display System
# Background and object rendering utilities

# Include common utilities
include "common_utils.rpy"

# Display configuration
define ROOM_DISPLAY_CONFIG = {
    "fallback_background_color": "#222222",
    "default_background": "images/room1.png"
}

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
    
    # Mouse position is now available via get_mouse_position() from common_utils

# Screen fragment for room background
screen room_background():
    # Fallback background color
    add get_fallback_background()
    
    # Room background image
    add get_room_background()

# Screen fragment for object display
screen room_objects():
    # Display object images
    for obj_name, obj_data in room_objects.items():
        if should_display_object(obj_data):
            $ props = get_object_display_properties(obj_data)
            add props["image"]:
                xpos props["xpos"]
                ypos props["ypos"]
                xsize props["xsize"]
                ysize props["ysize"]

# Screen fragment for bloom effects
screen room_bloom_effects():
    # Show enhanced matrix-based bloom for hovered objects
    if current_hover_object and current_hover_object in room_objects:
        $ bloom_data = apply_bloom_to_object(room_objects[current_hover_object], current_hover_object, current_hover_object)
        
        if bloom_data:
            # Debug: Log color being used
            if config.developer:
                $ print("Bloom color for {}: {}".format(current_hover_object, bloom_data["color"]))
            
            # Create enhanced matrix-based bloom effect using global utilities
            add bloom_data["image"] at configurable_bloom(
                bloom_data["parameters"]["bloom_alpha_min"], 
                bloom_data["parameters"]["bloom_alpha_max"], 
                1.0/bloom_data["parameters"]["bloom_pulse_speed"]
            ):
                xpos bloom_data["dimensions"]["x"]
                ypos bloom_data["dimensions"]["y"]
                xsize bloom_data["dimensions"]["width"]
                ysize bloom_data["dimensions"]["height"]
                # Apply enhanced bloom with color tinting and brightness
                matrixcolor TintMatrix(bloom_data["color"]) * BrightnessMatrix(bloom_data["parameters"]["bloom_intensity"])
                blur bloom_data["parameters"]["blur_amount"]
                alpha bloom_data["parameters"]["bloom_alpha_max"] * room_objects[current_hover_object].get("bloom_softness", 0.7)

# Utility functions for display customization
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
