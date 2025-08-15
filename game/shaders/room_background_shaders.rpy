# Room Background Shaders Integration
# Applies shader effects to room backgrounds and objects uniformly

# Global defaults for shader UI-adjustable values
default film_grain_downscale = 2.0
default lighting_strength = 1.0
default lighting_animated = False
default lighting_anim_speed = 0.5
default lighting_anim_strength = 0.15

init python:
    from renpy.uguu import GL_CLAMP_TO_EDGE
    
    def update_lighting_strength(value):
        """Update lighting strength and force screen refresh"""
        store.lighting_strength = float(value)
        print(f"[LIGHTING] Strength updated to: {store.lighting_strength}")
        renpy.restart_interaction()
    
    def update_lighting_speed(value):
        """Update lighting animation speed and force screen refresh"""
        store.lighting_anim_speed = float(value)
        print(f"[LIGHTING] Speed updated to: {store.lighting_anim_speed}")
        renpy.restart_interaction()
    
    class LightingStrengthValue(BarValue):
        def __init__(self):
            pass
        
        def get_adjustment(self):
            return ui.adjustment(range=3.0, value=store.lighting_strength, step=0.1, page=0.1, changed=self.changed)
        
        def changed(self, value):
            store.lighting_strength = value
            print(f"[LIGHTING] Strength changed to: {store.lighting_strength}")
            renpy.restart_interaction()
    
    class LightingSpeedValue(BarValue):
        def __init__(self):
            pass
        
        def get_adjustment(self):
            return ui.adjustment(range=2.9, value=store.lighting_anim_speed, step=0.1, page=0.1, changed=self.changed)
        
        def changed(self, value):
            store.lighting_anim_speed = value
            print(f"[LIGHTING] Speed changed to: {store.lighting_anim_speed}")
            renpy.restart_interaction()

# Transform that applies current shader effects to any displayable
transform room_background_and_objects_with_shaders():
    mesh True
    gl_texture_wrap (GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)
    u_lod_bias 0.0
    gl_mipmap True
    function update_combined_shaders

