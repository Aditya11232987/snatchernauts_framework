# Letterbox Shader V2 - Speed-Based System
# Creates cinematic letterbox bars with 5 animation speed options
# Integrates with the neo-noir shader layer system

# Letterbox state variables
default letterbox_enabled = False
default letterbox_speed_mode = 2  # 0=very slow, 1=slow, 2=normal, 3=fast, 4=very fast
default letterbox_height = 80.0
default letterbox_color = (0.0, 0.0, 0.0)  # Black bars
default _letterbox_was_enabled = False  # Track previous state for animations

init python:
    # Letterbox speed configuration (duration in seconds)
    letterbox_speeds = {
        0: {"name": "Very Slow", "duration": 2.5},
        1: {"name": "Slow", "duration": 1.5}, 
        2: {"name": "Normal", "duration": 0.8},
        3: {"name": "Fast", "duration": 0.4},
        4: {"name": "Very Fast", "duration": 0.2}
    }
    
    def get_letterbox_duration():
        """Get current letterbox animation duration based on speed mode"""
        return letterbox_speeds.get(letterbox_speed_mode, letterbox_speeds[2])["duration"]
    
    def get_letterbox_speed_name():
        """Get current letterbox speed name for notifications"""
        return letterbox_speeds.get(letterbox_speed_mode, letterbox_speeds[2])["name"]
    
    def cycle_letterbox_speed():
        """Cycle through letterbox speed options"""
        global letterbox_speed_mode
        letterbox_speed_mode = (letterbox_speed_mode + 1) % len(letterbox_speeds)
        
        # Show notification
        speed_name = get_letterbox_speed_name()
        renpy.notify(f"Letterbox Speed: {speed_name}")
    
    def toggle_letterbox():
        """Toggle letterbox on/off with current speed setting"""
        global letterbox_enabled
        letterbox_enabled = not letterbox_enabled
        
        # Show notification
        if letterbox_enabled:
            speed_name = get_letterbox_speed_name()
            renpy.notify(f"Letterbox ON ({speed_name})")
        else:
            renpy.notify("Letterbox OFF")
        
        # Restart interaction to apply changes
        renpy.restart_interaction()
    
    def letterbox_combined_action():
        """Combined action for 'l' key: toggle letterbox or cycle speed only on ease-in"""
        global letterbox_enabled, letterbox_speed_mode, _letterbox_was_enabled
        
        # Update the previous state tracker
        _letterbox_was_enabled = letterbox_enabled
        
        if not letterbox_enabled:
            # Cycle to next speed before turning on (ease-in with new speed)
            letterbox_speed_mode = (letterbox_speed_mode + 1) % len(letterbox_speeds)
            letterbox_enabled = True
            speed_name = get_letterbox_speed_name()
            renpy.notify(f"Letterbox ON ({speed_name})")
            renpy.restart_interaction()
        else:
            # Turn off letterbox (ease-out) - no speed change
            letterbox_enabled = False
            renpy.notify("Letterbox OFF")
            renpy.restart_interaction()
    
    def set_letterbox_speed(speed_index):
        """Set letterbox speed to specific index (0-4)"""
        global letterbox_speed_mode
        if 0 <= speed_index < len(letterbox_speeds):
            letterbox_speed_mode = speed_index
            speed_name = get_letterbox_speed_name()
            
            if letterbox_enabled:
                renpy.notify(f"Letterbox Speed: {speed_name}")
                renpy.restart_interaction()
    
    def letterbox_force_off():
        """Force letterbox off regardless of current state"""
        global letterbox_enabled
        if letterbox_enabled:
            letterbox_enabled = False
            renpy.notify("Letterbox OFF")
            
            # Hide overlay after animation
            duration = get_letterbox_duration()
            renpy.call_in_new_context("letterbox_cleanup", duration)
            renpy.restart_interaction()

# Enhanced letterbox shader with smooth ease-in/out animations
transform letterbox_ease_in(duration=0.8, height=80.0, color=(0.0, 0.0, 0.0)):
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_color color
    u_letterbox_height 0.0
    u_letterbox_alpha 0.0
    
    # Parallel animations for smooth effect
    parallel:
        # Ease in the height with smooth easing
        easein_quart duration u_letterbox_height height
    parallel:
        # Fade in the alpha slightly faster for better visual flow
        ease (duration * 0.7) u_letterbox_alpha 1.0

transform letterbox_ease_out(duration=0.8, height=80.0, color=(0.0, 0.0, 0.0)):
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_color color
    u_letterbox_height height
    u_letterbox_alpha 1.0
    
    # Parallel animations for smooth effect
    parallel:
        # Ease out the height with smooth easing
        easeout_quart duration u_letterbox_height 0.0
    parallel:
        # Fade out the alpha slightly slower for better visual flow
        ease (duration * 1.3) u_letterbox_alpha 0.0

transform letterbox_static(height=80.0, color=(0.0, 0.0, 0.0)):
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_color color
    u_letterbox_height height
    u_letterbox_alpha 1.0

# Transform that applies letterbox effect with current settings
# Note: This transform is not used directly - the shader layer system 
# calls letterbox_ease_in/out transforms directly based on letterbox_enabled state

# Speed preset transforms for quick access
transform letterbox_very_slow_in():
    letterbox_ease_in(2.5, letterbox_height, letterbox_color)

transform letterbox_slow_in():
    letterbox_ease_in(1.5, letterbox_height, letterbox_color)

transform letterbox_normal_in():
    letterbox_ease_in(0.8, letterbox_height, letterbox_color)

transform letterbox_fast_in():
    letterbox_ease_in(0.4, letterbox_height, letterbox_color)

transform letterbox_very_fast_in():
    letterbox_ease_in(0.2, letterbox_height, letterbox_color)

transform letterbox_very_slow_out():
    letterbox_ease_out(2.5, letterbox_height, letterbox_color)

transform letterbox_slow_out():
    letterbox_ease_out(1.5, letterbox_height, letterbox_color)

transform letterbox_normal_out():
    letterbox_ease_out(0.8, letterbox_height, letterbox_color)

transform letterbox_fast_out():
    letterbox_ease_out(0.4, letterbox_height, letterbox_color)

transform letterbox_very_fast_out():
    letterbox_ease_out(0.2, letterbox_height, letterbox_color)

# Letterbox overlay screen (renders above all content)
screen letterbox_overlay():
    # High z-order to appear above all content
    zorder 95
    
    # Show overlay for both ease-in and ease-out animations
    if letterbox_enabled:
        # Ease-in animation when turning on
        add Solid("#0000") at letterbox_ease_in(
            get_letterbox_duration(), 
            letterbox_height, 
            letterbox_color
        ):
            xsize config.screen_width
            ysize config.screen_height
    else:
        # Ease-out animation when turning off (only if we were previously on)
        $ was_enabled = getattr(store, '_letterbox_was_enabled', False)
        if was_enabled:
            add Solid("#0000") at letterbox_ease_out(
                get_letterbox_duration(), 
                letterbox_height, 
                letterbox_color
            ):
                xsize config.screen_width
                ysize config.screen_height
            
            # Clear the was_enabled flag after the animation duration
            timer get_letterbox_duration() action SetVariable('_letterbox_was_enabled', False)

# Cleanup label for removing letterbox screen after fade-out
label letterbox_cleanup(duration):
    $ renpy.pause(duration, hard=True)
    $ renpy.hide_screen("letterbox_overlay")
    return
