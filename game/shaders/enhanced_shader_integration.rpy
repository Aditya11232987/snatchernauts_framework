# Enhanced Shader Integration with Bloom Support
# Properly layers shaders between objects and CRT to work with bloom
#
# Overview
# - Properly layers: Background → Objects → Shaders → Bloom → CRT
# - Maintains compatibility with existing bloom system
# - Shaders affect both background and objects uniformly

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
        """Build a custom transform for multiple active shaders"""
        # Create composite transform name for complex combinations
        if active_shaders:
            shader_names = [f"{s[0]}_{s[1]}" for s in active_shaders[:3]]  # Limit to 3 for performance
            return "custom_" + "_".join(shader_names) + "_composite"
        return None
        
    def get_shader_transform_for_object(obj_name, obj_data):
        """Get appropriate shader transform for a specific object"""
        # Objects inherit room shader effects for consistency
        room_transform = apply_room_shader_effects()
        
        # Special cases for investigation modes that override room effects
        if current_investigation_mode == 1:  # evidence_analysis_mode
            if obj_name in ["evidence", "clue", "document", "photo"]:
                return "evidence_highlight_mode"
        elif current_investigation_mode == 2:  # suspect_tracking_mode
            if obj_name in ["suspect_photo", "person", "character"]:
                return "suspect_tracking_mode"
        elif current_investigation_mode == 4:  # revelation_moment_mode
            if "important" in obj_data.get("tags", []):
                return "revelation_moment_mode"
        
        # Otherwise use same shader as room for consistency
        return room_transform
        
    def should_apply_shader_to_bloom():
        """Determine if current shader effects should influence bloom"""
        # Some shaders enhance bloom, others might interfere
        shader_transform = apply_room_shader_effects()
        
        if shader_transform:
            # These shaders work well with bloom
            bloom_compatible = [
                "film_grain", "vintage_sepia", "atmospheric_fog", 
                "dynamic_lighting", "color_grading", "crime_scene_atmosphere",
                "alley_atmosphere", "nighttime_street_atmosphere"
            ]
            
            for compatible in bloom_compatible:
                if compatible in str(shader_transform):
                    return True
                    
        return False

