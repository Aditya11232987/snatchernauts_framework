# Edge Detection Shader
# Highlight important outlines and details using Sobel edge detection
#
# Overview
# - Sobel edge detection algorithm
# - Adjustable edge strength and threshold
# - Customizable edge color overlay

init python hide:
    # Edge Detection - highlight important outlines
    renpy.register_shader(
        "edge_detection",
        variables="""
        uniform float u_edge_strength;
        uniform vec3 u_edge_color;
        uniform float u_edge_threshold;
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
        vec2 texel_size = 1.0 / u_model_size;
        
        // Sample surrounding pixels
        vec3 tl = texture2D(tex0, v_tex_coord + vec2(-texel_size.x, -texel_size.y)).rgb;
        vec3 tm = texture2D(tex0, v_tex_coord + vec2(0.0, -texel_size.y)).rgb;
        vec3 tr = texture2D(tex0, v_tex_coord + vec2(texel_size.x, -texel_size.y)).rgb;
        vec3 ml = texture2D(tex0, v_tex_coord + vec2(-texel_size.x, 0.0)).rgb;
        vec3 center = texture2D(tex0, v_tex_coord).rgb;
        vec3 mr = texture2D(tex0, v_tex_coord + vec2(texel_size.x, 0.0)).rgb;
        vec3 bl = texture2D(tex0, v_tex_coord + vec2(-texel_size.x, texel_size.y)).rgb;
        vec3 bm = texture2D(tex0, v_tex_coord + vec2(0.0, texel_size.y)).rgb;
        vec3 br = texture2D(tex0, v_tex_coord + vec2(texel_size.x, texel_size.y)).rgb;
        
        // Sobel edge detection
        vec3 gx = -tl + tr - 2.0*ml + 2.0*mr - bl + br;
        vec3 gy = -tl - 2.0*tm - tr + bl + 2.0*bm + br;
        
        float edge = length(gx) + length(gy);
        edge = smoothstep(u_edge_threshold, u_edge_threshold + 0.1, edge);
        
        // Blend edge with original
        vec4 original = texture2D(tex0, v_tex_coord);
        vec3 edge_overlay = mix(original.rgb, u_edge_color, edge * u_edge_strength);
        
        gl_FragColor = vec4(edge_overlay, original.a);
        """
    )

# Transform definitions for edge detection
transform edge_detection_effect(strength=0.5, color=(1.0, 1.0, 1.0), threshold=0.1):
    mesh True
    shader "edge_detection"
    u_edge_strength strength
    u_edge_color color
    u_edge_threshold threshold

transform subtle_edges():
    mesh True
    shader "edge_detection"
    u_edge_strength 0.3
    u_edge_color (0.9, 0.9, 1.0)
    u_edge_threshold 0.15

transform strong_edges():
    mesh True
    shader "edge_detection"
    u_edge_strength 0.8
    u_edge_color (1.0, 1.0, 1.0)
    u_edge_threshold 0.08

transform evidence_highlight():
    mesh True
    shader "edge_detection"
    u_edge_strength 0.6
    u_edge_color (1.0, 1.0, 0.5)
    u_edge_threshold 0.1

transform danger_highlight():
    mesh True
    shader "edge_detection"
    u_edge_strength 0.7
    u_edge_color (1.0, 0.5, 0.5)
    u_edge_threshold 0.12
