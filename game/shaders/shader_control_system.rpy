# Advanced Shader Control System
# Comprehensive hotkey management to avoid key conflicts
#
# Overview
# - Modifier key combinations (Shift+, Ctrl+, Alt+)
# - Cycling through shader presets with single keys
# - Dedicated shader menu for complex control
# - Context-sensitive shader switching

init python:
    # Shader state management
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
    
    # Composite atmosphere presets
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
    
    current_atmosphere_preset = 0
    current_investigation_mode = 0
    investigation_modes = [
        "none",
        "evidence_analysis_mode",
        "suspect_tracking_mode", 
        "memory_flashback_mode",
        "revelation_moment_mode"
    ]
    
    shader_menu_active = False
    shader_quick_help_visible = False
    
    def cycle_shader_preset(shader_name, direction=1):
        """Cycle through presets for a specific shader"""
        if shader_name not in shader_states:
            return
            
        state = shader_states[shader_name]
        state["preset"] = (state["preset"] + direction) % len(state["presets"])
        
        # Enable shader if cycling forward from "off"
        if direction > 0 and state["preset"] == 1:
            state["enabled"] = True
        # Disable shader if cycled to "off"
        elif state["preset"] == 0:
            state["enabled"] = False
        else:
            state["enabled"] = True
            
        apply_current_shader_preset(shader_name)
        show_shader_notification(shader_name, state["presets"][state["preset"]])
        
    def apply_current_shader_preset(shader_name):
        """Apply the current preset for a shader"""
        if shader_name not in shader_states:
            return
            
        state = shader_states[shader_name]
        preset_name = state["presets"][state["preset"]]
        
        # This would integrate with your existing shader application system
        # For now, we'll store the state and let the room system handle application
        renpy.restart_interaction()
        
    def cycle_atmosphere_preset(direction=1):
        """Cycle through atmosphere presets"""
        global current_atmosphere_preset
        current_atmosphere_preset = (current_atmosphere_preset + direction) % len(atmosphere_presets)
        preset_name = atmosphere_presets[current_atmosphere_preset]
        show_shader_notification("Atmosphere", preset_name)
        renpy.restart_interaction()
        
    def cycle_investigation_mode(direction=1):
        """Cycle through investigation modes"""
        global current_investigation_mode
        current_investigation_mode = (current_investigation_mode + direction) % len(investigation_modes)
        mode_name = investigation_modes[current_investigation_mode]
        show_shader_notification("Investigation Mode", mode_name)
        renpy.restart_interaction()
        
    def toggle_shader_menu():
        """Toggle the shader control menu"""
        global shader_menu_active
        shader_menu_active = not shader_menu_active
        if shader_menu_active:
            renpy.show_screen("shader_control_menu")
        else:
            renpy.hide_screen("shader_control_menu")
            
    def toggle_quick_help():
        """Toggle quick help overlay"""
        global shader_quick_help_visible
        shader_quick_help_visible = not shader_quick_help_visible
        if shader_quick_help_visible:
            renpy.show_screen("shader_quick_help")
        else:
            renpy.hide_screen("shader_quick_help")
            
    def show_shader_notification(shader_name, preset_name):
        """Show a brief notification about shader changes"""
        notification_text = f"{shader_name}: {preset_name}"
        renpy.show_screen("shader_notification", notification_text)
        
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
        
    def get_current_shader_transform():
        """Get the appropriate transform based on current shader states"""
        # This integrates with your existing room system
        if current_atmosphere_preset > 0:
            return atmosphere_presets[current_atmosphere_preset]
        elif current_investigation_mode > 0:
            return investigation_modes[current_investigation_mode]
        else:
            # Build custom transform based on individual shader states
            return build_custom_shader_transform()
            
    def build_custom_shader_transform():
        """Build a custom transform from individual shader states"""
        # This would create a composite transform based on enabled shaders
        enabled_effects = []
        for shader_name, state in shader_states.items():
            if state["enabled"] and state["preset"] > 0:
                preset_name = state["presets"][state["preset"]]
                enabled_effects.append((shader_name, preset_name))
        return enabled_effects

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

