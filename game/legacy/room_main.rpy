# Room Exploration System - Main File
# Point-and-click interface with hover effects and floating descriptions
#
# Overview
# - Legacy entry point. Prefer `label play_room` in game/script.rpy.
#
# INSTRUCTIONS: To modify objects, edit room_config.rpy

# Utility and API modules loaded by Ren'Py script loader

## Main exploration screen moved to ui/screens_room.rpy for easier editing

## Defaults moved to game/script.rpy for central configuration
    
    
# Label to start room exploration
label explore_room:
    # Backward-compatible entry; loads room1 and shows the room exploration screen
    $ load_room("room1")
    $ on_room_enter("room1")
    
    # Start room1 music
    play music "audio/room1.mp3" loop
    
    # Show room exploration screen
    show screen room_exploration_shaders
    $ renpy.pause(hard=True)
    return