# Enhanced room exploration screen with shader integration
screen room_exploration_shaders():
    # Simple room fade-in control
    $ room_has_faded_in = getattr(store, 'room_has_faded_in', False)
    if not room_has_faded_in:
        timer ROOM_DISPLAY_CONFIG["fade_duration"] action SetVariable('room_has_faded_in', True)
    
    $ input_locked = not room_has_faded_in
    $ suppress_room_fade_once = getattr(store, 'suppress_room_fade_once', False)
    
    # Force CRT to always be enabled and animated during gameplay
    $ store.crt_enabled = True
    $ store.crt_animated = True
    
    # Determine active grading and grain transforms
    $ cg_state = shader_states["color_grading"]["current"] if "color_grading" in shader_states else 0
    $ grain_state = shader_states["film_grain"]["current"] if "film_grain" in shader_states else 0
    $ grade_transform = None
    # Lighting transform at frame level for uniform effect
    $ li_state = shader_states["lighting"]["current"] if "lighting" in shader_states else 0
    $ light_transform = None
    $ _li_name = (shader_states["lighting"]["presets"][li_state] if "lighting" in shader_states and li_state < len(shader_states["lighting"]["presets"]) else "n/a")
    $ _cg_name = (shader_states["color_grading"]["presets"][cg_state] if "color_grading" in shader_states and cg_state < len(shader_states["color_grading"]["presets"]) else "n/a")
    $ _gr_name = (shader_states["film_grain"]["presets"][grain_state] if "film_grain" in shader_states and grain_state < len(shader_states["film_grain"]["presets"]) else "n/a")
    $ _crt_on = getattr(store, 'crt_enabled', False)
    $ _crt_anim = getattr(store, 'crt_animated', False)
    python:
        try:
            from renpy.store import shader_debug_enabled
            if shader_debug_enabled:
                _emit_pipeline_summary_if_changed(cg_state, _cg_name, li_state, _li_name, grain_state, _gr_name, _crt_on, _crt_anim)
        except Exception:
            pass
    if li_state > 0:
        $ li_preset = shader_states["lighting"]["presets"][li_state]
        # Use dynamic lighting so strength and animation apply live
        $ light_transform = Transform(function=renpy.curry(dynamic_lighting_update)(preset=li_preset), mesh=True, shader="neo_noir_lighting")
    if cg_state > 0:
        $ cg_preset = shader_states["color_grading"]["presets"][cg_state]
        if cg_preset == "classic_noir":
            $ grade_transform = color_grade_classic_noir()
        elif cg_preset == "neon_night":
            $ grade_transform = color_grade_neon_night()
        elif cg_preset == "rain_streets":
            $ grade_transform = color_grade_rain_streets()
        elif cg_preset == "smoky_bar":
            $ grade_transform = color_grade_smoky_bar()
        elif cg_preset == "miami_vice":
            $ grade_transform = color_grade_miami_vice()
        elif cg_preset == "detective_office":
            $ grade_transform = color_grade_detective_office()
        elif cg_preset == "crime_scene":
            $ grade_transform = color_grade_crime_scene()
        elif cg_preset == "blade_runner":
            $ grade_transform = color_grade_blade_runner()
        elif cg_preset == "evidence_room":
            $ grade_transform = color_grade_evidence_room()
        elif cg_preset == "midnight_chase":
            $ grade_transform = color_grade_midnight_chase()
    $ grain_transform = None
    if grain_state > 0:
        $ grain_preset = shader_states["film_grain"]["presets"][grain_state]
        $ _fg_downscale = getattr(store, 'film_grain_downscale', 2.0)
        if grain_preset == "subtle":
            $ grain_transform = room_film_grain_overlay(grain_intensity=0.02, grain_size=120.0, downscale=_fg_downscale)
        elif grain_preset == "moderate":
            $ grain_transform = room_film_grain_overlay(grain_intensity=0.05, grain_size=100.0, downscale=_fg_downscale)
        elif grain_preset == "heavy":
            $ grain_transform = room_film_grain_overlay(grain_intensity=0.10, grain_size=80.0, downscale=_fg_downscale)

    # Apply shaders to the background and objects layer
    # Note: Built-in Ren'Py transitions are applied at the screen level (via "with transition")
    # Shaders are applied on top of the transitioned content
    if hasattr(store, 'crt_enabled') and store.crt_enabled:
        $ _prev = getattr(store, '_last_crt_state', None)
        $ store._last_crt_state = 'on'
        if shader_debug_enabled and _prev != 'on' and not getattr(store, '_suppress_crt_boot_logs', False):
            $ print("[ROOM SHADERS] CRT ON")
        $ crt_warp = getattr(store, 'crt_warp', 0.2)
        $ crt_scan = getattr(store, 'crt_scan', 0.5)
        $ crt_chroma = getattr(store, 'crt_chroma', 0.9)
        $ crt_scanline_size = getattr(store, 'crt_scanline_size', 1.0)
        $ crt_vignette_strength = getattr(store, 'crt_vignette_strength', 0.35)
        $ crt_vignette_width = getattr(store, 'crt_vignette_width', 0.25)
        $ crt_animated = getattr(store, 'crt_animated', False)
        frame at (light_transform if light_transform else room_no_fade(), grade_transform if grade_transform else room_no_fade(), grain_transform if grain_transform else room_no_fade(), (animated_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size, vignette_strength=crt_vignette_strength, vignette_width=crt_vignette_width) if crt_animated else static_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size, vignette_strength=crt_vignette_strength, vignette_width=crt_vignette_width))):
            background None
            add get_fallback_background() at black_background()
            # Draw room background with standard fade
            if not room_has_faded_in and not suppress_room_fade_once:
                add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
            else:
                add get_room_background() at room_no_fade()
            $ suppress_room_fade_once = False
            # Apply shaders to room objects with desaturation effect for hovered objects
            for obj_name, obj_data in room_objects.items():
                if should_display_object(obj_data) and not is_object_hidden(obj_data):
                    $ props = get_object_display_properties(obj_data)
                    $ is_hovered = (current_hover_object == obj_name)
                    $ was_hovered = getattr(store, 'previous_hover_object', None) == obj_name
                    
                    # Choose transform based on hover state
                    # Base transform: fade/no-fade based on room state
                    if room_has_faded_in:
                        $ base_transform = room_no_fade()
                    else:
                        $ base_transform = room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
                    
                    if is_hovered:
                        if hasattr(store, 'bloom_debug_hover') and store.bloom_debug_hover:
                            $ debug_bloom(f"[HOVER] {obj_name}: ACTIVE HOVER - applying desaturation pulse")
                        $ object_transform = (base_transform, get_hover_desaturation_transform(obj_data))
                    elif was_hovered and not is_hovered:
                        # Object was hovered but no longer is - use graceful fadeout
                        if hasattr(store, 'bloom_debug_hover') and store.bloom_debug_hover:
                            $ debug_bloom(f"[HOVER] {obj_name}: LEAVING HOVER - applying graceful fadeout (0.4s)")
                        $ object_transform = (base_transform, object_desaturation_fadeout)
                    else:
                        # Object was never hovered or has finished fading out
                        $ object_transform = (base_transform, object_normal_saturation)
                    
                    add props["image"] at object_transform:
                        xpos props["xpos"]
                        ypos props["ypos"]
                        xsize props["xsize"]
                        ysize props["ysize"]
    else:
        $ _prev = getattr(store, '_last_crt_state', None)
        $ store._last_crt_state = 'off'
        if shader_debug_enabled and _prev != 'off' and not getattr(store, '_suppress_crt_boot_logs', False):
            $ print("[ROOM SHADERS] CRT OFF")
        # Non-CRT version with shaders
        add get_fallback_background() at black_background()
        if not room_has_faded_in and not suppress_room_fade_once:
            add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
        else:
            add get_room_background() at room_no_fade()
        $ suppress_room_fade_once = False
        for obj_name, obj_data in room_objects.items():
            if should_display_object(obj_data) and not is_object_hidden(obj_data):
                $ props = get_object_display_properties(obj_data)
                $ is_hovered = (current_hover_object == obj_name)
                $ was_hovered = getattr(store, 'previous_hover_object', None) == obj_name
                
                # Choose transform based on hover state
                if is_hovered:
                    $ object_transform = (room_no_fade() if room_has_faded_in else room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), get_hover_desaturation_transform(obj_data))
                elif was_hovered and not is_hovered:
                    # Object was hovered but no longer is - use graceful fadeout
                    $ object_transform = (room_no_fade() if room_has_faded_in else room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), object_desaturation_fadeout)
                else:
                    # Object was never hovered or has finished fading out
                    $ object_transform = (room_no_fade() if room_has_faded_in else room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]), object_normal_saturation)
                
                add props["image"] at object_transform:
                    xpos props["xpos"]
                    ypos props["ypos"]
                    xsize props["xsize"]
                    ysize props["ysize"]
        # Note: Bloom effects now handled via desaturation in object rendering
    
    # Film grain and color grading now applied as transforms on the main frame to avoid outline artifacts.
    # (No separate overlays needed.)
    
    # Fog overlay removed per new design
    
    # Debug: Show input status and bloom information (only when debug enabled)
    if getattr(store, 'show_debug_overlay', False):
        text "Input: [('LOCKED' if input_locked else 'ACTIVE')] | Fade: [room_has_faded_in] | Objects: [len(room_objects)]":
            xpos 10
            ypos 100
            color "#ffff00"
            size 16
        
        # Debug: Show gamepad and bloom status
        text "Gamepad Nav: [('ON' if gamepad_navigation_enabled else 'OFF')] | Selected: [gamepad_selected_object] | Hover: [current_hover_object]":
            xpos 10
            ypos 120
            color "#00ff00"
            size 14
            
        # Debug: Show desaturation status (replaces bloom)
        if current_hover_object and current_hover_object in room_objects:
            text "Desaturation: ACTIVE for [current_hover_object]":
                xpos 10
                ypos 140
                color "#ff8800"
                size 14
        else:
            text "Desaturation: NO HOVER OBJECT":
                xpos 10
                ypos 140
                color "#ff0000"
                size 14
    
    # Interactive elements from original system
    if not input_locked and not getattr(store,'interactions_paused', False):
        use object_hotspots
    else:
        # Show debug when input is locked
        text "INPUT LOCKED - waiting for room fade":
            xpos 10
            ypos 120
            color "#ff0000"
            size 14
    
    # Description system - show floating descriptions on hover (above CRT)
    # Keep description visible when interaction menu is active
    if (not input_locked) and (not getattr(store,'interactions_paused', False)) and current_hover_object:
        $ obj = room_objects[current_hover_object]
        $ box_width, box_height = calculate_description_box_size(obj["description"])
        $ position_setting = obj.get("box_position", "auto")
        $ box_x, box_y, box_position = calculate_box_position(obj, box_width, box_height, position_setting)
        $ float_intensity = obj.get("float_intensity", 1.0)
        use floating_description_box(obj, box_width, box_height, box_x, box_y, float_intensity)
    
    # Interaction menu (must be included for interactions to work!)
    if not getattr(store,'interactions_paused', False):
        use interaction_menu
    
    # Letterbox overlay (above CRT, below UI)
    use letterbox_overlay
    
    # UI and debug overlays - FORCE ABOVE CRT
    if not input_locked:
        use room_ui_buttons
    use info_overlay
    
    # Include the shader hotkeys - MOVED HERE TO ENSURE THEY WORK
    use shader_hotkeys
    
    # Show shader help if enabled - MOVED HERE TO BE ON TOP
    if shader_help_visible:
        use shader_help
    
    # Keyboard navigation for interaction menus
    if (not input_locked) and interaction_menu_active:
        key "K_UP" action Function(navigate_interaction_menu, "up")
        key "K_DOWN" action Function(navigate_interaction_menu, "down")
        key "K_RETURN" action Function(execute_selected_action)
        key "K_ESCAPE" action Function(keyboard_cancel_action)
    
    # Allow access to game menu with Escape/Start button
    
    # Gamepad controls (from original system)
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
    
    # Global shortcuts (updated hotkeys)
    if not input_locked and not getattr(store,'interactions_paused', False):
        key "shift_p" action Function(toggle_crt_effect)  # CRT toggle
        key "f" action Function(fade_out_room_audio)  # Audio fade
        # key "g" action Function(toggle_fog_shader)  # Removed: fog shader no longer in use
        key "l" action Function(letterbox_combined_action)
        key "shift_x" action Function(letterbox_force_off)
        key "i" action ToggleVariable("show_info_overlay")
        key "alt_c" action Function(toggle_crt_animation)  # CRT animation
        
        # Bloom debug hotkeys
        key "shift_d" action Function(toggle_bloom_debug)  # Toggle bloom debug
        key "shift_v" action Function(toggle_bloom_verbose)  # Toggle verbose debug
        key "shift_r" action Function(set_bloom_debug, True, True)  # Reset debug to full
    
    # Scanline size testing
    if not input_locked:
        key "1" action Function(set_crt_parameters, scanline_size=0.5)
        key "2" action Function(set_crt_parameters, scanline_size=1.0)
        key "3" action Function(set_crt_parameters, scanline_size=1.5)
        key "4" action Function(set_crt_parameters, scanline_size=3.0)
    
    # Vignette live tuning
    if not input_locked:
        key "[" action Function(adjust_vignette, delta_strength=-0.05)
        key "]" action Function(adjust_vignette, delta_strength=0.05)
        key "-" action Function(adjust_vignette, delta_width=-0.02)
        key "=" action Function(adjust_vignette, delta_width=0.02)
        key "0" action Function(adjust_vignette, set_strength=0.35, set_width=0.25)

