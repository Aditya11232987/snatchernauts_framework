# Main game script - clean entry point to room1

# Main entry point - fade out, then pixelate into room1
label start:
    # Install the enhanced shader system
    $ install_shader_system()
    
    # Global game start hook
    $ on_game_start()
    
    # Fade out from main menu to black over 2 seconds, hold for 0.5s
    scene black
    with Fade(2.0, 0.5, 0.0)
    
    # Load room1 data in background (invisible preparation)
    $ load_room("room1")
    $ on_room_enter("room1")
    
    # Start room1 music
    play music "audio/room1.mp3" loop
    
    # Show complete room screen with 2-second pixelate transition (14 levels for smoother effect)
    show screen room_exploration_shaders
    with Pixellate(2.0, 14)
    
    # Keep room active for user interaction
    $ renpy.pause(hard=True)
    
    return
