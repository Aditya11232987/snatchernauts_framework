# The script of the game goes in this file.

# Defaults for unified room startup
default default_room = "room1"
default default_room_music = "audio/room1.mp3"

# Display/effects defaults (centralized)
default crt_enabled = True
default crt_warp = 0.2
default crt_scan = 0.5
default crt_chroma = 0.9
default crt_scanline_size = 1.0
default crt_animated = True
# CRT vignette defaults
default crt_vignette_strength = 0.95
default crt_vignette_width = 0.14
default bloom_fade_active = False
default bloom_fade_object = None
default bloom_fade_data = None
default bloom_fade_start_time = 0.0
default room_has_faded_in = False

# Unified entry to run the room exploration loop.
# Usage: call play_room("room1", "audio/room1.mp3")
label play_room(room=None, music=None):
    # Reset visual state
    $ store.room_faded_in = False

    # Ensure CRT parameters are set to defaults
    $ store.crt_enabled = True
    $ store.crt_warp = 0.2
    $ store.crt_scan = 0.5
    $ store.crt_chroma = 0.9
    $ store.crt_scanline_size = 1.0
    $ store.crt_animated = True
    $ store.crt_vignette_strength = 0.95
    $ store.crt_vignette_width = 0.14
    $ set_crt_parameters(warp=store.crt_warp, scan=store.crt_scan, chroma=store.crt_chroma, scanline_size=store.crt_scanline_size)

    # Resolve room and music
    if room is None:
        $ room = default_room
    $ load_room(room)

    if music is None:
        $ music = default_room_music
    if music:
        $ renpy.music.set_volume(0.0, channel="music")
        play music music loop
        $ renpy.music.set_volume(1.0, delay=2.0, channel="music")

    # Run the exploration screen
    call screen room_exploration

    # Teardown
    if music:
        stop music fadeout 2.0
    return

# Convenience alias for cleaner script calls
label go(room, music=None):
    $ default_room = room
    call play_room(room, music)
    return

# Main entry point - calls the room exploration system
label start:
    # Show the info overlay with continue button
    $ show_info_overlay = True
    $ show_continue_button = True
    
    # Show a simple background while displaying the overlay
    scene black
    
    # Call screen to show the info overlay with continue button
    call screen info_overlay_start
    
    # After clicking continue, hide the overlay and proceed to room
    $ show_info_overlay = False
    $ show_continue_button = False
    
    # Enter the default room using the unified entry
    call play_room from _call_play_room
    return

# Developer helper to jump straight into any room during local testing
label dev_start_room(room="room1", music=None):
    call play_room(room, music)
    return
