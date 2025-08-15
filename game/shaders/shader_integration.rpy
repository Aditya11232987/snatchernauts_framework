# Shader Integration System
# Core system for managing all shader effects and hotkeys

init python:
    # Shader state management - only includes actively used shaders
    shader_states = {
        "film_grain": {"current": 0, "presets": ["off", "subtle", "moderate", "heavy"]},
        "lighting": {"current": 0, "presets": [
            "off",
            "street_lamp", "neon_signs", "window_blinds", "police_lights", "desk_lamp",
            "car_headlights", "interrogation", "sunset_window", "dark_alley", "tv_glow"
        ]},
        "color_grading": {"current": 0, "presets": [
            "off",
            "classic_noir", "neon_night", "rain_streets", "smoky_bar", "miami_vice",
            "detective_office", "crime_scene", "blade_runner", "evidence_room", "midnight_chase"
        ]}
    }
    
    # Atmosphere presets list
    atmosphere_presets = [
        "none", "crime_scene", "abandoned_building", "nighttime_street", 
        "laboratory", "interrogation_room", "warehouse", "office", 
        "alley", "stormy_night", "misty_morning", "sunset"
    ]
    
    # Investigation modes list  
    investigation_modes = [
        "none", "evidence_analysis", "suspect_tracking", 
        "memory_flashback", "revelation_moment"
    ]
    
    # Current preset indices
    current_atmosphere_preset = 0
    current_investigation_mode = 0
    
    # Shader help overlay state
    shader_help_visible = False
    shader_menu_visible = False
    
    # When True, the room_exploration_shaders screen should not re-run fade in
    suppress_room_fade_once = False

# Debug function for shader hotkeys
init python:
    shader_debug_enabled = False  # Set True to emit shader debug prints
    def debug_shader_key(key_name):
        """Debug function to log shader key presses"""
        if shader_debug_enabled:
            print(f"[SHADER DEBUG] Hotkey pressed: {key_name}")

# Functions for shader management
init python:
    def cycle_shader_effect(shader_name, reverse=False):
        """Cycle through presets for a specific shader effect"""
        global shader_states
        
        if shader_debug_enabled:
            print(f"[SHADER DEBUG] cycle_shader_effect called: {shader_name}, reverse={reverse}")
        
        if shader_name not in shader_states:
            if shader_debug_enabled:
                print(f"[SHADER DEBUG] ERROR: {shader_name} not found in shader_states")
            return
            
        state = shader_states[shader_name]
        presets = state["presets"]
        old_current = state["current"]
        
        if reverse:
            state["current"] = (state["current"] - 1) % len(presets)
        else:
            state["current"] = (state["current"] + 1) % len(presets)
            
        current_preset = presets[state["current"]]
        
        if shader_debug_enabled:
            print(f"[SHADER DEBUG] {shader_name}: {old_current} -> {state['current']} ({current_preset})")
        
        # Show notification
        renpy.show_screen("shader_notification", 
                         message=f"{shader_name.replace('_', ' ').title()}: {current_preset.title()}",
                         duration=2.0)
        
        # Prevent room fade re-trigger and refresh screen
        global suppress_room_fade_once
        suppress_room_fade_once = True
        renpy.restart_interaction()
    
    def cycle_atmosphere_preset(reverse=False):
        """Cycle through atmosphere presets"""
        global current_atmosphere_preset, atmosphere_presets
        
        old_preset = current_atmosphere_preset
        
        if reverse:
            current_atmosphere_preset = (current_atmosphere_preset - 1) % len(atmosphere_presets)
        else:
            current_atmosphere_preset = (current_atmosphere_preset + 1) % len(atmosphere_presets)
            
        preset_name = atmosphere_presets[current_atmosphere_preset]
        
        if shader_debug_enabled:
            print(f"[SHADER DEBUG] Atmosphere preset: {old_preset} -> {current_atmosphere_preset} ({preset_name})")
            print(f"[SHADER DEBUG] get_current_atmosphere_transform() returns: {get_current_atmosphere_transform()}")
        
        # Show notification
        renpy.show_screen("shader_notification",
                         message=f"Atmosphere: {preset_name.replace('_', ' ').title()}",
                         duration=2.0)
    
    def cycle_investigation_mode(reverse=False):
        """Cycle through investigation modes"""
        global current_investigation_mode, investigation_modes
        
        if reverse:
            current_investigation_mode = (current_investigation_mode - 1) % len(investigation_modes)
        else:
            current_investigation_mode = (current_investigation_mode + 1) % len(investigation_modes)
            
        mode_name = investigation_modes[current_investigation_mode]
        
        # Show notification  
        renpy.show_screen("shader_notification",
                         message=f"Investigation: {mode_name.replace('_', ' ').title()}",
                         duration=2.0)
    
    def reset_all_shaders():
        """Reset all shader effects to off state and refresh rendering"""
        global shader_states, current_atmosphere_preset, current_investigation_mode, suppress_room_fade_once, shader_debug_enabled
        
        # Zero out all shader states
        for shader_name in shader_states:
            try:
                old = shader_states[shader_name]["current"]
                shader_states[shader_name]["current"] = 0
                if shader_debug_enabled:
                    print(f"[SHADER RESET] {shader_name}: {old} -> 0")
            except Exception as e:
                print(f"[SHADER RESET] Failed to reset {shader_name}: {e}")
        
        # Reset atmosphere/investigation presets
        current_atmosphere_preset = 0
        current_investigation_mode = 0
        
        # Ensure CRT and related flags are disabled
        try:
            store.crt_enabled = False
            store.crt_animated = False
            # Reset vignette to defaults
            store.crt_vignette_strength = 0.35
            store.crt_vignette_width = 0.25
        except Exception:
            pass
        
        # Prevent room fade from re-triggering and force an interaction refresh
        suppress_room_fade_once = True
        
        # Show notification
        renpy.show_screen("shader_notification",
                         message="All Shaders Reset",
                         duration=2.0)
        
        # Refresh the scene so transforms are re-evaluated immediately
        renpy.restart_interaction()
    
    def get_current_shader_transform(shader_name):
        """Get the current transform for a shader effect"""
        if shader_name not in shader_states:
            return f"{shader_name}_off"
            
        state = shader_states[shader_name]
        current_preset = state["presets"][state["current"]]
        return f"{shader_name}_{current_preset}"
    
    def get_current_atmosphere_transform():
        """Get the current atmosphere preset transform"""
        preset_name = atmosphere_presets[current_atmosphere_preset]
        return f"{preset_name}_atmosphere"
    
    def get_current_investigation_transform():
        """Get the current investigation mode transform"""
        mode_name = investigation_modes[current_investigation_mode]
        return f"{mode_name}_investigation"
    
    def install_shader_system():
        """Initialize the shader system - call this at game start"""
        # Reset all states
        reset_all_shaders()
        
        # Log installation
        print("[SHADER] Shader system installed and ready")

