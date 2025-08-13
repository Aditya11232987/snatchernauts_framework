# Letterbox Shader
# Creates cinematic letterbox bars with smooth animations
# Renders above all content but below UI elements

# Letterbox shader definition
init python:
    # Register the letterbox shader with proper Ren'Py syntax (variables string + 300 stages)
    renpy.register_shader(
        "letterbox_shader",
        variables="""
            uniform float u_letterbox_height;
            uniform float u_letterbox_alpha;
            uniform vec3 u_letterbox_color;
            uniform vec2 u_model_size;
            uniform sampler2D tex0;
            attribute vec2 a_tex_coord;
            attribute vec4 a_position;
            varying vec2 v_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = a_position.xy / u_model_size;
        """,
        fragment_300="""
            // Calculate thresholds using normalized coordinates (0..1)
            float screen_height = max(u_model_size.y, 1.0);
            float bar_height_px = max(u_letterbox_height, 0.0);
            float frac = clamp(bar_height_px / screen_height, 0.0, 0.5);
            float top_threshold = frac;
            float bottom_threshold = 1.0 - frac;

            bool in_letterbox = (v_tex_coord.y < top_threshold || v_tex_coord.y > bottom_threshold);

            if (in_letterbox) {
                gl_FragColor = vec4(u_letterbox_color, u_letterbox_alpha);
            } else {
                gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
            }
        """
    )

# Letterbox animation transforms
transform letterbox_fade_in(duration=0.8):
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_alpha 0.0
    parallel:
        ease duration u_letterbox_alpha 1.0

transform letterbox_fade_out(duration=0.8):
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_alpha 1.0
    parallel:
        ease duration u_letterbox_alpha 0.0

transform letterbox_instant_on():
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_alpha 1.0

transform letterbox_instant_off():
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_alpha 0.0

# Dynamic letterbox transforms with configurable parameters
transform letterbox_dynamic_fade_in(duration=0.8, height=80, color=(0.0, 0.0, 0.0)):
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_color color
    u_letterbox_height 0.0
    u_letterbox_alpha 0.0
    parallel:
        ease duration u_letterbox_height height
    parallel:
        ease duration u_letterbox_alpha 1.0

transform letterbox_dynamic_fade_out(duration=0.8, height=80, color=(0.0, 0.0, 0.0)):
    mesh True
    shader "letterbox_shader"
    u_model_size (config.screen_width, config.screen_height)
    u_letterbox_color color
    u_letterbox_height height
    u_letterbox_alpha 1.0
    parallel:
        ease duration u_letterbox_height 0.0
    parallel:
        ease duration u_letterbox_alpha 0.0

# Letterbox control variables
default letterbox_shader_active = False
default letterbox_shader_height = 80.0
default letterbox_shader_color = (0.0, 0.0, 0.0)
default letterbox_shader_duration = 0.8

# Framework integration functions
init python:
    def show_letterbox_shader(duration=None, height=None, color=None, wait_for_animation=False):
        """Show letterbox effect using shader system.
        
        Args:
            duration: Animation duration in seconds (default: 0.8)
            height: Height of letterbox bars in pixels (default: 80.0)
            color: RGB color tuple for bars (default: (0.0, 0.0, 0.0))
            wait_for_animation: Whether to pause execution during animation
        """
        global letterbox_shader_active, letterbox_shader_height, letterbox_shader_color, letterbox_shader_duration
        
        if duration is None:
            duration = letterbox_shader_duration
        if height is None:
            height = letterbox_shader_height
        if color is None:
            color = letterbox_shader_color
            
        letterbox_shader_active = True
        letterbox_shader_height = height
        letterbox_shader_color = color
        letterbox_shader_duration = duration
        
        # Show the letterbox overlay screen if not already shown
        if not renpy.get_screen("letterbox_shader_overlay"):
            renpy.show_screen("letterbox_shader_overlay")
        
        # Restart interaction to trigger animations
        renpy.restart_interaction()
        
        # Wait for animation to complete if requested
        if wait_for_animation:
            renpy.pause(duration, hard=True)
            
        return
    
    def hide_letterbox_shader(duration=None, wait_for_animation=False):
        """Hide letterbox effect using shader system.
        
        Args:
            duration: Animation duration in seconds (default: 0.8)
            wait_for_animation: Whether to pause execution during animation
        """
        global letterbox_shader_active, letterbox_shader_duration
        
        if duration is None:
            duration = letterbox_shader_duration
            
        if not letterbox_shader_active:
            return
            
        letterbox_shader_active = False
        letterbox_shader_duration = duration
        
        # Trigger hide animations by restarting interaction
        if renpy.get_screen("letterbox_shader_overlay"):
            renpy.restart_interaction()
            
            # Wait for the fade-out animation to complete
            if wait_for_animation:
                renpy.pause(duration, hard=True)
            
            # Schedule screen removal after animation
            renpy.call_in_new_context("letterbox_shader_cleanup", duration)
        
        return
    
    def toggle_letterbox_shader():
        """Toggle letterbox shader on/off"""
        if letterbox_shader_active:
            hide_letterbox_shader()
        else:
            show_letterbox_shader()
    
    def set_letterbox_shader_params(height=None, color=None, duration=None):
        """Set letterbox shader parameters
        
        Args:
            height: Height of letterbox bars in pixels
            color: RGB color tuple for bars
            duration: Default animation duration
        """
        global letterbox_shader_height, letterbox_shader_color, letterbox_shader_duration
        
        if height is not None:
            letterbox_shader_height = height
        if color is not None:
            letterbox_shader_color = color  
        if duration is not None:
            letterbox_shader_duration = duration
        
        # Refresh the screen if letterbox is active
        if letterbox_shader_active and renpy.get_screen("letterbox_shader_overlay"):
            renpy.restart_interaction()

