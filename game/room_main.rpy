# Room Exploration System - Main File
# Point-and-click interface with hover effects and floating descriptions
#
# INSTRUCTIONS: To modify objects, edit room_config.rpy

# Include the separated files
include "room_config.rpy"
include "room_transforms.rpy"
include "room_functions.rpy"
include "room_editor.rpy"
include "bloom_shader.rpy"
include "room_debug.rpy"
include "room_descriptions.rpy"
include "room_ui.rpy"
include "room_display.rpy"

# Screen for the room exploration - Now fully modular
screen room_exploration():
    # Room background and objects
    use room_background
    use room_objects
    use room_bloom_effects
    
    # Interactive elements
    use object_hotspots
    
    # Description system - show floating descriptions on hover
    if current_hover_object:
        $ obj = room_objects[current_hover_object]
        $ box_width, box_height = calculate_description_box_size(obj["description"])
        $ position_setting = obj.get("box_position", "auto")
        $ box_x, box_y, box_position = calculate_box_position(obj, box_width, box_height, position_setting)
        $ float_intensity = obj.get("float_intensity", 1.0)
        
        use floating_description_box(obj, box_width, box_height, box_x, box_y, float_intensity)
    
    # UI and debug
    use room_ui_buttons
    use debug_overlay
    
    # Gamepad controls for object navigation
    if gamepad_navigation_enabled:
        # Object navigation controls
        key "pad_dpleft_press" action Function(gamepad_navigate, "left")
        key "pad_dpright_press" action Function(gamepad_navigate, "right")
        key "pad_dpup_press" action Function(gamepad_navigate, "up")
        key "pad_dpdown_press" action Function(gamepad_navigate, "down")
        
        # Alternative gamepad controls (left stick)
        key "pad_leftx_neg" action Function(gamepad_navigate, "left")
        key "pad_leftx_pos" action Function(gamepad_navigate, "right")
        key "pad_lefty_neg" action Function(gamepad_navigate, "up")
        key "pad_lefty_pos" action Function(gamepad_navigate, "down")
        
        # Select first object if none selected
        key "pad_a_press" action Function(gamepad_select_first_object)
        
        # Toggle gamepad navigation (always available)
        key "pad_back_press" action Function(toggle_gamepad_navigation)

# Label to start room exploration
label explore_room:
    scene black with fade
    "You step into a mysterious room..."
    
    # Ensure room1 is loaded
    $ load_room("room1")
    
    call screen room_exploration
    
    "You step back, having examined the room thoroughly."
    return
