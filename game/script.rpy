# The script of the game goes in this file.

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
    
    call explore_room from _call_explore_room
    return
