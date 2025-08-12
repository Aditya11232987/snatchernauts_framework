# Room Configuration
# Contains all room object definitions and constants organized by room

# Utility modules loaded by Ren'Py script loader

# Object configuration templates to eliminate duplication
define DEFAULT_BLOOM_CONFIG = {
    "bloom_enabled": True,
    "bloom_intensity": 0.5,
    "bloom_radius": 8.0,
    "bloom_threshold": 0.03,
    "bloom_softness": 0.8,
    "bloom_alpha_min": 0.3,
    "bloom_alpha_max": 0.7,
    "bloom_pulse_speed": 1.0
}

define DEFAULT_ANIMATION_CONFIG = {
    "hover_animation_type": "breathe",
    "hover_scale_boost": 1.02,
    "hover_brightness_boost": 0.1
}

define DEFAULT_OBJECT_CONFIG = {
    "float_intensity": 0.5,
    "box_position": "auto"
}


# Room definitions organized by room ID
define ROOM_DEFINITIONS = {
    "room1": {
        "background": "images/room1.png",
        "objects": {
            "detective": merge_configs({
                # Basic object properties
                "x": 211, "y": 124, 
                "scale_percent": 100,
                "width": 328,   # calc_size("detective", 101)[0] = 328 pixels
                "height": 499,  # calc_size("detective", 101)[1] = 499 pixels
                "image": "images/detective.png",
                "description": "A mysterious detective figure. They seem to be investigating something important.",
                "box_position": "right",
                "float_intensity": 0.5,
                # Object type
                "object_type": "character",
            },
            # Custom bloom configuration (overrides defaults)
            create_bloom_config(
                BLOOM_PRESETS["neon_normal"]),
            # Custom animation configuration
            create_animation_config({
                "hover_scale_boost": 1.00,         # Slightly larger scale
                "hover_brightness_boost": 0.2      # Normal brightness boost
            })),

            
            "patreon": merge_configs({
                # Basic object properties
                "x": 690, "y": 167, 
                "scale_percent": 100,
                "width": 364,   # calc_size("patreon", 100)[0] = 364 pixels
                "height": 450,  # calc_size("patreon", 100)[1] = 450 pixels
                "image": "images/patreon.png",
                "description": "Another down on his luck fool drinking his last drink before contemplating his existence.",
                "box_position": "right+40",
                "float_intensity": 0.5,
                # Object type
                "object_type": "item",
            },
            # Custom bloom configuration (overrides defaults)
            create_bloom_config(
                BLOOM_PRESETS["neon_subtle"]),
            # Custom animation configuration
            create_animation_config({
                "hover_scale_boost": 1.00,         # Slightly larger scale
                "hover_brightness_boost": 0.0      # Normal brightness boost
            })),
            # You can add more objects here if you have more images
            # or create invisible hotspots for objects painted directly in room1.png
        }
    },
    # Add more rooms here:
    # "room2": {
    #     "background": "images/room2.png",
    #     "objects": {
    #         # Using the helper function for easy object creation:
    #         "new_object": create_room_object(
    #             x=100, y=200,
    #             image="images/object.png",
    #             description="Description here",
    #             scale_percent=100,
    #             box_position="auto",
    #             float_intensity=1.0,
    #             bloom_overrides={"bloom_intensity": 0.8},
    #             animation_overrides={"hover_scale_boost": 1.05}
    #         )
    #     }
    # }
}

# BOX POSITION OPTIONS:
# "top+30"    - Above object, 30px distance
# "bottom+50" - Below object, 50px distance  
# "left+25"   - Left of object, 25px distance
# "right+60"  - Right of object, 60px distance
# "auto"      - Let system choose best position (default if not specified)

# Global room interaction variables
default current_room_id = "room1"  # Currently active room
default current_hover_object = None
default speech_bubble_offset = 0.0

# Current room objects (dynamically set based on current_room_id)
default room_objects = {}
default room_background = ""

# GLOBAL EDITOR MODE VARIABLES
default editor_mode = False
default selected_object = None  # Currently selected object to move
default move_speed = 5  # Pixels to move per keypress
default show_editor_help = True

# GAMEPAD NAVIGATION VARIABLES
default gamepad_selected_object = None  # Currently highlighted object via gamepad
default gamepad_navigation_enabled = True  # Enable/disable gamepad navigation



# Load room1 by default
init 1 python:
    load_room("room1")
