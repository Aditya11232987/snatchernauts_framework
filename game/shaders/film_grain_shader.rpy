# Film Grain Shader
# Adds texture and vintage feel to the detective game
#
# Overview
# - Procedural film grain effect
# - Adjustable strength and contrast
# - Animated grain pattern

init python hide:
    # Film Grain Effect - adds texture and vintage feel
    renpy.register_shader(
        "film_grain",
        fragment_functions="""
        float random(vec2 co) {
            return fract(sin(dot(co.xy, vec2(12.9898,78.233))) * 43758.5453);
        }
        
        float grain(vec2 uv, float time, float strength) {
            float noise = random(uv + vec2(time, time * 0.3));
            return mix(1.0, noise, strength);
        }
        """,
        variables="""
        uniform float u_grain_strength;
        uniform float u_grain_time;
        uniform float u_grain_contrast;
        uniform vec2 u_model_size;
        uniform sampler2D tex0;
        attribute vec2 a_tex_coord;
        attribute vec4 a_position;
        varying vec2 v_tex_coord;
        """,
        vertex_300="""
        v_tex_coord = a_position.xy/u_model_size;
        """,
        fragment_300="""
        vec4 color = texture2D(tex0, v_tex_coord);
        
        // Generate grain in [-1, 1] with larger grain pattern and slower animation
        float n = grain(v_tex_coord * 300.0, u_grain_time * 0.4, 1.0) * 2.0 - 1.0;
        
        // Apply additive grain so midtones don't crush
        color.rgb += n * u_grain_strength;
        
        // Apply contrast around mid-gray without darkening
        color.rgb = (color.rgb - 0.5) * (1.0 + u_grain_contrast) + 0.5;
        
        // Clamp to valid range
        color.rgb = clamp(color.rgb, 0.0, 1.0);
        
        gl_FragColor = color;
        """
    )

# Transform definitions for film grain
transform film_grain_effect(strength=0.1, contrast=0.2):
    mesh True
    shader "film_grain"
    u_grain_strength strength
    u_grain_contrast contrast
    block:
        u_grain_time 0.0
        linear 60.0 u_grain_time 60.0
        repeat

transform subtle_grain():
    mesh True
    shader "film_grain"
    u_grain_strength 0.08
    u_grain_contrast 0.15
    block:
        u_grain_time 0.0
        linear 60.0 u_grain_time 60.0
        repeat

transform moderate_grain():
    mesh True
    shader "film_grain"
    u_grain_strength 0.16
    u_grain_contrast 0.22
    block:
        u_grain_time 0.0
        linear 60.0 u_grain_time 60.0
        repeat

transform heavy_grain():
    mesh True
    shader "film_grain"
    u_grain_strength 0.25
    u_grain_contrast 0.35
    block:
        u_grain_time 0.0
        linear 60.0 u_grain_time 60.0
        repeat
