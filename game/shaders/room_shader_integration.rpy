# Room Shader Integration
# Integrates the advanced shader control system with the existing room exploration
#
# Overview
# - Patches existing room exploration screen
# - Adds shader application logic
# - Maintains compatibility with existing systems

init python:
    # Integration functions for existing room system
    def apply_room_shader_effects():
        """Apply shader effects to the current room background"""
        current_transform = get_room_shader_transform()
        
        if current_transform:
            if isinstance(current_transform, str) and current_transform != "none":
                # Apply preset atmosphere or investigation mode
                return current_transform
            elif isinstance(current_transform, tuple) and current_transform[0] == "custom":
                # Handle custom shader combinations
                return build_custom_room_transform(current_transform[1])
        
        return None
        
    def build_custom_room_transform(active_shaders):
        """Build a custom transform name for multiple active shaders"""
        # For now, use the first active shader as primary
        # In a full implementation, you'd create composite transforms
        if active_shaders:
            shader_name, preset_name = active_shaders[0]
            return f"{shader_name}_{preset_name}_effect"
        return None
        
    def get_shader_transform_for_object(obj_name, obj_data):
        """Get appropriate shader transform for a specific object"""
        # Check if this object should have special shader treatment
        room_transform = apply_room_shader_effects()
        
        # Some objects might need different shader treatment
        if obj_name == "evidence" and current_investigation_mode == 1:  # evidence_analysis_mode
            return "evidence_highlight_mode"
        elif obj_name == "suspect_photo" and current_investigation_mode == 2:  # suspect_tracking_mode
            return "suspect_tracking_mode"
        
        return room_transform

# Enhanced room background display with shader integration
screen room_background_and_objects_with_shaders():
    $ room_has_faded_in = getattr(store, 'room_has_faded_in', False)
    $ shader_transform = apply_room_shader_effects()
    
    if not room_has_faded_in:
        timer ROOM_DISPLAY_CONFIG["fade_duration"] action SetVariable('room_has_faded_in', True)

    if hasattr(store, 'crt_enabled') and store.crt_enabled:
        $ crt_warp = getattr(store, 'crt_warp', 0.2)
        $ crt_scan = getattr(store, 'crt_scan', 0.5)
        $ crt_chroma = getattr(store, 'crt_chroma', 0.9)
        $ crt_scanline_size = getattr(store, 'crt_scanline_size', 1.0)
        $ crt_vignette_strength = getattr(store, 'crt_vignette_strength', 0.35)
        $ crt_vignette_width = getattr(store, 'crt_vignette_width', 0.25)
        $ crt_animated = getattr(store, 'crt_animated', False)
        
        frame at (animated_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size, vignette_strength=crt_vignette_strength, vignette_width=crt_vignette_width) if crt_animated else static_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size, vignette_strength=crt_vignette_strength, vignette_width=crt_vignette_width)):
            background None
            add get_fallback_background() at black_background()
            
            # Apply shader transform to room background
            if not room_has_faded_in:
                if shader_transform:
                    add get_room_background() at Transform(room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), At(Null(), expression(shader_transform)))
                else:
                    add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
            else:
                if shader_transform:
                    add get_room_background() at Transform(room_no_fade(), At(Null(), expression(shader_transform)))
                else:
                    add get_room_background() at room_no_fade()
            
            # Apply shader transforms to objects
            for obj_name, obj_data in room_objects.items():
                if should_display_object(obj_data) and not is_object_hidden(obj_data):
                    $ props = get_object_display_properties(obj_data)
                    $ obj_shader_transform = get_shader_transform_for_object(obj_name, obj_data)
                    
                    if not room_has_faded_in:
                        if obj_shader_transform:
                            add props["image"] at Transform(room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), At(Null(), expression(obj_shader_transform))):
                                xpos props["xpos"]
                                ypos props["ypos"] 
                                xsize props["xsize"]
                                ysize props["ysize"]
                        else:
                            add props["image"] at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]):
                                xpos props["xpos"]
                                ypos props["ypos"]
                                xsize props["xsize"]
                                ysize props["ysize"]
                    else:
                        if obj_shader_transform:
                            add props["image"] at Transform(room_no_fade(), At(Null(), expression(obj_shader_transform))):
                                xpos props["xpos"]
                                ypos props["ypos"]
                                xsize props["xsize"] 
                                ysize props["ysize"]
                        else:
                            add props["image"] at room_no_fade():
                                xpos props["xpos"]
                                ypos props["ypos"]
                                xsize props["xsize"]
                                ysize props["ysize"]
                                
            use room_bloom_effects_internal
    else:
        # Non-CRT path with shader support
        add get_fallback_background() at black_background()
        
        if not room_has_faded_in:
            if shader_transform:
                add get_room_background() at Transform(room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), At(Null(), expression(shader_transform)))
            else:
                add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
        else:
            if shader_transform:
                add get_room_background() at Transform(room_no_fade(), At(Null(), expression(shader_transform)))
            else:
                add get_room_background() at room_no_fade()
        
        for obj_name, obj_data in room_objects.items():
            if should_display_object(obj_data) and not is_object_hidden(obj_data):
                $ props = get_object_display_properties(obj_data)
                $ obj_shader_transform = get_shader_transform_for_object(obj_name, obj_data)
                
                if not room_has_faded_in:
                    if obj_shader_transform:
                        add props["image"] at Transform(room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), At(Null(), expression(obj_shader_transform))):
                            xpos props["xpos"]
                            ypos props["ypos"]
                            xsize props["xsize"]
                            ysize props["ysize"]
                    else:
                        add props["image"] at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]):
                            xpos props["xpos"]
                            ypos props["ypos"]
                            xsize props["xsize"]
                            ysize props["ysize"]
                else:
                    if obj_shader_transform:
                        add props["image"] at Transform(room_no_fade(), At(Null(), expression(obj_shader_transform))):
                            xpos props["xpos"]
                            ypos props["ypos"]
                            xsize props["xsize"]
                            ysize props["ysize"]
                    else:
                        add props["image"] at room_no_fade():
                            xpos props["xpos"]
                            ypos props["ypos"]
                            xsize props["xsize"]
                            ysize props["ysize"]
        
        use room_bloom_effects_internal

