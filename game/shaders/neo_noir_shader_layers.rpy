# Neo-Noir Unified Shader Layer System
# Manages the layered shader architecture for the game
# Layer 1: Dynamic Lighting (affects background and objects)
# Layer 2: Game Overlay (CRT, noise, color grading)

init -10 python:
    # Shader system state variables
    store.shader_system_enabled = True
    store.current_shader_stack = []
    
    # Layer states
    store.lighting_layer_enabled = True
    store.overlay_layer_enabled = True
    
    # Individual effect states
    store.crt_effect_enabled = True
    store.noise_effect_enabled = True
    store.color_grading_enabled = True
    
    def apply_shader_stack(displayable):
        """Apply the complete shader stack to a displayable"""
        result = displayable
        
        # Layer 1: Dynamic Lighting (bottom layer, affects scene)
        if store.lighting_layer_enabled and store.current_lighting != "neutral":
            for preset_id, _, transform in store.lighting_presets:
                if preset_id == store.current_lighting:
                    result = At(result, transform)
                    break
        
        # Layer 2: Game Overlay Effects (top layer)
        if store.overlay_layer_enabled:
            # Apply color grading first
            if store.color_grading_enabled and store.current_color_grade != "off":
                for preset_id, _, transform in store.color_grade_presets:
                    if preset_id == store.current_color_grade:
                        result = At(result, transform)
                        break
            
            # Apply noise/grain effect (bottom layer)
            if store.noise_effect_enabled and hasattr(store, 'film_grain_enabled') and store.film_grain_enabled:
                result = At(result, film_grain_effect)
            
            # Apply CRT effect (middle layer)
            if store.crt_effect_enabled and getattr(store, 'crt_enabled', False):
                crt_warp = getattr(store, 'crt_warp', 0.2)
                crt_scan = getattr(store, 'crt_scan', 0.5)
                crt_chroma = getattr(store, 'crt_chroma', 0.9)
                crt_scanline_size = getattr(store, 'crt_scanline_size', 1.0)
                crt_vignette_strength = getattr(store, 'crt_vignette_strength', 0.35)
                crt_vignette_width = getattr(store, 'crt_vignette_width', 0.25)
                crt_animated = getattr(store, 'crt_animated', False)
                
                if crt_animated:
                    result = At(result, animated_chroma_crt(
                        crt_warp, crt_scan, crt_chroma, crt_scanline_size,
                        vignette_strength=crt_vignette_strength,
                        vignette_width=crt_vignette_width
                    ))
                else:
                    result = At(result, static_chroma_crt(
                        crt_warp, crt_scan, crt_chroma, crt_scanline_size,
                        vignette_strength=crt_vignette_strength,
                        vignette_width=crt_vignette_width
                    ))
            
            # Letterbox is now handled as a separate overlay screen - see letterbox_overlay screen below
        
        return result

# Enhanced room exploration screen with proper shader layering
screen neo_noir_room_exploration():
    # Get room state
    $ room_has_faded_in = getattr(store, 'room_has_faded_in', False)
    if not room_has_faded_in:
        timer ROOM_DISPLAY_CONFIG["fade_duration"] action SetVariable('room_has_faded_in', True)
    
    $ input_locked = not room_has_faded_in
    
    # Layer 1: Scene with Dynamic Lighting
    # This layer contains the background and objects
    $ scene_layer = Composite(
        (1280, 720),
        (0, 0), get_room_background() if hasattr(store, 'room_background') else Solid("#000000")
    )
    
    # Add objects to scene layer
    for obj_name, obj_data in room_objects.items():
        if should_display_object(obj_data) and not is_object_hidden(obj_data):
            $ props = get_object_display_properties(obj_data)
            $ obj_image = Transform(props["image"], 
                xpos=props["xpos"], ypos=props["ypos"],
                xsize=props["xsize"], ysize=props["ysize"])
            $ scene_layer = Composite(
                (1280, 720),
                (0, 0), scene_layer,
                (0, 0), obj_image
            )
    
    # Apply shader stack to the complete scene
    add apply_shader_stack(scene_layer)
    
    # Letterbox overlay (above shader effects, below UI) - always present but animation controlled by letterbox_enabled
    use letterbox_overlay
    
    # UI Layer (above all shader effects)
    # Interactive elements
    if not input_locked:
        use object_hotspots
    
    # Description system
    if (not input_locked) and current_hover_object and not interaction_menu_active:
        $ obj = room_objects[current_hover_object]
        $ box_width, box_height = calculate_description_box_size(obj["description"])
        $ position_setting = obj.get("box_position", "auto")
        $ box_x, box_y, box_position = calculate_box_position(obj, box_width, box_height, position_setting)
        $ float_intensity = obj.get("float_intensity", 1.0)
        use floating_description_box(obj, box_width, box_height, box_x, box_y, float_intensity)
    
    # Interaction menu
    use interaction_menu
    
    # UI buttons and overlays
    if not input_locked:
        use room_ui_buttons
    use info_overlay
    
    # Shader controls
    use neo_noir_shader_controls
    
    # Keyboard navigation
    if (not input_locked) and interaction_menu_active:
        key "K_UP" action Function(navigate_interaction_menu, "up")
        key "K_DOWN" action Function(navigate_interaction_menu, "down")
        key "K_RETURN" action Function(execute_selected_action)
        key "K_ESCAPE" action Function(keyboard_cancel_action)
    
    # Gamepad controls
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

