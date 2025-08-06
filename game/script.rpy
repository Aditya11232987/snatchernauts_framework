# The script of the game goes in this file.

# Main entry point - calls the room exploration system
label start:
    "Welcome to the Interactive Room Explorer!"
    "This will display your room1.png as a point-and-click interface."
    
    "NOTE: You'll need to adjust the object coordinates in room_config.rpy"
    "to match the actual objects visible in your room1.png image."
    
    menu:
        "Explore the room":
            call explore_room
        "Explore with letterbox effect":
            $ show_letterbox()
            call explore_room
            $ hide_letterbox()
        "Exit":
            return
    
    "Thanks for exploring!"
    return
