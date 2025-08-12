# Room Debug Display System
# Debug information and development utilities

# Common utilities are loaded elsewhere in the project.

init python:
    def get_debug_mouse_text():
        """Get formatted mouse position text"""
        x, y = get_mouse_position()
        return "Mouse: ({}, {})".format(x, y)
    
    def get_debug_room_info():
        """Get current room debug information"""
        info = [
            "Current room: {}".format(store.current_room_id),
            "Background: {}".format(store.room_background)
        ]
        
        # Add bloom color info for hovered object
        if store.current_hover_object and store.current_hover_object in store.room_objects:
            obj_config = store.room_objects[store.current_hover_object]
            if obj_config.get("bloom_enabled", True):
                fallback_color = obj_config.get("bloom_color", "#ffffff")
                bloom_color = get_bloom_color(obj_config["image"], fallback_color)
                info.append("Bloom color ({}): {}".format(store.current_hover_object, bloom_color))
        
        return info

# Debug display styles
define DEBUG_TEXT_STYLE = {
    "color": "#ffffff",
    "size": 16
}

define DEBUG_POSITIONS = {
    "mouse": {"xpos": 10, "ypos": 10},
    "room_info": {"xpos": 10, "ypos_start": 30, "line_height": 20}
}

# Screen fragment for debug display (appears above letterbox)
screen debug_overlay():
    # Put debug info on a high z-order to appear above letterbox
    zorder 200
    
    if is_developer_mode():
        # Mouse coordinates (original position)
        text get_debug_mouse_text():
            xpos DEBUG_POSITIONS["mouse"]["xpos"]
            ypos DEBUG_POSITIONS["mouse"]["ypos"]
            color DEBUG_TEXT_STYLE["color"]
            size DEBUG_TEXT_STYLE["size"]
        
        # Room information - dynamically show all info lines (original position)
        $ room_info = get_debug_room_info()
        for i, info_line in enumerate(room_info):
            text info_line:
                xpos DEBUG_POSITIONS["room_info"]["xpos"]
                ypos DEBUG_POSITIONS["room_info"]["ypos_start"] + (i * DEBUG_POSITIONS["room_info"]["line_height"])
                color DEBUG_TEXT_STYLE["color"]
                size DEBUG_TEXT_STYLE["size"]
