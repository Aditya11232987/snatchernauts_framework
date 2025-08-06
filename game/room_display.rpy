# Room Display System
# Background and object rendering utilities

# Include common utilities
include "common_utils.rpy"

# Display configuration
define ROOM_DISPLAY_CONFIG = {
    "fallback_background_color": "#000000",  # Pure black for smooth fade-in
    "default_background": "images/room1.png",
    "fade_duration": 2.0
}

# Smooth fade-in transform for room elements
transform room_fade_in(duration=2.0):
    alpha 0.0
    ease duration alpha 1.0

# No fade transform (for when room has already faded in)
transform room_no_fade():
    alpha 1.0

# Smooth fade-out transform for room elements
transform room_fade_out(duration=2.0):
    alpha 1.0
    ease duration alpha 0.0

# Immediate black background (no fade)
transform black_background():
    alpha 1.0

# CRT Shader Integration (from ~/Downloads/CRT_shaders.rpy)
init python hide:
    renpy.register_shader(
        "chroma_crt", # https://www.shadertoy.com/view/4dX3zN
        fragment_functions="""
        vec2 uuv(float wp, vec2 tex_coord)
    {
    // squared distance from center
    vec2 uvv = tex_coord;
    vec2 dc = 0.5-uvv;
    dc *= dc;

    // warp the fragment coordinates
    uvv -= .5; uvv *= 1.+(dc.yx*wp); uvv += .5;
    return uvv;
    }
""", variables="""
    uniform float u_warp;
    uniform float u_scan;
    uniform float u_chroma;
    uniform float u_scanline_size;
    uniform float u_scanline_offset;
    uniform vec2 u_model_size;
    uniform sampler2D tex0;
    attribute vec2 a_tex_coord;
    attribute vec4 a_position;
    varying vec2 v_tex_coord;
""", vertex_300="""
    //v_tex_coord = a_tex_coord;
    v_tex_coord = a_position.xy/u_model_size;
""", fragment_300="""
    vec2 uv = uuv(u_warp, v_tex_coord);

    #define PI 3.14159265359

    // outside boundaries is transparent
    if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
        gl_FragColor = vec4(0.0);
    } else {
        vec2 texra = texture2D(tex0, uv).ra;
        vec2 texga = texture2D(tex0, uuv(u_warp*u_chroma, v_tex_coord)).ga;
        vec2 texba = texture2D(tex0, uuv(u_warp*u_chroma*u_chroma, v_tex_coord)).ba;
        vec4 pure = vec4(texra.x, texga.x, texba.x, (texra.y+texga.y+texba.y)/3.);
        
        // Resolution-independent scanlines using fixed density
        // Calculate scanlines based on UV coordinates with consistent density
        float scanline_density = 200.0; // Fixed scanline density regardless of resolution
        float normalized_y = (uv.y * scanline_density) + u_scanline_offset;
        float scanline_pattern = sin(normalized_y * PI * u_scanline_size);
        float apply = pow(abs(scanline_pattern) * u_scan, 2.);
        
        // sample the texture
        gl_FragColor = mix(pure, vec4(0.0), apply);
    }
"""
)

# CRT Transform for individual elements
transform chroma_crt(warp=.2, scan=.5, chroma=.9, scanline_size=1.0):
    mesh True
    shader "chroma_crt"
    u_warp warp
    u_scan scan
    u_chroma chroma
    u_scanline_size scanline_size
    u_scanline_offset 0.0  # Static scanlines

# Animated CRT Transform with scrolling scanlines
transform animated_chroma_crt(base_warp=.2, base_scan=.5, base_chroma=.9, base_scanline_size=1.0, animation_intensity=0.1, animation_speed=2.0):
    mesh True
    shader "chroma_crt"
    # Keep these static - no animation
    u_warp base_warp
    u_scan base_scan
    u_chroma base_chroma
    u_scanline_size base_scanline_size
    
    # Animate scanline offset to create scrolling effect (like a TV)
    block:
        u_scanline_offset 0.0
        linear animation_speed u_scanline_offset (200.0 * animation_intensity)  # Scroll using scanline density
        repeat

# Static CRT Transform (no animation)
transform static_chroma_crt(warp=.2, scan=.5, chroma=.9, scanline_size=1.0):
    mesh True
    shader "chroma_crt"
    u_warp warp
    u_scan scan
    u_chroma chroma
    u_scanline_size scanline_size
    u_scanline_offset 0.0  # Static scanlines

# CRT Transform for whole layers (better for full-screen effects)
transform black_chroma_crt(child, warp=.2, scan=.5, chroma=.9, scanline_size=1.0):
    contains:
        "black"
    contains:
        At(child, chroma_crt(warp, scan, chroma, scanline_size))

