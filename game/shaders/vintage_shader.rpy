# Vintage Sepia Shader
# Classic detective aesthetic with sepia tones and vignette
#
# Overview
# - Sepia tone conversion
# - Vintage contrast adjustment
# - Corner vignette for old film feel

init python hide:
    # Vintage Sepia Effect - classic detective aesthetic
    renpy.register_shader(
        "vintage_sepia",
        variables="""
        uniform float u_sepia_strength;
        uniform float u_sepia_contrast;
        uniform float u_vignette_intensity;
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
        
        // Convert to grayscale first
        float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
        
        // Apply sepia tone
        vec3 sepia = vec3(
            min(1.0, gray * (1.0 + 0.2 * u_sepia_strength) + 0.1 * u_sepia_strength),
            min(1.0, gray * (1.0 + 0.05 * u_sepia_strength) + 0.02 * u_sepia_strength),
            gray * (1.0 - 0.1 * u_sepia_strength)
        );
        
        // Mix original and sepia based on strength
        color.rgb = mix(color.rgb, sepia, u_sepia_strength);
        
        // Add vintage contrast
        color.rgb = (color.rgb - 0.5) * u_sepia_contrast + 0.5;
        
        // Add corner vignette for vintage feel
        vec2 center = v_tex_coord - 0.5;
        float dist = length(center);
        float vignette = 1.0 - smoothstep(0.3, 0.8, dist * u_vignette_intensity);
        color.rgb *= vignette;
        
        gl_FragColor = color;
        """
    )

# Transform definitions for vintage effects
transform vintage_sepia_effect(strength=0.7, contrast=1.2, vignette=1.5):
    mesh True
    shader "vintage_sepia"
    u_sepia_strength strength
    u_sepia_contrast contrast
    u_vignette_intensity vignette

transform light_sepia():
    mesh True
    shader "vintage_sepia"
    u_sepia_strength 0.4
    u_sepia_contrast 1.1
    u_vignette_intensity 1.2

transform heavy_sepia():
    mesh True
    shader "vintage_sepia"
    u_sepia_strength 0.9
    u_sepia_contrast 1.4
    u_vignette_intensity 2.0

transform noir_vintage():
    mesh True
    shader "vintage_sepia"
    u_sepia_strength 0.6
    u_sepia_contrast 1.6
    u_vignette_intensity 1.8