# Enhanced room exploration screen with shader controls
screen room_exploration_with_shaders():
    # Lock input until the initial fade completes
    $ input_locked = not room_has_faded_in
    
    # Room background and objects with shader support
    use room_background_and_objects_with_shaders
    use room_bloom_effects

    # Interactive elements
    if not input_locked:
        use object_hotspots

    # Description system - show floating descriptions on hover
    if (not input_locked) and current_hover_object and not interaction_menu_active:
        $ obj = room_objects[current_hover_object]
        $ box_width, box_height = calculate_description_box_size(obj["description"])
        $ position_setting = obj.get("box_position", "auto")
        $ box_x, box_y, box_position = calculate_box_position(obj, box_width, box_height, position_setting)
        $ float_intensity = obj.get("float_intensity", 1.0)
        use floating_description_box(obj, box_width, box_height, box_x, box_y, float_intensity)

    # UI and debug overlays
    if not input_locked:
        use room_ui_buttons
    use info_overlay
    
    # ADD SHADER CONTROLS HERE
    use shader_enhanced_controls

    # Existing keyboard navigation for interaction menus
    if (not input_locked) and interaction_menu_active:
        key "K_UP" action Function(navigate_interaction_menu, "up")
        key "K_DOWN" action Function(navigate_interaction_menu, "down")
        key "K_RETURN" action Function(execute_selected_action)
        key "K_ESCAPE" action Function(keyboard_cancel_action)

    # Prevent accidental entry into the game menu (right click / Esc) during exploration
    if not input_locked:
        key "game_menu" action NullAction()

    # Existing gamepad controls
    if (not input_locked) and gamepad_navigation_enabled:
        if interaction_menu_active:
            key "pad_dpup_press" action Function(navigate_interaction_menu, "up")
            key "pad_dpdown_press" action Function(navigate_interaction_menu, "down")
            key "pad_lefty_neg" action Function(navigate_interaction_menu, "up")
            key "pad_lefty_pos" action Function(navigate_interaction_menu, "down")
        else:
            key "pad_dpleft_press" action Function(gamepad_navigate, "left")
            key "pad_dpright_press" action Function(gamepad_navigate, "right")
            key "pad_dpup_press" action Function(gamepad_navigate, "up")
            key "pad_dpdown_press" action Function(gamepad_navigate, "down")
            key "pad_leftx_neg" action Function(gamepad_navigate, "left")
            key "pad_leftx_pos" action Function(gamepad_navigate, "right")
            key "pad_lefty_neg" action Function(gamepad_navigate, "up")
            key "pad_lefty_pos" action Function(gamepad_navigate, "down")

        key "pad_a_press" action Function(gamepad_confirm_action)
        if interaction_menu_active:
            key "pad_b_press" action Function(gamepad_cancel_action)
        else:
            key "pad_b_press" action Function(gamepad_select_first_object)
        key "pad_back_press" action Function(toggle_gamepad_navigation)

    # EXISTING Global shortcuts (now updated to avoid conflicts)
    if not input_locked:
        # NOTE: 'c' was moved to Shift+C to avoid conflicts
        key "shift_K_c" action Function(toggle_crt_effect)  # Changed from 'c'
        key "f" action Function(fade_out_room_audio)  # Keep 'f' for audio fade
        key "l" action Function(toggle_letterbox)
        key "i" action ToggleVariable("show_info_overlay")
        # Toggle CRT scanline animation
        key "a" action Function(toggle_crt_animation)

    # Scanline size testing (keep existing)
    if not input_locked:
        key "1" action Function(set_crt_parameters, scanline_size=0.5)
        key "2" action Function(set_crt_parameters, scanline_size=1.0)
        key "3" action Function(set_crt_parameters, scanline_size=1.5)
        key "4" action Function(set_crt_parameters, scanline_size=3.0)

    # Vignette live tuning (keep existing)
    if not input_locked:
        key "[" action Function(adjust_vignette, delta_strength=-0.05)
        key "]" action Function(adjust_vignette, delta_strength=0.05)
        key "-" action Function(adjust_vignette, delta_width=-0.02)
        key "=" action Function(adjust_vignette, delta_width=0.02)
        key "0" action Function(adjust_vignette, set_strength=0.35, set_width=0.25)