# Enhanced room background display with shader integration and bloom support
screen room_background_and_objects_enhanced():
    $ room_has_faded_in = getattr(store, 'room_has_faded_in', False)
    $ shader_transform = apply_room_shader_effects()
    
    if not room_has_faded_in:
        timer ROOM_DISPLAY_CONFIG["fade_duration"] action SetVariable('room_has_faded_in', True)

    if hasattr(store, 'crt_enabled') and store.crt_enabled:
        # WITH CRT - place content inside CRT frame
        $ crt_warp = getattr(store, 'crt_warp', 0.2)
        $ crt_scan = getattr(store, 'crt_scan', 0.5)
        $ crt_chroma = getattr(store, 'crt_chroma', 0.9)
        $ crt_scanline_size = getattr(store, 'crt_scanline_size', 1.0)
        $ crt_vignette_strength = getattr(store, 'crt_vignette_strength', 0.35)
        $ crt_vignette_width = getattr(store, 'crt_vignette_width', 0.25)
        $ crt_animated = getattr(store, 'crt_animated', False)
        
        # Main CRT frame - outermost container
        frame at (animated_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size, vignette_strength=crt_vignette_strength, vignette_width=crt_vignette_width) if crt_animated else static_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size, vignette_strength=crt_vignette_strength, vignette_width=crt_vignette_width)):
            background None
            
            # Black fallback background
            add get_fallback_background() at black_background()
            
            # Layer 1: Room background (possibly with shader)
            if shader_transform:
                # Room background with shader applied
                frame:
                    background None
                    if not room_has_faded_in:
                        add get_room_background() at Transform(room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), expression(shader_transform))
                    else:
                        add get_room_background() at Transform(room_no_fade(), expression(shader_transform))
                    
                    # Layer 2: Objects with same shader for consistency
                    for obj_name, obj_data in room_objects.items():
                        if should_display_object(obj_data) and not is_object_hidden(obj_data):
                            $ props = get_object_display_properties(obj_data)
                            $ obj_shader = get_shader_transform_for_object(obj_name, obj_data)
                            
                            if not room_has_faded_in:
                                add props["image"] at Transform(room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), expression(obj_shader or shader_transform)):
                                    xpos props["xpos"]
                                    ypos props["ypos"]
                                    xsize props["xsize"]
                                    ysize props["ysize"]
                            else:
                                add props["image"] at Transform(room_no_fade(), expression(obj_shader or shader_transform)):
                                    xpos props["xpos"]
                                    ypos props["ypos"]
                                    xsize props["xsize"]
                                    ysize props["ysize"]
            else:
                # Standard rendering without shaders
                if not room_has_faded_in:
                    add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
                else:
                    add get_room_background() at room_no_fade()
                
                for obj_name, obj_data in room_objects.items():
                    if should_display_object(obj_data) and not is_object_hidden(obj_data):
                        $ props = get_object_display_properties(obj_data)
                        if not room_has_faded_in:
                            add props["image"] at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]):
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
            
            # Layer 3: Bloom effects on top of shader-affected content
            use room_bloom_effects_internal
    else:
        # WITHOUT CRT - direct rendering
        add get_fallback_background() at black_background()
        
        # Layer 1: Room background with shader
        if shader_transform:
            # Room background with shader applied
            frame:
                background None
                if not room_has_faded_in:
                    add get_room_background() at Transform(room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), expression(shader_transform))
                else:
                    add get_room_background() at Transform(room_no_fade(), expression(shader_transform))
                
                # Layer 2: Objects with same shader for consistency
                for obj_name, obj_data in room_objects.items():
                    if should_display_object(obj_data) and not is_object_hidden(obj_data):
                        $ props = get_object_display_properties(obj_data)
                        $ obj_shader = get_shader_transform_for_object(obj_name, obj_data)
                        
                        if not room_has_faded_in:
                            add props["image"] at Transform(room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), expression(obj_shader or shader_transform)):
                                xpos props["xpos"]
                                ypos props["ypos"]
                                xsize props["xsize"]
                                ysize props["ysize"]
                        else:
                            add props["image"] at Transform(room_no_fade(), expression(obj_shader or shader_transform)):
                                xpos props["xpos"]
                                ypos props["ypos"]
                                xsize props["xsize"]
                                ysize props["ysize"]
        else:
            # Standard rendering without shaders
            if not room_has_faded_in:
                add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
            else:
                add get_room_background() at room_no_fade()
            
            for obj_name, obj_data in room_objects.items():
                if should_display_object(obj_data) and not is_object_hidden(obj_data):
                    $ props = get_object_display_properties(obj_data)
                    if not room_has_faded_in:
                        add props["image"] at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]):
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
        
        # Layer 3: Bloom effects on top of shader-affected content
        use room_bloom_effects_internal

# Enhanced exploration screen with shader controls and bloom compatibility
screen room_exploration_enhanced():
    # Lock input until the initial fade completes
    $ input_locked = not room_has_faded_in
    
    # Room background and objects with shader support that works with bloom
    use room_background_and_objects_enhanced
    use room_bloom_effects  # External bloom effects - kept for compatibility

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

    # EXISTING CONTROLS (moved to shader_control_system.rpy)
    if not input_locked:
        # NOTE: 'c' was moved to Shift+P (CRT Parameter) to avoid conflicts with shader keys
        key "shift_K_p" action Function(toggle_crt_effect)  # Changed from 'c'
        
        # Keep existing keys that don't conflict
        key "f" action Function(fade_out_room_audio)  # Keep 'f' for audio fade
        key "l" action Function(toggle_letterbox)
        key "i" action ToggleVariable("show_info_overlay")
        
        # CRT animation toggle moved to Alt+A for Animation
        key "alt_K_a" action Function(toggle_crt_animation)  # Changed from 'a'

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

# Note: Custom composite transforms would be implemented here in a future version
# For now, we use the predefined composite transforms from detective_composite_shaders.rpy

# Helper function to adapt existing setup to new system
init python:
    def install_enhanced_shader_system():
        """Replace the standard room exploration screen with enhanced version"""
        global room_exploration
        renpy.hide_screen("room_exploration")
        room_exploration = renpy.display.screen.get_screen_variant("room_exploration_enhanced")
        print("Enhanced shader system installed successfully!")
        
# Example usage for your game:
# label start:
#     $ install_enhanced_shader_system()
#     jump your_game_start