# Fog shader toggle removed (feature deprecated)

# Helper function for shader application
init python:
    # Lighting preset dynamic builder for animation and strength
    def _apply_lighting_preset_uniforms(trans, preset, st):
        # defaults
        trans.u_ambient_color = (1.0, 1.0, 1.0); trans.u_ambient_intensity = 0.3
        trans.u_light_pos = (0.5, 0.3); trans.u_light_color = (1.0, 1.0, 1.0); trans.u_light_intensity = 1.0; trans.u_light_radius = 0.8
        trans.u_light2_pos = (0.8, 0.7); trans.u_light2_color = (1.0, 1.0, 1.0); trans.u_light2_intensity = 0.5; trans.u_light2_radius = 0.6
        trans.u_shadow_softness = 0.5; trans.u_shadow_intensity = 0.7
        trans.u_specular_intensity = 0.0; trans.u_specular_size = 2.0
        trans.u_fog_density = 0.0; trans.u_fog_color = (0.5, 0.5, 0.6)
        # per-preset overrides
        if preset == "street_lamp":
            trans.u_light_pos = (0.5, 0.2); trans.u_light_color = (1.0, 0.9, 0.7); trans.u_light_intensity = 1.2; trans.u_light_radius = 0.6
            trans.u_ambient_color = (0.3, 0.3, 0.4); trans.u_ambient_intensity = 0.2; trans.u_shadow_softness = 0.3; trans.u_shadow_intensity = 0.8; trans.u_fog_density = 0.3; trans.u_fog_color = (0.2, 0.2, 0.3)
        elif preset == "neon_signs":
            trans.u_light_pos = (0.1, 0.3); trans.u_light_color = (1.0, 0.3, 0.6); trans.u_light_intensity = 0.9; trans.u_light_radius = 0.5
            trans.u_light2_pos = (0.9, 0.4); trans.u_light2_color = (0.3, 0.8, 1.0); trans.u_light2_intensity = 0.8; trans.u_light2_radius = 0.5
            trans.u_ambient_color = (0.4, 0.3, 0.5); trans.u_ambient_intensity = 0.3; trans.u_shadow_softness = 0.6; trans.u_shadow_intensity = 0.6
        elif preset == "window_blinds":
            trans.u_light_pos = (0.7, 0.3); trans.u_light_color = (0.9, 0.95, 1.0); trans.u_light_intensity = 1.1; trans.u_light_radius = 0.7
            trans.u_light2_pos = (0.3, 0.6); trans.u_light2_color = (0.6, 0.65, 0.8); trans.u_light2_intensity = 0.3; trans.u_light2_radius = 0.4
            trans.u_ambient_color = (0.4, 0.45, 0.5); trans.u_ambient_intensity = 0.25; trans.u_shadow_softness = 0.2; trans.u_shadow_intensity = 0.85; trans.u_fog_density = 0.4; trans.u_fog_color = (0.3, 0.35, 0.4)
        elif preset == "police_lights":
            trans.u_light_pos = (0.3, 0.5); trans.u_light_color = (1.0, 0.0, 0.2); trans.u_light_intensity = 1.0; trans.u_light_radius = 0.6
            trans.u_light2_pos = (0.7, 0.5); trans.u_light2_color = (0.0, 0.3, 1.0); trans.u_light2_intensity = 1.0; trans.u_light2_radius = 0.6
            trans.u_ambient_color = (0.2, 0.2, 0.3); trans.u_ambient_intensity = 0.15; trans.u_shadow_softness = 0.4; trans.u_shadow_intensity = 0.7
        elif preset == "desk_lamp":
            trans.u_light_pos = (0.75, 0.6); trans.u_light_color = (1.0, 0.95, 0.8); trans.u_light_intensity = 1.3; trans.u_light_radius = 0.45
            trans.u_ambient_color = (0.35, 0.33, 0.3); trans.u_ambient_intensity = 0.2; trans.u_shadow_softness = 0.25; trans.u_shadow_intensity = 0.75; trans.u_fog_density = 0.5; trans.u_fog_color = (0.4, 0.38, 0.35)
        elif preset == "car_headlights":
            trans.u_light_pos = (0.2, 0.5); trans.u_light_color = (1.0, 1.0, 0.95); trans.u_light_intensity = 1.5; trans.u_light_radius = 0.8
            trans.u_light2_pos = (0.8, 0.5); trans.u_light2_color = (1.0, 1.0, 0.95); trans.u_light2_intensity = 1.5; trans.u_light2_radius = 0.8
            trans.u_ambient_color = (0.2, 0.2, 0.25); trans.u_ambient_intensity = 0.1; trans.u_shadow_softness = 0.15; trans.u_shadow_intensity = 0.9; trans.u_specular_intensity = 0.3; trans.u_specular_size = 1.5; trans.u_fog_density = 0.6; trans.u_fog_color = (0.25, 0.25, 0.3)
        elif preset == "interrogation":
            trans.u_light_pos = (0.5, 0.5); trans.u_light_color = (0.95, 1.0, 0.95); trans.u_light_intensity = 1.4; trans.u_light_radius = 0.9
            trans.u_ambient_color = (0.8, 0.85, 0.8); trans.u_ambient_intensity = 0.4; trans.u_shadow_softness = 0.1; trans.u_shadow_intensity = 0.95; trans.u_specular_intensity = 0.2; trans.u_specular_size = 1.0
        elif preset == "sunset_window":
            trans.u_light_pos = (0.85, 0.4); trans.u_light_color = (1.0, 0.7, 0.4); trans.u_light_intensity = 1.2; trans.u_light_radius = 0.9
            trans.u_light2_pos = (0.15, 0.3); trans.u_light2_color = (0.8, 0.5, 0.3); trans.u_light2_intensity = 0.4; trans.u_light2_radius = 0.5
            trans.u_ambient_color = (0.6, 0.45, 0.35); trans.u_ambient_intensity = 0.35; trans.u_shadow_softness = 0.5; trans.u_shadow_intensity = 0.65; trans.u_fog_density = 0.3; trans.u_fog_color = (0.7, 0.5, 0.4)
        elif preset == "dark_alley":
            trans.u_light_pos = (0.3, 0.1); trans.u_light_color = (0.6, 0.6, 0.7); trans.u_light_intensity = 0.6; trans.u_light_radius = 0.4
            trans.u_light2_pos = (0.8, 0.9); trans.u_light2_color = (0.4, 0.4, 0.5); trans.u_light2_intensity = 0.3; trans.u_light2_radius = 0.3
            trans.u_ambient_color = (0.15, 0.15, 0.2); trans.u_ambient_intensity = 0.15; trans.u_shadow_softness = 0.35; trans.u_shadow_intensity = 0.95; trans.u_fog_density = 0.8; trans.u_fog_color = (0.1, 0.1, 0.15)
        elif preset == "tv_glow":
            trans.u_light_pos = (0.5, 0.6); trans.u_light_color = (0.8, 0.9, 1.0); trans.u_light_intensity = 0.9; trans.u_light_radius = 0.7
            trans.u_ambient_color = (0.3, 0.35, 0.45); trans.u_ambient_intensity = 0.25; trans.u_shadow_softness = 0.7; trans.u_shadow_intensity = 0.5; trans.u_fog_density = 0.2; trans.u_fog_color = (0.35, 0.4, 0.5)
        # Apply strength and animation wobble
        strength = getattr(store,'lighting_strength',1.0)
        animated = getattr(store,'lighting_animated', False)
        speed = getattr(store,'lighting_anim_speed',0.5)
        anim_strength = getattr(store,'lighting_anim_strength',0.15)
        trans.u_light_intensity *= strength
        trans.u_light2_intensity *= strength
        if animated:
            import math
            wobble = anim_strength * strength * (0.5 + 0.5 * math.sin(st * 2.0 * 3.14159 * speed))
            trans.u_light_intensity += wobble
            trans.u_light2_intensity += wobble
            # For police_lights: add alternating effect
            if preset == "police_lights":
                red_cycle = 0.5 + 0.5 * math.sin(st * 4.0 * 3.14159 * speed)
                blue_cycle = 0.5 + 0.5 * math.sin(st * 4.0 * 3.14159 * speed + 3.14159)
                trans.u_light_intensity *= (0.5 + 0.5 * red_cycle)
                trans.u_light2_intensity *= (0.5 + 0.5 * blue_cycle)

    def dynamic_lighting_update(trans, st, at, preset):
        _apply_lighting_preset_uniforms(trans, preset, st)
        return 0

    # Cache of last-reported pipeline signature to avoid per-frame spam
    if not hasattr(store, '_last_pipeline_sig'):
        store._last_pipeline_sig = None
    if not hasattr(store, '_last_crt_state'):
        store._last_crt_state = None
    # Default suppress CRT boot logs until explicitly disabled after room enter
    if not hasattr(store, '_suppress_crt_boot_logs'):
        store._suppress_crt_boot_logs = True

    def _emit_pipeline_summary_if_changed(cg_state, cg_name, li_state, li_name, gr_state, gr_name, crt_on, crt_anim):
        """Emit a concise pipeline summary only when state changes."""
        try:
            from renpy.store import shader_debug_enabled
            sig = (cg_state, cg_name, li_state, li_name, gr_state, gr_name, bool(crt_on), bool(crt_anim))
            if shader_debug_enabled and sig != store._last_pipeline_sig:
                print(f"[PIPELINE] CG={cg_state}:{cg_name} | LI={li_state}:{li_name} | GR={gr_state}:{gr_name} | CRT={'ON' if crt_on else 'OFF'}{' (anim)' if crt_anim else ''}")
                store._last_pipeline_sig = sig
        except Exception:
            pass

    def update_combined_shaders(trans, st, at):
        """Combined shaders for background. Includes fog to cover full screen.
        """
        # Ensure model properties are safe
        trans.mesh = True
        trans.gl_texture_wrap = (GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)
        trans.u_lod_bias = 0.0
        trans.gl_mipmap = True

        # Build shader parts list (film grain kept external). We now support neo-noir grading + lighting.
        parts = []
        # Lighting animation parameters
        lighting_strength = getattr(store, 'lighting_strength', 1.0)
        lighting_animated = getattr(store, 'lighting_animated', False)
        lighting_anim_speed = getattr(store, 'lighting_anim_speed', 0.5)

        # Color grading moved to fullscreen overlay to avoid shader variable conflicts when combined.
        # (See color_grading_overlay screen.)

        # Dynamic lighting via neo-noir lighting shader
        if "lighting" in shader_states:
            li_state = shader_states["lighting"]["current"]
            if li_state > 0:
                parts.append("neo_noir_lighting")
                preset = shader_states["lighting"]["presets"][li_state]
                # Common defaults
                trans.u_ambient_color = (1.0, 1.0, 1.0); trans.u_ambient_intensity = 0.3
                trans.u_light_pos = (0.5, 0.3); trans.u_light_color = (1.0, 1.0, 1.0); trans.u_light_intensity = 1.0; trans.u_light_radius = 0.8
                trans.u_light2_pos = (0.8, 0.7); trans.u_light2_color = (1.0, 1.0, 1.0); trans.u_light2_intensity = 0.5; trans.u_light2_radius = 0.6
                trans.u_shadow_softness = 0.5; trans.u_shadow_intensity = 0.7
                trans.u_specular_intensity = 0.0; trans.u_specular_size = 2.0
                trans.u_fog_density = 0.0; trans.u_fog_color = (0.5, 0.5, 0.6)
                # Apply global strength
                trans.u_light_intensity *= lighting_strength
                trans.u_light2_intensity *= lighting_strength
                # Optional subtle animation
                if lighting_animated:
                    import math
                    wobble = 0.05 * lighting_strength * (0.5 + 0.5 * math.sin(st * 2.0 * 3.14159 * lighting_anim_speed))
                    trans.u_light_intensity += wobble
                    trans.u_light2_intensity += wobble
                if preset == "street_lamp":
                    trans.u_light_pos = (0.5, 0.2); trans.u_light_color = (1.0, 0.9, 0.7); trans.u_light_intensity = 1.2; trans.u_light_radius = 0.6
                    trans.u_ambient_color = (0.3, 0.3, 0.4); trans.u_ambient_intensity = 0.2; trans.u_shadow_softness = 0.3; trans.u_shadow_intensity = 0.8; trans.u_fog_density = 0.3; trans.u_fog_color = (0.2, 0.2, 0.3)
                elif preset == "neon_signs":
                    trans.u_light_pos = (0.1, 0.3); trans.u_light_color = (1.0, 0.3, 0.6); trans.u_light_intensity = 0.9; trans.u_light_radius = 0.5
                    trans.u_light2_pos = (0.9, 0.4); trans.u_light2_color = (0.3, 0.8, 1.0); trans.u_light2_intensity = 0.8; trans.u_light2_radius = 0.5
                    trans.u_ambient_color = (0.4, 0.3, 0.5); trans.u_ambient_intensity = 0.3; trans.u_shadow_softness = 0.6; trans.u_shadow_intensity = 0.6
                elif preset == "window_blinds":
                    trans.u_light_pos = (0.7, 0.3); trans.u_light_color = (0.9, 0.95, 1.0); trans.u_light_intensity = 1.1; trans.u_light_radius = 0.7
                    trans.u_light2_pos = (0.3, 0.6); trans.u_light2_color = (0.6, 0.65, 0.8); trans.u_light2_intensity = 0.3; trans.u_light2_radius = 0.4
                    trans.u_ambient_color = (0.4, 0.45, 0.5); trans.u_ambient_intensity = 0.25; trans.u_shadow_softness = 0.2; trans.u_shadow_intensity = 0.85; trans.u_fog_density = 0.4; trans.u_fog_color = (0.3, 0.35, 0.4)
                elif preset == "police_lights":
                    trans.u_light_pos = (0.3, 0.5); trans.u_light_color = (1.0, 0.0, 0.2); trans.u_light_intensity = 1.0; trans.u_light_radius = 0.6
                    trans.u_light2_pos = (0.7, 0.5); trans.u_light2_color = (0.0, 0.3, 1.0); trans.u_light2_intensity = 1.0; trans.u_light2_radius = 0.6
                    trans.u_ambient_color = (0.2, 0.2, 0.3); trans.u_ambient_intensity = 0.15; trans.u_shadow_softness = 0.4; trans.u_shadow_intensity = 0.7
                elif preset == "desk_lamp":
                    trans.u_light_pos = (0.75, 0.6); trans.u_light_color = (1.0, 0.95, 0.8); trans.u_light_intensity = 1.3; trans.u_light_radius = 0.45
                    trans.u_ambient_color = (0.35, 0.33, 0.3); trans.u_ambient_intensity = 0.2; trans.u_shadow_softness = 0.25; trans.u_shadow_intensity = 0.75; trans.u_fog_density = 0.5; trans.u_fog_color = (0.4, 0.38, 0.35)
                elif preset == "car_headlights":
                    trans.u_light_pos = (0.2, 0.5); trans.u_light_color = (1.0, 1.0, 0.95); trans.u_light_intensity = 1.5; trans.u_light_radius = 0.8
                    trans.u_light2_pos = (0.8, 0.5); trans.u_light2_color = (1.0, 1.0, 0.95); trans.u_light2_intensity = 1.5; trans.u_light2_radius = 0.8
                    trans.u_ambient_color = (0.2, 0.2, 0.25); trans.u_ambient_intensity = 0.1; trans.u_shadow_softness = 0.15; trans.u_shadow_intensity = 0.9; trans.u_specular_intensity = 0.3; trans.u_specular_size = 1.5; trans.u_fog_density = 0.6; trans.u_fog_color = (0.25, 0.25, 0.3)
                elif preset == "interrogation":
                    trans.u_light_pos = (0.5, 0.5); trans.u_light_color = (0.95, 1.0, 0.95); trans.u_light_intensity = 1.4; trans.u_light_radius = 0.9
                    trans.u_ambient_color = (0.8, 0.85, 0.8); trans.u_ambient_intensity = 0.4; trans.u_shadow_softness = 0.1; trans.u_shadow_intensity = 0.95; trans.u_specular_intensity = 0.2; trans.u_specular_size = 1.0
                elif preset == "sunset_window":
                    trans.u_light_pos = (0.85, 0.4); trans.u_light_color = (1.0, 0.7, 0.4); trans.u_light_intensity = 1.2; trans.u_light_radius = 0.9
                    trans.u_light2_pos = (0.15, 0.3); trans.u_light2_color = (0.8, 0.5, 0.3); trans.u_light2_intensity = 0.4; trans.u_light2_radius = 0.5
                    trans.u_ambient_color = (0.6, 0.45, 0.35); trans.u_ambient_intensity = 0.35; trans.u_shadow_softness = 0.5; trans.u_shadow_intensity = 0.65; trans.u_fog_density = 0.3; trans.u_fog_color = (0.7, 0.5, 0.4)
                elif preset == "dark_alley":
                    trans.u_light_pos = (0.3, 0.1); trans.u_light_color = (0.6, 0.6, 0.7); trans.u_light_intensity = 0.6; trans.u_light_radius = 0.4
                    trans.u_light2_pos = (0.8, 0.9); trans.u_light2_color = (0.4, 0.4, 0.5); trans.u_light2_intensity = 0.3; trans.u_light2_radius = 0.3
                    trans.u_ambient_color = (0.15, 0.15, 0.2); trans.u_ambient_intensity = 0.15; trans.u_shadow_softness = 0.35; trans.u_shadow_intensity = 0.95; trans.u_fog_density = 0.8; trans.u_fog_color = (0.1, 0.1, 0.15)
                elif preset == "tv_glow":
                    trans.u_light_pos = (0.5, 0.6); trans.u_light_color = (0.8, 0.9, 1.0); trans.u_light_intensity = 0.9; trans.u_light_radius = 0.7
                    trans.u_ambient_color = (0.3, 0.35, 0.45); trans.u_ambient_intensity = 0.25; trans.u_shadow_softness = 0.7; trans.u_shadow_intensity = 0.5; trans.u_fog_density = 0.2; trans.u_fog_color = (0.35, 0.4, 0.5)
        # Apply shader parts or clear
        if parts:
            trans.shader = parts
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] Combined shader parts: {parts}")
            except Exception:
                pass
        else:
            trans.shader = None
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print("[SHADER DEBUG] Combined shader parts: none")
            except Exception:
                pass
        return 0

    def shader_debug_and_setup(trans, st, at):
        """Transform function that logs shader states before ATL processing"""
        # Get current shader states and log them
        film_grain_transform = get_current_shader_transform("film_grain")
        fog_transform = get_current_shader_transform("fog")
        vintage_transform = get_current_shader_transform("vintage")
        
        try:
            from renpy.store import shader_debug_enabled
            if shader_debug_enabled:
                print(f"[SHADER DEBUG] Transform called: grain={film_grain_transform}, fog={fog_transform}, vintage={vintage_transform}")
        except Exception:
            pass
        
        # Return None to indicate no pause - this prevents ATLTransform comparison issues
        # Transform functions should return timing values, not ATLTransform objects
        return None
    
    def apply_film_grain_transform(trans, st, at):
        """Apply film grain transform based on current state"""
        current_state = shader_states["film_grain"]["current"]
        if current_state == 0:
            return None  # Off
        elif current_state == 1:
            # Apply subtle film grain
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] Applying subtle film grain")
            except Exception:
                pass
            return None  # We'll implement actual shader application later
        elif current_state == 2:
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] Applying moderate film grain")
            except Exception:
                pass
            return None
        elif current_state == 3:
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] Applying heavy film grain")
            except Exception:
                pass
            return None
        return None
    
    def apply_fog_transform(trans, st, at):
        """Apply fog transform based on current state"""
        current_state = shader_states["fog"]["current"]
        if current_state > 0:
            preset_name = shader_states["fog"]["presets"][current_state]
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] Applying fog effect: {preset_name}")
            except Exception:
                pass
        return None
    
    def apply_vintage_transform(trans, st, at):
        """Apply vintage transform based on current state"""
        current_state = shader_states["vintage"]["current"]
        if current_state > 0:
            preset_name = shader_states["vintage"]["presets"][current_state]
            print(f"[SHADER DEBUG] Applying vintage effect: {preset_name}")
        return None
    
    def get_and_apply_current_shader(trans, st, at):
        """Apply the most appropriate shader based on current states"""
        # Log current shader states
        film_grain_transform = get_current_shader_transform("film_grain")
        fog_transform = get_current_shader_transform("fog")
        vintage_transform = get_current_shader_transform("vintage")
        
        try:
            from renpy.store import shader_debug_enabled
            if shader_debug_enabled:
                print(f"[SHADER DEBUG] Checking shaders: grain={film_grain_transform}, fog={fog_transform}, vintage={vintage_transform}")
        except Exception:
            pass
        
        # Apply the first active shader we find
        # Priority: film grain > fog > vintage
        
        film_grain_state = shader_states["film_grain"]["current"]
        fog_state = shader_states["fog"]["current"]
        vintage_state = shader_states["vintage"]["current"]
        
        if film_grain_state > 0:
            # Apply film grain shader
            preset = shader_states["film_grain"]["presets"][film_grain_state]
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] APPLYING FILM GRAIN: {preset}")
            except Exception:
                pass
            
            # Set shader properties on the transform
            trans.mesh = True
            trans.shader = "film_grain_shader"
            
            if preset == "subtle":
                trans.u_grain_intensity = 0.02
                trans.u_grain_size = 120.0
            elif preset == "moderate":
                trans.u_grain_intensity = 0.05
                trans.u_grain_size = 100.0
            elif preset == "heavy":
                trans.u_grain_intensity = 0.1
                trans.u_grain_size = 80.0
            
            trans.u_time = st * 0.1  # Animate time
            
        elif fog_state > 0:
            # Apply fog shader
            preset = shader_states["fog"]["presets"][fog_state]
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] APPLYING FOG: {preset}")
            except Exception:
                pass
            
            trans.mesh = True
            trans.shader = "fog_shader"
            
            if preset == "light":
                trans.u_fog_density = 0.2
                trans.u_fog_height = 0.3
                trans.u_fog_color = (0.8, 0.8, 0.9)
            elif preset == "moderate":
                trans.u_fog_density = 0.4
                trans.u_fog_height = 0.5
                trans.u_fog_color = (0.7, 0.7, 0.8)
            elif preset == "heavy":
                trans.u_fog_density = 0.6
                trans.u_fog_height = 0.7
                trans.u_fog_color = (0.6, 0.6, 0.7)
            elif preset == "mysterious":
                trans.u_fog_density = 0.8
                trans.u_fog_height = 0.9
                trans.u_fog_color = (0.5, 0.5, 0.6)
            
            trans.u_time = st * 0.05  # Animate time for fog movement
            
        elif vintage_state > 0:
            # Apply vintage shader
            preset = shader_states["vintage"]["presets"][vintage_state]
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] APPLYING VINTAGE: {preset}")
            except Exception:
                pass
            
            trans.mesh = True
            trans.shader = "vintage_shader"
            
            if preset == "light":
                trans.u_sepia_intensity = 0.3
                trans.u_vintage_strength = 0.2
                trans.u_contrast = 1.1
                trans.u_brightness = -0.05
            elif preset == "moderate":
                trans.u_sepia_intensity = 0.6
                trans.u_vintage_strength = 0.4
                trans.u_contrast = 1.2
                trans.u_brightness = -0.1
            elif preset == "heavy":
                trans.u_sepia_intensity = 0.8
                trans.u_vintage_strength = 0.6
                trans.u_contrast = 1.3
                trans.u_brightness = -0.15
            elif preset == "noir":
                trans.u_sepia_intensity = 0.9
                trans.u_vintage_strength = 0.8
                trans.u_contrast = 1.5
                trans.u_brightness = -0.2
        
        else:
            # No shader active - make sure mesh and shader are cleared
            if hasattr(trans, 'mesh'):
                trans.mesh = False
            if hasattr(trans, 'shader'):
                trans.shader = None
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] No active shader")
            except Exception:
                pass
        
        return None
    
    def get_shader_debug_info():
        """Get debug information about current shader states"""
        info = {}
        for shader_name in shader_states:
            info[shader_name] = get_current_shader_transform(shader_name)
        return info
    
    def get_active_shader_transform():
        """Get the name of the currently active shader transform"""
        # Priority: film grain > fog > vintage
        film_grain_state = shader_states["film_grain"]["current"]
        fog_state = shader_states["fog"]["current"]
        vintage_state = shader_states["vintage"]["current"]
        
        if film_grain_state > 0:
            preset = shader_states["film_grain"]["presets"][film_grain_state]
            transform_name = f"film_grain_{preset}"
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] ACTIVE SHADER: {transform_name}")
            except Exception:
                pass
            return transform_name
        elif fog_state > 0:
            preset = shader_states["fog"]["presets"][fog_state]
            transform_name = f"fog_{preset}"
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] ACTIVE SHADER: {transform_name}")
            except Exception:
                pass
            return transform_name
        elif vintage_state > 0:
            preset = shader_states["vintage"]["presets"][vintage_state]
            transform_name = f"vintage_{preset}"
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] ACTIVE SHADER: {transform_name}")
            except Exception:
                pass
            return transform_name
        else:
            try:
                from renpy.store import shader_debug_enabled
                if shader_debug_enabled:
                    print(f"[SHADER DEBUG] NO ACTIVE SHADER")
            except Exception:
                pass
            return None
    
    def apply_shader_to_transform(transform_name, shader_effects=None):
        """Apply shader effects to a transform (placeholder for future implementation)"""
        # This will be expanded later to actually apply shader effects
        # For now, just return the original transform name
        return transform_name
    
    def get_hover_desaturation_transform(obj_data):
        """Get desaturation transform for hovered objects"""
        # Get desaturation parameters from object data
        pulse_speed = obj_data.get("desaturation_pulse_speed", obj_data.get("bloom_pulse_speed", 1.0))
        
        # Debug output
        try:
            if hasattr(store, 'bloom_debug_enabled') and store.bloom_debug_enabled:
                debug_bloom(f"Creating desaturation transform with pulse_speed={pulse_speed}")
        except:
            pass
        
        # Return the transform function that corresponds to the desaturation effect
        # We need to get the actual transform function, not the string name
        return object_desaturation_highlight
    
    def apply_desaturation_effect(trans, st, at, pulse_speed):
        """Apply desaturation effect with pulsing animation"""
        import math
        
        # Calculate pulsing saturation between 0.3 and 1.0
        cycle_time = pulse_speed * 2.0  # Full cycle time
        progress = (st % cycle_time) / cycle_time  # 0.0 to 1.0
        saturation_value = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(progress * 2 * math.pi))
        
        # Apply the matrix color transform
        trans.matrixcolor = renpy.display.matrix.SaturationMatrix(saturation_value)
        
        return None