# Quick help overlay
screen shader_quick_help():
    zorder 100
    modal False
    
    frame:
        xalign 0.02
        yalign 0.02
        padding (15, 10)
        background "#000000dd"
        
        vbox:
            text "Shader Controls (Quick Help)" size 18 color "#ffff00"
            null height 5
            
            text "Basic Controls:" size 14 color "#ffffff"
            text "S - Shader Menu" size 12 color "#cccccc"
            text "H - Toggle This Help" size 12 color "#cccccc"
            text "R - Reset All Shaders" size 12 color "#cccccc"
            
            null height 8
            text "Cycling (Shift+Key):" size 14 color "#ffffff"
            text "Shift+G - Film Grain" size 12 color "#cccccc"
            text "Shift+F - Fog Effects" size 12 color "#cccccc"
            text "Shift+V - Vintage/Sepia" size 12 color "#cccccc"
            text "Shift+L - Lighting" size 12 color "#cccccc"
            text "Shift+R - Rain Effects" size 12 color "#cccccc"
            
            null height 8
            text "Atmosphere (Alt+Key):" size 14 color "#ffffff"
            text "Alt+A - Cycle Atmosphere" size 12 color "#cccccc"
            text "Alt+I - Investigation Mode" size 12 color "#cccccc"
            
            textbutton "Close (H)" action Function(toggle_quick_help) text_size 12

# Comprehensive shader control menu
screen shader_control_menu():
    zorder 150
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        padding (30, 20)
        background "#000000ee"
        
        vbox:
            hbox:
                text "Shader Control Center" size 28 color "#ffff00"
                null width 500
                textbutton "X" action Function(toggle_shader_menu) text_size 24
                
            null height 15
            
            hbox:
                # Left column - Individual Effects
                vbox:
                    xsize 350
                    text "Individual Effects" size 20 color "#ffffff"
                    null height 10
                    
                    for shader_name, state in shader_states.items():
                        hbox:
                            text shader_name.replace('_', ' ').title() size 14 color "#cccccc" xsize 140
                            
                            # Current preset display
                            text state["presets"][state["preset"]] size 14 color "#ffff88" xsize 80
                            
                            # Cycle buttons
                            textbutton "<" action Function(cycle_shader_preset, shader_name, -1) text_size 12
                            textbutton ">" action Function(cycle_shader_preset, shader_name, 1) text_size 12
                
                null width 50
                
                # Right column - Composite Presets  
                vbox:
                    xsize 350
                    text "Atmosphere Presets" size 20 color "#ffffff"
                    null height 10
                    
                    hbox:
                        text "Current:" size 14 color "#cccccc" xsize 70
                        text atmosphere_presets[current_atmosphere_preset] size 14 color "#ffff88" xsize 180
                        textbutton "<" action Function(cycle_atmosphere_preset, -1) text_size 12
                        textbutton ">" action Function(cycle_atmosphere_preset, 1) text_size 12
                    
                    null height 15
                    text "Investigation Modes" size 20 color "#ffffff"
                    null height 10
                    
                    hbox:
                        text "Current:" size 14 color "#cccccc" xsize 70
                        text investigation_modes[current_investigation_mode] size 14 color "#ffff88" xsize 180
                        textbutton "<" action Function(cycle_investigation_mode, -1) text_size 12
                        textbutton ">" action Function(cycle_investigation_mode, 1) text_size 12
                    
                    null height 30
                    
                    # Quick preset buttons
                    text "Quick Presets" size 18 color "#ffffff"
                    null height 10
                    
                    grid 2 3:
                        spacing 5
                        textbutton "Crime Scene" action [SetVariable("current_atmosphere_preset", 1), Function(toggle_shader_menu)] text_size 12
                        textbutton "Noir Alley" action [SetVariable("current_atmosphere_preset", 8), Function(toggle_shader_menu)] text_size 12
                        textbutton "Stormy Night" action [SetVariable("current_atmosphere_preset", 9), Function(toggle_shader_menu)] text_size 12
                        textbutton "Laboratory" action [SetVariable("current_atmosphere_preset", 4), Function(toggle_shader_menu)] text_size 12
                        textbutton "Office" action [SetVariable("current_atmosphere_preset", 7), Function(toggle_shader_menu)] text_size 12
                        textbutton "Reset All" action Function(reset_all_shaders) text_size 12
            
            null height 20
            
            hbox:
                xalign 0.5
                textbutton "Apply & Close" action Function(toggle_shader_menu) text_size 16
                null width 20
                textbutton "Reset All" action Function(reset_all_shaders) text_size 16

