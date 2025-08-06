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
    # Room background and objects on the same layer
    use room_background_and_objects
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
    
    # Keyboard shortcuts for new features (always available)
    key "c" action Function(toggle_crt_effect)
    key "f" action Function(fade_out_room_audio)
    key "r" action Function(renpy.restart_interaction)  # Refresh/restart interaction
    
    # Scanline size testing shortcuts
    key "1" action Function(set_crt_parameters, scanline_size=0.5)   # Fine scanlines
    key "2" action Function(set_crt_parameters, scanline_size=1.0)   # Normal scanlines
    key "3" action Function(set_crt_parameters, scanline_size=1.5)   # Thick scanlines
    key "4" action Function(set_crt_parameters, scanline_size=3.0)   # Very thick scanlines

# Initialize CRT variables with your specified defaults
init python:
    # Force these values every time (override any saved values)
    store.crt_enabled = True
    store.crt_warp = 0.2
    store.crt_scan = 0.5
    store.crt_chroma = 0.9
    store.crt_scanline_size = 1.0  # Your preferred scanline size (same as key '2')
    
    print(f"CRT defaults initialized - scanline_size: {store.crt_scanline_size}")
    
    
# Label to start room exploration
label explore_room:
    scene black with fade
    "You step into a mysterious room..."
    
    # Reset fade state so room can fade in properly
    $ store.room_faded_in = False
    
    # Ensure CRT parameters are set to defaults
    $ store.crt_enabled = True
    $ store.crt_warp = 0.2
    $ store.crt_scan = 0.5
    $ store.crt_chroma = 0.9
    $ store.crt_scanline_size = 1.0
    
    # Apply the CRT parameters using the function
    $ set_crt_parameters(warp=store.crt_warp, scan=store.crt_scan, chroma=store.crt_chroma, scanline_size=store.crt_scanline_size)
    
    # Ensure room1 is loaded
    $ load_room("room1")
    
    # Start music at 0 volume and begin playing immediately
    $ renpy.music.set_volume(0.0, channel="music")
    play music "audio/room1.mp3" loop
    
    # Start volume tween immediately to sync with visual fade-in (2 second duration)
    $ renpy.music.set_volume(1.0, delay=2.0, channel="music")
    
    call screen room_exploration
    
    # Fade out audio when leaving
    stop music fadeout 2.0
    "You step back, having examined the room thoroughly."
    return