# Function to auto-apply room-specific shaders
init python:
    def auto_apply_room_shaders():
        """Automatically apply appropriate shaders for the current room context"""
        # This can be expanded to set different defaults based on room
        # For now, it ensures shaders are ready
        pass
    
    def apply_room_shader_effects():
        """Get the current combined shader transform for room elements"""
        # This returns a transform that can be applied to any room element
        return "room_background_and_objects_with_shaders"
    
    def get_shader_transform_for_object(obj_name):
        """Get shader transform for specific objects, with possible overrides"""
        # Most objects use the standard room shaders
        # But evidence or special objects might override this
        
        # Check if this is an evidence object that needs special highlighting
        if hasattr(store, 'evidence_objects') and obj_name in store.evidence_objects:
            # Force edge detection for evidence when in evidence analysis mode
            if current_investigation_mode == 1:  # evidence_analysis_mode
                return "evidence_analysis_mode"
        
        # Default to room shaders
        return apply_room_shader_effects()

# Screen for full shader menu interface
screen shader_menu():
    modal True
    $ interactions_paused = True
    
    # Allow closing the menu with Escape
    key "game_menu" action [SetVariable("interactions_paused", False), Hide("shader_menu")]
    key "K_ESCAPE" action [SetVariable("interactions_paused", False), Hide("shader_menu")]
    
    if shader_menu_visible or renpy.get_screen("shader_menu"):
        
        frame:
            background "#000000ee"
            padding (20, 20)
            xalign 0.5 yalign 0.5
            xsize 1100 ysize 720
            
            vbox:
                spacing 12
                text "Shader Control Panel" size 36 color "#ffffff" text_align 0.5
                null height 6
                
                # Current preset labels
                $ cg_state = shader_states["color_grading"]["current"]
                $ li_state = shader_states["lighting"]["current"]
                $ cg_name = shader_states["color_grading"]["presets"][cg_state].replace('_', ' ').title()
                $ li_name = shader_states["lighting"]["presets"][li_state].replace('_', ' ').title()
                text "Color Grading: [cg_name]    |    Lighting: [li_name]" size 22 color "#ccccff" text_align 0.5
                null height 6

                # Scrollable content with a side scrollbar
                hbox:
                    spacing 10
                    viewport id "shader_menu_vp":
                        draggable True
                        mousewheel True
                        scrollbars "vertical"
                        xmaximum 1050
                        ymaximum 600
                        has vbox
                        spacing 16
                        
                        hbox:
                            spacing 30
                            
                            # Column 1: Color Grading
                            vbox:
                                spacing 12
                                text "Color Grading" size 24 color "#ffff00"
                                vbox:
                                    spacing 8
                                    for i, preset in enumerate(shader_states["color_grading"]["presets"]):
                                        $ is_current = (i == shader_states["color_grading"]["current"])
                                        textbutton preset.replace('_', ' ').title():
                                            action [
                                                SetDict(shader_states["color_grading"], "current", i),
                                                SetVariable("suppress_room_fade_once", True),
                                                Function(renpy.restart_interaction)
                                            ]
                                            text_color ("#ffff00" if is_current else "#cccccc")
                                            text_size 16
                            
                            # Column 2: Lighting
                            vbox:
                                spacing 12
                                text "Lighting" size 24 color "#ffff00"
                                vbox:
                                    spacing 8
                                    for i, preset in enumerate(shader_states["lighting"]["presets"]):
                                        $ is_current = (i == shader_states["lighting"]["current"])
                                        textbutton preset.replace('_', ' ').title():
                                            action [
                                                SetDict(shader_states["lighting"], "current", i),
                                                SetVariable("suppress_room_fade_once", True),
                                                Function(renpy.restart_interaction)
                                            ]
                                            text_color ("#ffff00" if is_current else "#cccccc")
                                            text_size 16
                                null height 10
                                hbox:
                                    spacing 10
                                    $ _li_anim = getattr(store,'lighting_animated', False)
                                    textbutton ("Animation: On" if _li_anim else "Animation: Off"):
                                        action [
                                            Function(lambda: setattr(store,'lighting_animated', not getattr(store,'lighting_animated', False))),
                                            Function(renpy.restart_interaction)
                                        ]
                                        text_color ("#ffff00" if _li_anim else "#cccccc")
                                        text_size 16
                                hbox:
                                    spacing 10
                                    text "Strength:" size 16 color "#ffffff" yalign 0.5
                                    bar value LightingStrengthValue() xsize 120
                                    text "Speed:" size 16 color "#ffffff" yalign 0.5
                                    bar value LightingSpeedValue() xsize 120
                            
                            # Column 3: Effects (Film Grain + CRT)
                            vbox:
                                spacing 12
                                text "Effects" size 24 color "#ffff00"
                                text "Film Grain" size 18 color "#ffffff"
                                vbox:
                                    spacing 8
                                    for i, preset in enumerate(shader_states["film_grain"]["presets"]):
                                        $ is_current = (i == shader_states["film_grain"]["current"])
                                        textbutton preset.title():
                                            action [
                                                SetDict(shader_states["film_grain"], "current", i),
                                                SetVariable("suppress_room_fade_once", True),
                                                Function(renpy.restart_interaction)
                                            ]
                                            text_color ("#ffff00" if is_current else "#cccccc")
                                            text_size 16
                                hbox:
                                    spacing 10
                                    text "Grain Downscale:" size 16 color "#ffffff" yalign 0.5
                                    bar value VariableValue("film_grain_downscale", 1.0, 3.0) xsize 200
                                null height 8
                                text "CRT" size 18 color "#ffffff"
                                hbox:
                                    spacing 10
                                    $ _crt_on = getattr(store, 'crt_enabled', False)
                                    textbutton ("On" if _crt_on else "Off"):
                                        action [
                                            Function(toggle_crt_effect),
                                            SetVariable("suppress_room_fade_once", True),
                                            Function(renpy.restart_interaction)
                                        ]
                                        text_color ("#ffff00" if _crt_on else "#cccccc")
                                        text_size 16
                                    $ _crt_anim = getattr(store, 'crt_animated', False)
                                    textbutton ("Animation: On" if _crt_anim else "Animation: Off"):
                                        action [
                                            Function(toggle_crt_animation),
                                            SetVariable("suppress_room_fade_once", True),
                                            Function(renpy.restart_interaction)
                                        ]
                                        text_color ("#ffff00" if _crt_anim else "#cccccc")
                                        text_size 16
                                null height 8
                                text "Debug" size 18 color "#ffffff"
                                hbox:
                                    spacing 10
                                    textbutton "Hover Logs":
                                        action Function(toggle_bloom_hover)
                                    textbutton "Help":
                                        action [
                                            ToggleVariable("shader_help_visible"),
                                            Function(renpy.restart_interaction)
                                        ]

                null height 12
                hbox:
                    spacing 20
                    xalign 0.5
                    textbutton "Reset All":
                        action Function(reset_all_shaders)
                        text_size 20
                    textbutton "Close":
                        action [SetVariable("interactions_paused", False), Hide("shader_menu")]
                        text_size 20