# Enhanced shader control integration for room exploration screen
screen shader_enhanced_controls():
    # This gets added to your main room exploration screen
    if not input_locked:
        # Shader Menu Toggle
        key "s" action Function(toggle_shader_menu)
        
        # Quick Help Toggle  
        key "h" action Function(toggle_quick_help)
        
        # Reset All Shaders
        key "r" action Function(reset_all_shaders)
        
        # Individual Shader Cycling (Shift + Key)
        key "shift_K_g" action Function(cycle_shader_preset, "film_grain", 1)
        key "shift_K_f" action Function(cycle_shader_preset, "fog", 1) 
        key "shift_K_v" action Function(cycle_shader_preset, "vintage", 1)
        key "shift_K_l" action Function(cycle_shader_preset, "lighting", 1)
        key "shift_K_w" action Function(cycle_shader_preset, "rain", 1)  # W for weather
        key "shift_K_d" action Function(cycle_shader_preset, "depth_of_field", 1)
        key "shift_K_c" action Function(cycle_shader_preset, "color_grading", 1)
        key "shift_K_e" action Function(cycle_shader_preset, "edge_detection", 1)
        key "shift_K_m" action Function(cycle_shader_preset, "mystery_reveal", 1)
        key "shift_K_t" action Function(cycle_shader_preset, "flashlight", 1)  # T for torch
        
        # Reverse Cycling (Ctrl + Shift + Key)
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
        
        # Atmosphere and Investigation Mode Cycling (Alt + Key)
        key "alt_K_a" action Function(cycle_atmosphere_preset, 1)
        key "alt_K_i" action Function(cycle_investigation_mode, 1)
        
        # Reverse Atmosphere Cycling (Ctrl + Alt + Key)
        key "ctrl_alt_K_a" action Function(cycle_atmosphere_preset, -1)
        key "ctrl_alt_K_i" action Function(cycle_investigation_mode, -1)

# Function to integrate shader system with existing room display
init python:
    def get_room_shader_transform():
        """Get the appropriate shader transform for the current room state"""
        # Check for active atmosphere preset first
        if current_atmosphere_preset > 0:
            preset_name = atmosphere_presets[current_atmosphere_preset]
            if preset_name != "none":
                return preset_name
                
        # Check for active investigation mode
        if current_investigation_mode > 0:
            mode_name = investigation_modes[current_investigation_mode] 
            if mode_name != "none":
                return mode_name
                
        # If no presets active, check individual shaders
        active_shaders = []
        for shader_name, state in shader_states.items():
            if state["enabled"] and state["preset"] > 0:
                preset_name = state["presets"][state["preset"]]
                active_shaders.append((shader_name, preset_name))
                
        if active_shaders:
            return ("custom", active_shaders)
            
        return None

# Integration example for your existing room system
label example_shader_integration:
    scene bg room1
    
    # Apply current shader settings
    $ current_transform = get_room_shader_transform()
    if current_transform:
        if isinstance(current_transform, str):
            # It's a preset name
            show bg room1 at expression(current_transform)
        elif current_transform[0] == "custom":
            # It's a custom combination - would need custom handling
            pass
    
    "The room appears before you with the current atmospheric effects."
    return
