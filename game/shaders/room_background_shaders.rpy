# Room Background with Shader Integration
# Enhanced version of room_background_and_objects that applies shaders properly
# while maintaining compatibility with bloom and CRT systems

# Enhanced version of the room background and objects screen with shader support
screen room_background_and_objects_shaders():
    $ room_has_faded_in = getattr(store, 'room_has_faded_in', False)
    $ shader_transform_name = apply_room_shader_effects()
    $ shader_transform = renpy.store.__dict__.get(shader_transform_name, None) if shader_transform_name else None
    
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
            
            # Room background with optional shader
            if not room_has_faded_in:
                if shader_transform:
                    add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), shader_transform
                else:
                    add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
            else:
                if shader_transform:
                    add get_room_background() at room_no_fade(), shader_transform
                else:
                    add get_room_background() at room_no_fade()
            
            # Objects with optional shader (same as room for consistency)
            for obj_name, obj_data in room_objects.items():
                if should_display_object(obj_data) and not is_object_hidden(obj_data):
                    $ props = get_object_display_properties(obj_data)
                    $ obj_shader_name = get_shader_transform_for_object(obj_name, obj_data) or shader_transform_name
                    $ obj_shader = renpy.store.__dict__.get(obj_shader_name, None) if obj_shader_name else shader_transform
                    
                    if not room_has_faded_in:
                        if obj_shader:
                            add props["image"] at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), obj_shader:
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
                        if obj_shader:
                            add props["image"] at room_no_fade(), obj_shader:
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
            
            # Bloom effects applied on top of shader-affected content
            use room_bloom_effects_internal
    else:
        add get_fallback_background() at black_background()
        
        # Room background with optional shader
        if not room_has_faded_in:
            if shader_transform:
                add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), shader_transform
            else:
                add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
        else:
            if shader_transform:
                add get_room_background() at room_no_fade(), shader_transform
            else:
                add get_room_background() at room_no_fade()
        
        # Objects with optional shader (same as room for consistency)
        for obj_name, obj_data in room_objects.items():
            if should_display_object(obj_data) and not is_object_hidden(obj_data):
                $ props = get_object_display_properties(obj_data)
                $ obj_shader_name = get_shader_transform_for_object(obj_name, obj_data) or shader_transform_name
                $ obj_shader = renpy.store.__dict__.get(obj_shader_name, None) if obj_shader_name else shader_transform
                
                if not room_has_faded_in:
                    if obj_shader:
                        add props["image"] at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), obj_shader:
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
                    if obj_shader:
                        add props["image"] at room_no_fade(), obj_shader:
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
        
        # Bloom effects applied on top of shader-affected content
        use room_bloom_effects_internal

# Enhanced exploration screen with shader support
screen room_exploration_shaders():
    # Lock input until the initial fade completes
    $ input_locked = not room_has_faded_in
    
    # Room background and objects with shader support
    use room_background_and_objects_shaders
    use room_bloom_effects  # External bloom effects for compatibility
    
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
    
    # Add shader controls
    use shader_enhanced_controls
    
    # Handle pending dialogue scenes from interaction system (built into framework)
    if pending_dialogue_scene:
        $ scene_to_call = pending_dialogue_scene
        $ scene_args = pending_dialogue_args
        $ pending_dialogue_scene = None
        $ pending_dialogue_args = None
        # Trigger dialogue scene directly
        $ renpy.call_in_new_context(scene_to_call)
    
    # Existing keyboard navigation and remaining controls
    if (not input_locked) and interaction_menu_active:
        key "K_UP" action Function(navigate_interaction_menu, "up")
        key "K_DOWN" action Function(navigate_interaction_menu, "down")
        key "K_RETURN" action Function(execute_selected_action)
        key "K_ESCAPE" action Function(keyboard_cancel_action)
    
    # Prevent accidental entry into the game menu during exploration
    if not input_locked:
        key "game_menu" action NullAction()
    
    # EXISTING Global shortcuts (moved to avoid conflicts)
    if not input_locked:
        # Moved CRT toggle to Shift+P
        key "shift_K_p" action Function(toggle_crt_effect)
        
        # Keep existing audio control
        key "f" action Function(fade_out_room_audio)
        
        # Keep letterbox toggle
        key "l" action Function(toggle_letterbox)
        
        # Keep info overlay toggle
        key "i" action ToggleVariable("show_info_overlay")
        
        # Moved CRT animation to Alt+C
        key "alt_K_c" action Function(toggle_crt_animation)
    
    # Scanline size testing (unchanged)
    if not input_locked:
        key "1" action Function(set_crt_parameters, scanline_size=0.5)
        key "2" action Function(set_crt_parameters, scanline_size=1.0)
        key "3" action Function(set_crt_parameters, scanline_size=1.5)
        key "4" action Function(set_crt_parameters, scanline_size=3.0)
    
    # Vignette live tuning (unchanged)
    if not input_locked:
        key "[" action Function(adjust_vignette, delta_strength=-0.05)
        key "]" action Function(adjust_vignette, delta_strength=0.05)
        key "-" action Function(adjust_vignette, delta_width=-0.02)
        key "=" action Function(adjust_vignette, delta_width=0.02)
        key "0" action Function(adjust_vignette, set_strength=0.35, set_width=0.25)

# Helper function to install the enhanced shader system
init python:
    def install_shader_system():
        """
        Install the enhanced shader system by replacing the standard room exploration screen.
        Call this from your game script (e.g., at the start label).
        """
        global room_exploration, room_background_and_objects
        
        # First, hide any existing screens
        if renpy.get_screen("room_exploration"):
            renpy.hide_screen("room_exploration")
        
        # Replace the exploration screens with shader-enhanced versions
        room_exploration = renpy.display.screen.get_screen_variant("room_exploration_shaders")
        room_background_and_objects = renpy.display.screen.get_screen_variant("room_background_and_objects_shaders")
        
        renpy.notify("Enhanced shader system installed successfully!")
        
        # Fix any CRT toggle conflicts
        global toggle_crt_effect_original
        if not hasattr(store, 'toggle_crt_effect_original'):
            toggle_crt_effect_original = toggle_crt_effect
            
            def patched_toggle_crt(play_sound=True):
                """Patched version that doesn't conflict with shader hotkeys"""
                result = toggle_crt_effect_original(play_sound)
                renpy.notify("CRT effect: " + ("ON" if store.crt_enabled else "OFF"))
                return result
                
            store.toggle_crt_effect = patched_toggle_crt

# Example usage:
# label start:
#     $ install_shader_system()
#     jump game_start