# Room noise overlay screen - applies film grain as full-screen effect
screen room_noise_overlay():
    # Only show noise overlay when film grain is active
    $ grain_state = shader_states["film_grain"]["current"]
    if grain_state > 0:
        $ preset = shader_states["film_grain"]["presets"][grain_state]
        
        # Full-screen noise overlay with different parameters per preset
        $ _fg_downscale = getattr(store, 'film_grain_downscale', 2.0)
        if preset == "subtle":
            add Solid("#00000000") at room_film_grain_overlay(grain_intensity=0.02, grain_size=120.0, downscale=_fg_downscale):
                xsize config.screen_width
                ysize config.screen_height
        elif preset == "moderate":
            add Solid("#00000000") at room_film_grain_overlay(grain_intensity=0.05, grain_size=100.0, downscale=_fg_downscale):
                xsize config.screen_width
                ysize config.screen_height
        elif preset == "heavy":
            add Solid("#00000000") at room_film_grain_overlay(grain_intensity=0.1, grain_size=80.0, downscale=_fg_downscale):
                xsize config.screen_width
                ysize config.screen_height

# Room fog overlay screen - applies fog as full-screen effect
screen room_fog_overlay():
    # Only show fog overlay when fog is active
    $ fog_state = shader_states["fog"]["current"]
    if fog_state > 0:
        $ preset = shader_states["fog"]["presets"][fog_state]
        
        # Full-screen fog overlay with different parameters per preset
        if preset == "light":
            add Solid("#00000000") at room_soft_fog_overlay(fog_scale=4.0, fog_speed=0.02, fog_coverage=0.6, fog_softness=0.3, overlay_opacity=0.12, fog_color=(0.85, 0.87, 0.92)):
                xsize config.screen_width
                ysize config.screen_height
        elif preset == "moderate":
            add Solid("#00000000") at room_soft_fog_overlay(fog_scale=3.5, fog_speed=0.03, fog_coverage=0.55, fog_softness=0.28, overlay_opacity=0.18, fog_color=(0.80, 0.82, 0.88)):
                xsize config.screen_width
                ysize config.screen_height
        elif preset == "heavy":
            add Solid("#00000000") at room_soft_fog_overlay(fog_scale=3.0, fog_speed=0.04, fog_coverage=0.5, fog_softness=0.25, overlay_opacity=0.25, fog_color=(0.75, 0.78, 0.85)):
                xsize config.screen_width
                ysize config.screen_height
        elif preset == "mysterious":
            add Solid("#00000000") at room_soft_fog_overlay(fog_scale=2.5, fog_speed=0.05, fog_coverage=0.45, fog_softness=0.22, overlay_opacity=0.32, fog_color=(0.70, 0.72, 0.80)):
                xsize config.screen_width
                ysize config.screen_height

