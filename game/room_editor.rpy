# Global Room Editor
# Contains the live object editor screen - globally accessible

# GLOBAL REAL-TIME OBJECT EDITOR SCREEN
screen object_editor(room_id=None):
    modal True
    
    # Use specified room or current room
    $ editor_room_id = room_id if room_id else current_room_id
    $ editor_objects = get_room_objects(editor_room_id)
    $ editor_background = ROOM_DEFINITIONS[editor_room_id]["background"] if editor_room_id in ROOM_DEFINITIONS else "#222222"
    
    # Background
    add "#222222"
    if editor_background:
        add editor_background
    
    # Display all objects with selection highlight
    for obj_name, obj_data in editor_objects.items():
        if "image" in obj_data:
            add obj_data["image"]:
                xpos obj_data["x"]
                ypos obj_data["y"]
                xsize obj_data["width"]
                ysize obj_data["height"]
        
        # Highlight selected object with thick border
        if obj_name == selected_object:
            add Solid("#00ff00"):
                alpha 0.3
                xpos obj_data["x"]
                ypos obj_data["y"]
                xsize obj_data["width"]
                ysize obj_data["height"]
            
            # Thick green border for selected object
            frame:
                background None
                xpos obj_data["x"]
                ypos obj_data["y"]
                xsize obj_data["width"]
                ysize obj_data["height"]
                padding (0, 0)
                
                # Top border
                add Solid("#00ff00"):
                    xsize obj_data["width"]
                    ysize 4
                    ypos 0
                # Bottom border  
                add Solid("#00ff00"):
                    xsize obj_data["width"]
                    ysize 4
                    ypos obj_data["height"] - 4
                # Left border
                add Solid("#00ff00"):
                    xsize 4
                    ysize obj_data["height"]
                    xpos 0
                # Right border
                add Solid("#00ff00"):
                    xsize 4
                    ysize obj_data["height"]
                    xpos obj_data["width"] - 4
    
    # Help panel
    if show_editor_help:
        frame:
            xpos 20
            ypos 20
            background "#000000dd"
            padding (20, 15)
            
            vbox:
                text "🎮 GLOBAL OBJECT EDITOR" color "#00ff00" size 24
                text "Room: [editor_room_id]" color "#ffaa00" size 16
                if selected_object and selected_object in editor_objects:
                    text "Selected: [selected_object]" color "#ffff00" size 16
                    text "Position: ([editor_objects[selected_object]['x']], [editor_objects[selected_object]['y']])" color "#ffffff" size 16
                    text "Scale: [editor_objects[selected_object]['scale_percent']]% ([editor_objects[selected_object]['width']]x[editor_objects[selected_object]['height']]px)" color "#00ffaa" size 16
                else:
                    text "No object selected" color "#ff4444" size 16
                null height 10
                text "CONTROLS:" color "#ffaa00" size 16
                text "⬅➡⬆⬇ Arrow Keys: Move object" color "#ffffff" size 8
                text "WASD Keys: Move 1 pixel precisely" color "#ffff00" size 8
                text "Shift+Arrows: Move 10 pixels fast" color "#ffffff" size 8
                text "Q/E Keys: Scale object -5%/+5%" color "#ffffff" size 8
                text "Z/X Keys: Scale object -1%/+1% (precise)" color "#ffff00" size 8
                text "R Key: Reset object to 100% scale" color "#ffffff" size 8
                text "1-9 Keys: Select object by number" color "#ffffff" size 8
                text "+ / - Keys: Change move speed" color "#ffffff" size 8
                text "H: Toggle this help" color "#ffffff" size 8
                text "ESC: Exit editor" color "#ffffff" size 8
                null height 5
                if selected_object and selected_object in editor_objects:
                    text "Scale: [editor_objects[selected_object]['scale_percent']]%" color "#00ffaa" size 8
                text "Move speed: [move_speed] pixels" color "#cccccc" size 8
    
    # Room selector
    hbox:
        xpos 20
        ypos 540
        spacing 10
        
        text "Room:" color "#ffffff" size 16
        $ room_list = get_room_list()
        for room in room_list:
            textbutton room:
                action [Function(load_room, room), Return(), ShowMenu("object_editor", room)]
                text_size 16
                text_color ("#00ff00" if room == editor_room_id else "#ffffff")
                background ("#333333aa" if room == editor_room_id else "#222222aa")
                padding (8, 4)
    
    # Object selector buttons
    hbox:
        xpos 20
        ypos 580
        spacing 10
        
        $ obj_list = list(editor_objects.keys())
        for i, obj_name in enumerate(obj_list):
            textbutton "[i+1]: [obj_name]":
                action SetVariable("selected_object", obj_name)
                text_size 16
                text_color ("#00ff00" if obj_name == selected_object else "#ffffff")
                background ("#333333aa" if obj_name == selected_object else "#222222aa")
                padding (10, 5)
    
    # Save to File button - Permanently update room_config.rpy
    textbutton "💾 Save to File":
        xpos 520
        ypos 580
        action Function(update_room_config_file)
        text_color "#ffffff"
        text_hover_color "#00ff00"
        background "#333333aa"
        hover_background "#444444aa"
        padding (15, 8)
        text_size 16
    
    # Reset Changes button - Reset to original positions
    textbutton "🔄 Reset Room":
        xpos 670
        ypos 580
        action Function(reset_room_changes)
        text_color "#ffffff"
        text_hover_color "#ff8800"
        background "#333333aa"
        hover_background "#444444aa"
        padding (15, 8)
        text_size 16
    
    # Clear Persistent button - Remove persistent overrides only
    textbutton "🧹 Clear Persistent":
        xpos 820
        ypos 580
        action Function(clear_persistent_overrides)
        text_color "#ffffff"
        text_hover_color "#ff4444"
        background "#333333aa"
        hover_background "#444444aa"
        padding (15, 8)
        text_size 16
    
    # Exit editor button
    textbutton "❌ Exit Editor":
        xpos 1130
        ypos 20
        action [SetVariable("editor_mode", False), Return()]
        text_color "#ffffff"
        text_hover_color "#ff4444"
        background "#333333aa"
        padding (15, 8)
        text_size 16
    
    # KEYBOARD CONTROLS
    key "game_menu" action [SetVariable("editor_mode", False), Return()]  # ESC
    key "h" action ToggleVariable("show_editor_help")
    
    # Movement keys - Normal speed (uses move_speed setting)
    key "K_LEFT" action Function(move_object, selected_object, -move_speed, 0, editor_room_id)
    key "K_RIGHT" action Function(move_object, selected_object, move_speed, 0, editor_room_id)
    key "K_UP" action Function(move_object, selected_object, 0, -move_speed, editor_room_id)
    key "K_DOWN" action Function(move_object, selected_object, 0, move_speed, editor_room_id)
    
    # Pixel-precise movement - WASD keys (always 1 pixel)
    key "a" action Function(move_object, selected_object, -1, 0, editor_room_id)  # Left 1px
    key "d" action Function(move_object, selected_object, 1, 0, editor_room_id)   # Right 1px
    key "w" action Function(move_object, selected_object, 0, -1, editor_room_id)  # Up 1px
    key "s" action Function(move_object, selected_object, 0, 1, editor_room_id)   # Down 1px
    
    # Fast movement - Shift+Arrow keys (always 10 pixels)
    key "shift_K_LEFT" action Function(move_object, selected_object, -10, 0, editor_room_id)
    key "shift_K_RIGHT" action Function(move_object, selected_object, 10, 0, editor_room_id)
    key "shift_K_UP" action Function(move_object, selected_object, 0, -10, editor_room_id)
    key "shift_K_DOWN" action Function(move_object, selected_object, 0, 10, editor_room_id)
    
    # Scaling keys
    key "q" action Function(scale_object, selected_object, -5, editor_room_id)  # Scale smaller (5%)
    key "e" action Function(scale_object, selected_object, 5, editor_room_id)   # Scale larger (5%)
    key "z" action Function(scale_object, selected_object, -1, editor_room_id)  # Scale smaller (1% precise)
    key "x" action Function(scale_object, selected_object, 1, editor_room_id)   # Scale larger (1% precise)
    key "r" action Function(scale_object, selected_object, "reset", editor_room_id)  # Reset to 100%
    
    # Speed control
    key "K_PLUS" action SetVariable("move_speed", min(50, move_speed + 1))
    key "K_MINUS" action SetVariable("move_speed", max(1, move_speed - 1))
    key "K_EQUALS" action SetVariable("move_speed", min(50, move_speed + 1))  # + without shift
    
    # Object selection by number keys
    $ obj_list = list(room_objects.keys())
    if len(obj_list) > 0:
        key "K_1" action SetVariable("selected_object", obj_list[0])
    if len(obj_list) > 1:
        key "K_2" action SetVariable("selected_object", obj_list[1])
    if len(obj_list) > 2:
        key "K_3" action SetVariable("selected_object", obj_list[2])
    if len(obj_list) > 3:
        key "K_4" action SetVariable("selected_object", obj_list[3])
    if len(obj_list) > 4:
        key "K_5" action SetVariable("selected_object", obj_list[4])
    if len(obj_list) > 5:
        key "K_6" action SetVariable("selected_object", obj_list[5])
    if len(obj_list) > 6:
        key "K_7" action SetVariable("selected_object", obj_list[6])
    if len(obj_list) > 7:
        key "K_8" action SetVariable("selected_object", obj_list[7])
    if len(obj_list) > 8:
        key "K_9" action SetVariable("selected_object", obj_list[8])
