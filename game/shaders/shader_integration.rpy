# Shader Integration with Bloom Support
# Core functions for integrating shaders with existing room and bloom system
#
# Overview
# - Provides functions to apply shaders to rooms and objects
# - Maintains compatibility with bloom and CRT systems
# - Works directly with existing room_background_and_objects screen

init python:
    # Store for shader states
    shader_states = {
        "film_grain": {"enabled": False, "preset": 0, "presets": ["off", "subtle", "moderate", "heavy"]},
        "fog": {"enabled": False, "preset": 0, "presets": ["off", "light", "moderate", "heavy", "mysterious"]},
        "vintage": {"enabled": False, "preset": 0, "presets": ["off", "light", "moderate", "heavy", "noir"]},
        "lighting": {"enabled": False, "preset": 0, "presets": ["off", "candlelight", "streetlight", "moonlight"]},
        "rain": {"enabled": False, "preset": 0, "presets": ["off", "drizzle", "moderate", "heavy", "storm"]},
        "depth_of_field": {"enabled": False, "preset": 0, "presets": ["off", "center", "left", "right", "close"]},
        "color_grading": {"enabled": False, "preset": 0, "presets": ["off", "cool", "warm", "noir", "vintage"]},
        "edge_detection": {"enabled": False, "preset": 0, "presets": ["off", "subtle", "evidence", "danger"]},
        "mystery_reveal": {"enabled": False, "preset": 0, "presets": ["off", "slow", "fast"]},
        "flashlight": {"enabled": False, "preset": 0, "presets": ["off", "narrow", "wide", "police", "detective"]}
    }
    
    # Atmosphere presets
    atmosphere_presets = [
        "none",
        "crime_scene_atmosphere",
        "abandoned_building_atmosphere", 
        "nighttime_street_atmosphere",
        "laboratory_atmosphere",
        "interrogation_room_atmosphere",
        "warehouse_atmosphere",
        "office_atmosphere",
        "alley_atmosphere",
        "stormy_night_atmosphere",
        "misty_morning_atmosphere",
        "sunset_atmosphere"
    ]
    
    # Investigation modes
    investigation_modes = [
        "none",
        "evidence_analysis_mode",
        "suspect_tracking_mode", 
        "memory_flashback_mode",
        "revelation_moment_mode"
    ]
    
    # Current states
    current_atmosphere_preset = 0
    current_investigation_mode = 0
    
    # Transform mapping from shader presets to actual transform names
    shader_transform_mapping = {
        # Film Grain mappings (use real film grain transforms)
        "film_grain_subtle": "subtle_grain",
        "film_grain_moderate": "moderate_grain",
        "film_grain_heavy": "heavy_grain",
        
        # Fog mappings (use real fog shaders)
        "fog_light": "light_fog",
        "fog_moderate": "atmospheric_fog_effect",
        "fog_heavy": "heavy_fog",
        "fog_mysterious": "mysterious_fog",
        
        # Edge detection mappings (use real edge shaders)
        "edge_detection_subtle": "subtle_edges",
        "edge_detection_evidence": "evidence_highlight",
        "edge_detection_danger": "danger_highlight",
        
        # Vintage/Sepia mappings (use real sepia shaders)
        "vintage_light": "light_sepia",
        "vintage_moderate": "vintage_sepia_effect", 
        "vintage_heavy": "heavy_sepia",
        "vintage_noir": "noir_vintage",
        
        # Lighting mappings (use dynamic lighting shaders)
        "lighting_candlelight": "candlelight_effect",
        "lighting_streetlight": "streetlight_effect",
        "lighting_moonlight": "moonlight_effect",
        
        # Rain mappings (enable weather controls)
        "rain_drizzle": "light_drizzle",
        "rain_moderate": "rain_effect",
        "rain_heavy": "heavy_rain",
        "rain_storm": "storm_rain",
    }

    def _resolve_transform(name_or_obj):
        """Return a callable transform object for a given name or object; None if not found."""
        try:
            # Already a transform-like object
            if name_or_obj is None:
                return None
            if not isinstance(name_or_obj, str):
                return name_or_obj
            # Lookup in renpy.store
            if hasattr(renpy.store, name_or_obj):
                return getattr(renpy.store, name_or_obj)
        except Exception as e:
            try:
                renpy.log(f"[ShaderIntegration] Resolve transform error for {name_or_obj}: {e}")
            except Exception:
                pass
        return None
    
    def apply_room_shader_effects():
        """Apply shader effects to the current room background, returning a transform object."""
        # Check for atmosphere preset first
        if current_atmosphere_preset > 0:
            preset_name = atmosphere_presets[current_atmosphere_preset]
            if preset_name != "none":
                return _resolve_transform(preset_name)
                
        # Check for investigation mode
        if current_investigation_mode > 0:
            mode_name = investigation_modes[current_investigation_mode] 
            if mode_name != "none":
                return _resolve_transform(mode_name)
                
        # Check individual shaders
        active_shaders = []
        for shader_name, state in shader_states.items():
            if state["enabled"] and state["preset"] > 0:
                preset_name = state["presets"][state["preset"]]
                mapping_key = f"{shader_name}_{preset_name}"
                
                # Look up the actual transform object
                if mapping_key in shader_transform_mapping:
                    return _resolve_transform(shader_transform_mapping[mapping_key])
                    
                # Fallback to old naming convention
                transform_name = f"{shader_name}_{preset_name}_effect"
                obj = _resolve_transform(transform_name)
                if obj:
                    return obj
                
                active_shaders.append((shader_name, preset_name))
                
        # Return first valid shader transform
        if active_shaders:
            shader_name, preset_name = active_shaders[0]
            mapping_key = f"{shader_name}_{preset_name}"
            if mapping_key in shader_transform_mapping:
                return _resolve_transform(shader_transform_mapping[mapping_key])
            
        return None
        
    def get_shader_transform_for_object(obj_name, obj_data):
        """Get appropriate shader transform for a specific object"""
        # Special cases for investigation modes
        if current_investigation_mode == 1:  # evidence_analysis_mode
            if obj_name in ["evidence", "clue", "document", "photo"]:
                return "evidence_highlight_mode"
        elif current_investigation_mode == 2:  # suspect_tracking_mode
            if obj_name in ["suspect_photo", "person", "character"]:
                return "suspect_tracking_mode"
        elif current_investigation_mode == 4:  # revelation_moment_mode
            if "important" in obj_data.get("tags", []):
                return "revelation_moment_mode"
        
        # Default to same as room
        return apply_room_shader_effects()
        
    def cycle_shader_preset(shader_name, direction=1):
        """Cycle through presets for a specific shader"""
        if shader_name not in shader_states:
            return
            
        state = shader_states[shader_name]
        state["preset"] = (state["preset"] + direction) % len(state["presets"])
        
        # Enable/disable based on preset
        if direction > 0 and state["preset"] == 1:
            state["enabled"] = True
        elif state["preset"] == 0:
            state["enabled"] = False
        else:
            state["enabled"] = True
            
        # Reset atmosphere and investigation modes when using individual shaders
        global current_atmosphere_preset, current_investigation_mode
        current_atmosphere_preset = 0
        current_investigation_mode = 0
        
        # Show notification
        show_shader_notification(shader_name, state["presets"][state["preset"]])
        renpy.restart_interaction()
        
    def cycle_atmosphere_preset(direction=1):
        """Cycle through atmosphere presets"""
        global current_atmosphere_preset, current_investigation_mode
        
        # Reset individual shaders when using atmosphere preset
        for shader_name in shader_states:
            shader_states[shader_name]["enabled"] = False
            shader_states[shader_name]["preset"] = 0
            
        # Reset investigation mode
        current_investigation_mode = 0
        
        # Cycle atmosphere preset
        current_atmosphere_preset = (current_atmosphere_preset + direction) % len(atmosphere_presets)
        preset_name = atmosphere_presets[current_atmosphere_preset]
        
        show_shader_notification("Atmosphere", preset_name)
        renpy.restart_interaction()
        
    def cycle_investigation_mode(direction=1):
        """Cycle through investigation modes"""
        global current_investigation_mode, current_atmosphere_preset
        
        # Reset individual shaders when using investigation mode
        for shader_name in shader_states:
            shader_states[shader_name]["enabled"] = False
            shader_states[shader_name]["preset"] = 0
            
        # Reset atmosphere preset
        current_atmosphere_preset = 0
        
        # Cycle investigation mode
        current_investigation_mode = (current_investigation_mode + direction) % len(investigation_modes)
        mode_name = investigation_modes[current_investigation_mode]
        
        show_shader_notification("Investigation", mode_name)
        renpy.restart_interaction()
        
    def reset_all_shaders():
        """Reset all shaders to default state"""
        global current_atmosphere_preset, current_investigation_mode
        
        for shader_name in shader_states:
            shader_states[shader_name]["enabled"] = False
            shader_states[shader_name]["preset"] = 0
            
        current_atmosphere_preset = 0
        current_investigation_mode = 0
        
        show_shader_notification("All Shaders", "Reset")
        renpy.restart_interaction()
        
    def show_shader_notification(shader_name, preset_name):
        """Show a brief notification about shader changes"""
        notification_text = f"{shader_name}: {preset_name}"
        renpy.show_screen("shader_notification", notification_text)