# Letterbox shader overlay screen (renders above content, below UI)
screen letterbox_shader_overlay():
    # High z-order to appear above room content but below UI (which is typically 100+)
    zorder 95
    
    # Full screen overlay with letterbox shader
    if letterbox_shader_active:
        add Solid("#0000") at letterbox_dynamic_fade_in(
            letterbox_shader_duration, 
            letterbox_shader_height, 
            letterbox_shader_color
        ):
            xsize config.screen_width
            ysize config.screen_height
    else:
        add Solid("#0000") at letterbox_dynamic_fade_out(
            letterbox_shader_duration, 
            letterbox_shader_height, 
            letterbox_shader_color
        ):
            xsize config.screen_width
            ysize config.screen_height

# Cleanup label for removing letterbox screen after fade-out
label letterbox_shader_cleanup(duration):
    $ renpy.pause(duration, hard=True)
    $ renpy.hide_screen("letterbox_shader_overlay")
    return

# Developer controls for testing letterbox shader
screen letterbox_shader_controls():
    if config.developer:
        zorder 200
        
        frame:
            xalign 0.98
            yalign 0.02
            padding (10, 5)
            background "#000000dd"
            
            vbox:
                text "Letterbox Shader" size 14 color "#ffffff"
                null height 5
                
                textbutton "Toggle" action Function(toggle_letterbox_shader) text_size 12
                
                hbox:
                    text "Height:" size 10 color "#cccccc"
                    textbutton "60" action Function(set_letterbox_shader_params, height=60.0) text_size 10
                    textbutton "80" action Function(set_letterbox_shader_params, height=80.0) text_size 10  
                    textbutton "100" action Function(set_letterbox_shader_params, height=100.0) text_size 10
                
                hbox:
                    text "Color:" size 10 color "#cccccc"
                    textbutton "Black" action Function(set_letterbox_shader_params, color=(0.0, 0.0, 0.0)) text_size 10
                    textbutton "Red" action Function(set_letterbox_shader_params, color=(0.5, 0.0, 0.0)) text_size 10

# Auto-add developer controls if in developer mode
init python:
    if config.developer:
        config.overlay_screens.append("letterbox_shader_controls")

# Integration with existing letterbox functions (backward compatibility)
init python:
    # Replace the existing letterbox functions with shader versions for seamless integration
    def show_letterbox(duration=None, wait_for_animation=True):
        """Backward compatibility wrapper for existing letterbox calls"""
        return show_letterbox_shader(duration=duration, wait_for_animation=wait_for_animation)
    
    def hide_letterbox(duration=None, wait_for_animation=True):
        """Backward compatibility wrapper for existing letterbox calls"""
        return hide_letterbox_shader(duration=duration, wait_for_animation=wait_for_animation)
    
    def toggle_letterbox():
        """Backward compatibility wrapper for existing letterbox calls"""
        return toggle_letterbox_shader()