# Shader control screen with hotkeys
screen neo_noir_shader_controls():
    # CRT controls
    key "c" action [
        ToggleVariable("crt_enabled"),
        Function(renpy.notify, "CRT: " + ("ON" if store.crt_enabled else "OFF")),
        Function(renpy.restart_interaction)
    ]
    key "a" action [
        ToggleVariable("crt_animated"),
        Function(renpy.notify, "CRT Animation: " + ("ON" if store.crt_animated else "OFF")),
        Function(renpy.restart_interaction)
    ]
    
    # Scanline size presets
    key "1" action [Function(set_crt_parameters, scanline_size=0.5), Function(renpy.restart_interaction)]
    key "2" action [Function(set_crt_parameters, scanline_size=1.0), Function(renpy.restart_interaction)]
    key "3" action [Function(set_crt_parameters, scanline_size=1.5), Function(renpy.restart_interaction)]
    key "4" action [Function(set_crt_parameters, scanline_size=3.0), Function(renpy.restart_interaction)]
    
    # Vignette controls
    key "[" action [Function(adjust_vignette, delta_strength=-0.05), Function(renpy.restart_interaction)]
    key "]" action [Function(adjust_vignette, delta_strength=0.05), Function(renpy.restart_interaction)]
    key "-" action [Function(adjust_vignette, delta_width=-0.02), Function(renpy.restart_interaction)]
    key "=" action [Function(adjust_vignette, delta_width=0.02), Function(renpy.restart_interaction)]
    key "0" action [Function(adjust_vignette, set_strength=0.35, set_width=0.25), Function(renpy.restart_interaction)]
    
    # Color grading controls
    key "shift_K_c" action Function(cycle_color_grade, 1)
    key "ctrl_K_c" action Function(cycle_color_grade, -1)
    
    # Lighting controls
    key "shift_K_l" action Function(cycle_lighting, 1)
    key "ctrl_K_l" action Function(cycle_lighting, -1)
    
    # Film grain toggle
    key "g" action [
        ToggleVariable("film_grain_enabled"),
        Function(renpy.notify, "Film Grain: " + ("ON" if store.film_grain_enabled else "OFF")),
        Function(renpy.restart_interaction)
    ]
    
    # Letterbox controls
    key "l" action Function(letterbox_combined_action)
    key "shift_K_x" action Function(letterbox_force_off)  # Force letterbox off
    
    # Master shader toggle
    key "shift_K_s" action [
        ToggleVariable("shader_system_enabled"),
        Function(renpy.notify, "Shader System: " + ("ON" if store.shader_system_enabled else "OFF")),
        Function(renpy.restart_interaction)
    ]
    
    # Show shader help
    key "h" action [
        ToggleVariable("shader_help_visible"),
        Function(renpy.restart_interaction)
    ]
    
    # Info overlay toggle
    key "i" action ToggleVariable("show_info_overlay")

# Shader help overlay
screen neo_noir_shader_help():
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 20
        
        vbox:
            spacing 10
            
            text "Neo-Noir Shader Controls" size 24 color "#ffffff" xalign 0.5
            null height 10
            
            text "{b}CRT Effects:{/b}" size 18 color "#ffcc00"
            text "C - Toggle CRT effect" size 16
            text "A - Toggle CRT animation" size 16
            text "1-4 - Scanline size presets" size 16
            text "[ ] - Adjust vignette strength" size 16
            text "- = - Adjust vignette width" size 16
            text "0 - Reset vignette" size 16
            null height 5
            
            text "{b}Color Grading:{/b}" size 18 color "#ffcc00"
            text "Shift+C - Next color grade preset" size 16
            text "Ctrl+C - Previous color grade preset" size 16
            null height 5
            
            text "{b}Lighting:{/b}" size 18 color "#ffcc00"
            text "Shift+L - Next lighting preset" size 16
            text "Ctrl+L - Previous lighting preset" size 16
            null height 5
            
            text "{b}Letterbox:{/b}" size 18 color "#ffcc00"
            text "L - Toggle letterbox / cycle speed" size 16
            text "Shift+X - Force letterbox off" size 16
            null height 5
            
            text "{b}Other:{/b}" size 18 color "#ffcc00"
            text "G - Toggle film grain" size 16
            text "Shift+S - Toggle shader system" size 16
            text "I - Toggle info overlay" size 16
            text "H - Toggle this help" size 16
            null height 10
            
            textbutton "Close" action [
                SetVariable("shader_help_visible", False),
                Function(renpy.restart_interaction)
            ] xalign 0.5

# Initialize shader help visibility
default shader_help_visible = False
default film_grain_enabled = False