# Notification screen for shader changes
screen shader_notification(text):
    zorder 200
    timer 2.0 action Hide("shader_notification")
    
    frame:
        xalign 0.5
        yalign 0.1
        padding (20, 10)
        background "#000000cc"
        
        text text:
            color "#ffffff"
            size 24
            text_align 0.5

# Quick help screen
screen shader_quick_help():
    zorder 100
    modal False
    
    frame:
        xalign 0.02
        yalign 0.02
        padding (15, 10)
        background "#000000dd"
        
        vbox:
            text "Shader Controls" size 18 color "#ffff00"
            null height 5
            
            text "Shift+G - Film Grain" size 12 color "#cccccc"
            text "Shift+F - Fog Effects" size 12 color "#cccccc"
            text "Shift+V - Vintage/Sepia" size 12 color "#cccccc"
            text "Shift+L - Lighting" size 12 color "#cccccc"
            text "Shift+W - Weather/Rain" size 12 color "#cccccc"
            
            null height 5
            text "Alt+A - Atmosphere Presets" size 12 color "#cccccc"
            text "Alt+I - Investigation Modes" size 12 color "#cccccc"
            
            null height 5
            text "R - Reset All Effects" size 12 color "#cccccc"
            text "H - Toggle This Help" size 12 color "#cccccc"
            
            textbutton "Close" action Hide("shader_quick_help") text_size 12