init python:
    def get_room_background():
        """Get the current room background image"""
        if store.room_background:
            return store.room_background
        return ROOM_DISPLAY_CONFIG["default_background"]
    
    def get_fallback_background():
        """Get fallback background color"""
        return ROOM_DISPLAY_CONFIG["fallback_background_color"]
    
    def should_display_object(obj_data):
        """Check if an object should be displayed"""
        return "image" in obj_data
    
    def get_object_display_properties(obj_data):
        """Get display properties for an object"""
        return {
            "image": obj_data["image"],
            "xpos": obj_data["x"],
            "ypos": obj_data["y"],
            "xsize": obj_data["width"],
            "ysize": obj_data["height"]
        }
    
    # Mouse position is now available via get_mouse_position() from common_utils

# Combined screen for room background and objects on the same layer
screen room_background_and_objects():
    # Check if room has already faded in
    $ room_has_faded_in = getattr(store, 'room_has_faded_in', False)
    
    # Set timer to mark fade-in as complete after fade duration
    if not room_has_faded_in:
        timer ROOM_DISPLAY_CONFIG["fade_duration"] action SetVariable('room_has_faded_in', True)
    
    # Check if CRT effect should be applied
    if hasattr(store, 'crt_enabled') and store.crt_enabled:
        # Get CRT parameters with your specified defaults
        $ crt_warp = getattr(store, 'crt_warp', 0.2)
        $ crt_scan = getattr(store, 'crt_scan', 0.5) 
        $ crt_chroma = getattr(store, 'crt_chroma', 0.9)
        $ crt_scanline_size = getattr(store, 'crt_scanline_size', 1.0)
        
        # Apply static CRT shader to entire room content INCLUDING bloom effects
        frame at static_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size):
            background None
            
            # Black background that appears immediately (no fade)
            add get_fallback_background() at black_background()
            
            # Room background image with conditional fade-in effect
            if not room_has_faded_in:
                add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
            else:
                add get_room_background() at room_no_fade()
            
            # Display object images on the same layer as background with conditional fade-in effect
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
            
            # BLOOM EFFECTS INSIDE CRT FRAME - so they get warped with the objects
            use room_bloom_effects_internal
    else:
        # No CRT shader - normal display
        # Black background that appears immediately (no fade)
        add get_fallback_background() at black_background()
        
        # Room background image with conditional fade-in effect
        if not room_has_faded_in:
            add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
        else:
            add get_room_background() at room_no_fade()
        
        # Display object images on the same layer as background with conditional fade-in effect
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
        
        # BLOOM EFFECTS FOR NON-CRT MODE
        use room_bloom_effects_internal

# Legacy screen fragments maintained for backward compatibility
screen room_background():
    use room_background_and_objects

screen room_objects():
    # Empty - objects are now rendered in room_background_and_objects
    pass

# Internal bloom effects screen (used inside CRT frame)
screen room_bloom_effects_internal():
    # Show enhanced matrix-based bloom for hovered objects
    if current_hover_object and current_hover_object in room_objects:
        $ bloom_data = apply_bloom_to_object(room_objects[current_hover_object], current_hover_object, current_hover_object)
        
        if bloom_data:
            # Debug: Log color being used
            if config.developer:
                $ print("Bloom color for {}: {}".format(current_hover_object, bloom_data["color"]))
            
            # Create enhanced matrix-based bloom effect using global utilities
            add bloom_data["image"] at configurable_bloom(
                bloom_data["parameters"]["bloom_alpha_min"], 
                bloom_data["parameters"]["bloom_alpha_max"], 
                1.0/bloom_data["parameters"]["bloom_pulse_speed"]
            ):
                xpos bloom_data["dimensions"]["x"]
                ypos bloom_data["dimensions"]["y"]
                xsize bloom_data["dimensions"]["width"]
                ysize bloom_data["dimensions"]["height"]
                # Apply enhanced bloom with color tinting and brightness
                matrixcolor TintMatrix(bloom_data["color"]) * BrightnessMatrix(bloom_data["parameters"]["bloom_intensity"])
                blur bloom_data["parameters"]["blur_amount"]
                alpha bloom_data["parameters"]["bloom_alpha_max"] * room_objects[current_hover_object].get("bloom_softness", 0.7)

# External bloom effects screen (legacy/fallback for no CRT)
screen room_bloom_effects():
    # Only used when CRT is disabled - otherwise bloom is internal
    if not (hasattr(store, 'crt_enabled') and store.crt_enabled):
        use room_bloom_effects_internal

# Utility functions for display customization
init python:
    def set_fallback_background_color(color):
        """Set the fallback background color"""
        ROOM_DISPLAY_CONFIG["fallback_background_color"] = color
    
    def set_default_background(image_path):
        """Set the default background image"""
        ROOM_DISPLAY_CONFIG["default_background"] = image_path
    
    def hide_object(obj_name):
        """Temporarily hide an object from display"""
        if obj_name in store.room_objects:
            store.room_objects[obj_name]["_hidden"] = True
    
    def show_object(obj_name):
        """Show a previously hidden object"""
        if obj_name in store.room_objects:
            store.room_objects[obj_name]["_hidden"] = False
    
    def is_object_hidden(obj_data):
        """Check if an object is hidden"""
        return obj_data.get("_hidden", False)