# Film grain overlay transform for full-screen noise effect
transform room_film_grain_overlay(grain_intensity=0.05, grain_size=100.0, downscale=2.0):
    mesh True
    shader "film_grain_shader"
    u_grain_intensity grain_intensity
    u_grain_size grain_size
    u_grain_downscale downscale
    gl_texture_wrap (GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)
    u_lod_bias 0.0
    gl_mipmap True
    # Ensure continuous updates so u_time advances even when idle
    function film_grain_timepump

# Enhanced transform that intelligently applies shaders to different room elements
transform room_element_with_context_shaders(element_type="default"):
    # This can be used to apply different shader combinations based on element type
    # element_type could be "background", "character", "object", "evidence", etc.
    
    # Placeholder for context-aware shader application
    pass

# Fullscreen color grading overlay using neo-noir grading shader
transform overlay_neo_noir_grade(temperature=0.0, tint=0.0, saturation=1.0, contrast=1.0,
                                 brightness=0.0, gamma=1.0, color_filter=(1.0,1.0,1.0),
                                 shadow_tint=(1.0,1.0,1.0), highlight_tint=(1.0,1.0,1.0),
                                 vignette=0.0, film_grain=0.0):
    mesh True
    shader "neo_noir_color_grading"
    u_temperature temperature
    u_tint tint
    u_saturation saturation
    u_contrast contrast
    u_brightness brightness
    u_gamma gamma
    u_color_filter color_filter
    u_shadow_tint shadow_tint
    u_highlight_tint highlight_tint
    u_vignette vignette
    u_film_grain_amount film_grain
    gl_texture_wrap (GL_CLAMP_TO_EDGE, GL_CLAMP_TO_EDGE)
    u_lod_bias 0.0
    gl_mipmap True