# Hotkey definitions for shader controls
screen shader_hotkeys():
    # Core controls - using K_ prefix for proper Ren'Py key handling
    key "K_s" action [Function(debug_shader_key, "s"), ToggleScreen("shader_menu")]
    # Toggle shader debug prints quickly
    key "K_y" action ToggleVariable("shader_debug_enabled")
    key "K_h" action [Function(debug_shader_key, "h"), ToggleVariable("shader_help_visible")]  
    key "K_r" action [Function(debug_shader_key, "r"), Function(reset_all_shaders)]
    
    # Individual shader cycling (Shift+Key) - only for active shaders
    key ["K_LSHIFT", "K_g"] action [Function(debug_shader_key, "shift+g"), Function(cycle_shader_effect, "film_grain", False)]
    key ["K_LSHIFT", "K_l"] action [Function(debug_shader_key, "shift+l"), Function(cycle_shader_effect, "lighting", False)]
    key ["K_LSHIFT", "K_c"] action [Function(debug_shader_key, "shift+c"), Function(cycle_shader_effect, "color_grading", False)]
    
    # Reverse cycling (Ctrl+Shift+Key) - only for active shaders
    key ["K_LCTRL", "K_LSHIFT", "K_g"] action Function(cycle_shader_effect, "film_grain", True)
    key ["K_LCTRL", "K_LSHIFT", "K_l"] action Function(cycle_shader_effect, "lighting", True)
    key ["K_LCTRL", "K_LSHIFT", "K_c"] action Function(cycle_shader_effect, "color_grading", True)
    
    # Atmosphere and investigation presets
    key ["K_LALT", "K_a"] action [Function(debug_shader_key, "alt+a"), Function(cycle_atmosphere_preset, False)]
    key ["K_LALT", "K_i"] action [Function(debug_shader_key, "alt+i"), Function(cycle_investigation_mode, False)]
    key ["K_LCTRL", "K_LALT", "K_a"] action Function(cycle_atmosphere_preset, True)
    key ["K_LCTRL", "K_LALT", "K_i"] action Function(cycle_investigation_mode, True)

# Notification screen for shader changes
screen shader_notification(message, duration=2.0):
    timer duration action Hide("shader_notification")
    
    frame:
        background "#000080cc"
        padding (20, 10)
        xalign 0.5 yalign 0.1
        
        text message:
            color "#ffffff"
            size 24
            text_align 0.5

# Quick help overlay
screen shader_help():
    if shader_help_visible:
        modal True
        
        frame:
            background "#000000cc"
            padding (30, 30)
            xalign 0.5 yalign 0.5
            
            vbox:
                spacing 10
                
                text "Shader System Hotkeys" size 32 color "#ffffff" text_align 0.5
                null height 10
                
                hbox:
                    spacing 50
                    
                    vbox:
                        spacing 5
                        text "Core Controls:" size 24 color "#ffff00"
                        text "S - Shader Menu" size 18 color "#ffffff"
                        text "H - This Help" size 18 color "#ffffff"
                        text "R - Reset All" size 18 color "#ffffff"
                        
                        null height 10
                        
                        text "Active Effects (Shift+):" size 24 color "#ffff00"
                        text "G - Film Grain" size 18 color "#ffffff"
                        text "L - Lighting" size 18 color "#ffffff"
                        text "C - Color Grading" size 18 color "#ffffff"
                    
                    vbox:
                        spacing 5
                        text "Additional Controls:" size 24 color "#ffff00"
                        text "Y - Toggle Debug Output" size 18 color "#ffffff"
                        
                        null height 10
                        
                        text "Presets:" size 24 color "#ffff00"
                        text "Alt+A - Atmosphere" size 18 color "#ffffff"
                        text "Alt+I - Investigation" size 18 color "#ffffff"
                        
                        null height 10
                        
                        text "Reverse: Ctrl+Shift/Alt" size 18 color "#cccccc"
                
                null height 20
                
                textbutton "Close (H)" action ToggleVariable("shader_help_visible"):
                    xalign 0.5