# Enhanced shader controls integration
screen shader_enhanced_controls():
    if not hasattr(store, 'input_locked') or not input_locked:
        # Help toggle
        key "h" action [ToggleScreen("shader_quick_help"), renpy.curry(renpy.play)(["audio/ui/menu_toggle.wav"])]
        
        # Reset all shaders
        key "r" action Function(reset_all_shaders)
        
        # Individual shader cycling (Shift + Key)
        key "shift_K_g" action Function(cycle_shader_preset, "film_grain", 1)
        key "shift_K_f" action Function(cycle_shader_preset, "fog", 1)
        key "shift_K_v" action Function(cycle_shader_preset, "vintage", 1)
        key "shift_K_l" action Function(cycle_shader_preset, "lighting", 1)
        key "shift_K_w" action Function(cycle_shader_preset, "rain", 1)
        key "shift_K_d" action Function(cycle_shader_preset, "depth_of_field", 1)
        key "shift_K_c" action Function(cycle_shader_preset, "color_grading", 1)
        key "shift_K_e" action Function(cycle_shader_preset, "edge_detection", 1)
        key "shift_K_m" action Function(cycle_shader_preset, "mystery_reveal", 1)
        key "shift_K_t" action Function(cycle_shader_preset, "flashlight", 1)
        
        # Reverse cycling (Ctrl + Shift + Key)
        key "ctrl_shift_K_g" action Function(cycle_shader_preset, "film_grain", -1)
        key "ctrl_shift_K_f" action Function(cycle_shader_preset, "fog", -1)
        key "ctrl_shift_K_v" action Function(cycle_shader_preset, "vintage", -1)
        key "ctrl_shift_K_l" action Function(cycle_shader_preset, "lighting", -1)
        key "ctrl_shift_K_w" action Function(cycle_shader_preset, "rain", -1)
        key "ctrl_shift_K_d" action Function(cycle_shader_preset, "depth_of_field", -1)
        key "ctrl_shift_K_c" action Function(cycle_shader_preset, "color_grading", -1)
        key "ctrl_shift_K_e" action Function(cycle_shader_preset, "edge_detection", -1)
        key "ctrl_shift_K_m" action Function(cycle_shader_preset, "mystery_reveal", -1)
        key "ctrl_shift_K_t" action Function(cycle_shader_preset, "flashlight", -1)
        
        # Atmosphere and investigation mode cycling (Alt + Key)
        key "alt_K_a" action Function(cycle_atmosphere_preset, 1)
        key "alt_K_i" action Function(cycle_investigation_mode, 1)
        
        # Reverse atmosphere/investigation cycling
        key "ctrl_alt_K_a" action Function(cycle_atmosphere_preset, -1)
        key "ctrl_alt_K_i" action Function(cycle_investigation_mode, -1)