# Screen to apply color grading as a post-processing overlay
screen color_grading_overlay():
    $ cg_state = shader_states["color_grading"]["current"] if "color_grading" in shader_states else 0
    if cg_state > 0:
        $ preset = shader_states["color_grading"]["presets"][cg_state]
        # Defaults
        $ temperature = 0.0; tint = 0.0; saturation = 1.0; contrast = 1.0; brightness = 0.0; gamma = 1.0
        $ color_filter = (1.0,1.0,1.0); shadow_tint = (1.0,1.0,1.0); highlight_tint = (1.0,1.0,1.0)
        $ vignette = 0.3; film_grain = 0.0
        if preset == "classic_noir":
            $ temperature = -0.2; tint = 0.0; saturation = 0.3; contrast = 1.4; brightness = -0.1; gamma = 1.1; color_filter=(0.95,0.95,1.05); vignette=0.4
        elif preset == "neon_night":
            $ temperature = 0.1; tint = 0.15; saturation = 1.3; contrast = 1.2; brightness = 0.0; color_filter=(1.1,0.9,1.2)
        elif preset == "rain_streets":
            $ temperature = -0.3; tint = -0.1; saturation = 0.7; contrast = 1.1; brightness = -0.05; color_filter=(0.9,1.0,1.1); vignette=0.5
        elif preset == "smoky_bar":
            $ temperature = 0.4; tint = 0.05; saturation = 0.8; contrast = 0.95; brightness = 0.05; gamma = 1.15; color_filter=(1.15,1.0,0.85); vignette=0.6
        elif preset == "miami_vice":
            $ temperature = 0.05; tint = 0.2; saturation = 1.4; contrast = 1.3; brightness = 0.1; gamma = 0.9; color_filter=(1.15,0.95,1.1); vignette=0.2
        elif preset == "detective_office":
            $ temperature = 0.2; tint = -0.05; saturation = 0.6; contrast = 1.05; brightness = -0.02; gamma = 1.2; color_filter=(1.05,1.0,0.9); vignette=0.35
        elif preset == "crime_scene":
            $ temperature = -0.15; tint = 0.0; saturation = 0.9; contrast = 1.25; brightness = 0.02; gamma = 0.95; color_filter=(1.1,0.95,0.95); vignette=0.3
        elif preset == "blade_runner":
            $ temperature = 0.15; tint = 0.1; saturation = 1.1; contrast = 1.15; brightness = -0.08; gamma = 1.1; color_filter=(1.2,1.0,0.85); vignette=0.45
        elif preset == "evidence_room":
            $ temperature = -0.05; tint = -0.1; saturation = 0.75; contrast = 1.0; brightness = 0.1; gamma = 0.95; color_filter=(0.98,1.02,0.95); vignette=0.15
        elif preset == "midnight_chase":
            $ temperature = -0.25; tint = 0.05; saturation = 0.85; contrast = 1.35; brightness = -0.12; gamma = 1.05; color_filter=(0.9,0.95,1.15); vignette=0.55
        add Solid("#0000") at overlay_neo_noir_grade(temperature, tint, saturation, contrast, brightness, gamma, color_filter, shadow_tint, highlight_tint, vignette, film_grain):
            xsize config.screen_width
            ysize config.screen_height