# Automatic shader effect based on room context
init python:
    def auto_apply_room_shaders(room_name):
        """Automatically apply appropriate shader effects based on room type"""
        room_shader_mapping = {
            "crime_scene": 1,  # crime_scene_atmosphere  
            "alley": 8,        # alley_atmosphere
            "office": 7,       # office_atmosphere
            "warehouse": 6,    # warehouse_atmosphere
            "laboratory": 4,   # laboratory_atmosphere
            "interrogation": 5, # interrogation_room_atmosphere
            "street": 3,       # nighttime_street_atmosphere
            "abandoned": 2,    # abandoned_building_atmosphere
        }
        
        # Auto-set atmosphere based on room name
        global current_atmosphere_preset
        for keyword, preset_index in room_shader_mapping.items():
            if keyword in room_name.lower():
                current_atmosphere_preset = preset_index
                break
        else:
            current_atmosphere_preset = 0  # No preset
            
    def context_sensitive_shader_switch(context):
        """Switch shaders based on game context"""
        global current_investigation_mode, current_atmosphere_preset
        
        if context == "evidence_found":
            current_investigation_mode = 1  # evidence_analysis_mode
        elif context == "suspect_identified":
            current_investigation_mode = 2  # suspect_tracking_mode
        elif context == "flashback_sequence":
            current_investigation_mode = 3  # memory_flashback_mode
        elif context == "revelation":
            current_investigation_mode = 4  # revelation_moment_mode
        elif context == "normal_exploration":
            current_investigation_mode = 0  # back to normal
            
        renpy.restart_interaction()

# Example usage in your game script
label room_transition_example:
    # Auto-apply shaders when entering a room
    $ auto_apply_room_shaders("crime_scene_office")
    $ context_sensitive_shader_switch("normal_exploration")
    
    scene bg crime_scene
    "You enter the crime scene office..."
    
    # Later when evidence is found
    $ context_sensitive_shader_switch("evidence_found")
    "Something catches your eye - evidence!"
    
    return
