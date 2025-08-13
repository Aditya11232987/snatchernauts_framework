# Mystery Reveal Shader
# Gradually uncover hidden elements with organic reveal patterns
#
# Overview
# - Progressive reveal from center point
# - Noise-based organic reveal pattern
# - Smooth transition between hidden and revealed states

init python hide:
    # Mystery Reveal Effect - gradually uncover hidden elements
    renpy.register_shader(
        "mystery_reveal",
        fragment_functions="""
        float noise(vec2 uv) {
            return fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453);
        }
        
        float fbm(vec2 uv, float time) {
            float value = 0.0;
            float amplitude = 0.5;
            for(int i = 0; i < 4; i++) {
                value += amplitude * noise(uv * pow(2.0, float(i)) + time);
                amplitude *= 0.5;
            }
            return value;
        }
        """,
        variables="""
        uniform float u_reveal_progress;
        uniform float u_reveal_time;
        uniform vec2 u_reveal_center;
        uniform float u_reveal_radius;
        uniform vec3 u_hidden_color;
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
        vec4 original = texture2D(tex0, v_tex_coord);
        
        // Calculate distance from reveal center
        float dist = distance(v_tex_coord, u_reveal_center);
        
        // Add noise for organic reveal pattern
        float noise_val = fbm(v_tex_coord * 10.0, u_reveal_time * 0.5);
        
        // Calculate reveal mask
        float reveal_threshold = u_reveal_progress * u_reveal_radius;
        float reveal_mask = smoothstep(reveal_threshold - 0.1, reveal_threshold + 0.1, 
                                      dist + noise_val * 0.2);
        
        // Mix between hidden and revealed
        vec3 result = mix(original.rgb, u_hidden_color, reveal_mask);
        
        gl_FragColor = vec4(result, original.a);
        """
    )

# Transform definitions for mystery reveal
transform mystery_reveal_effect(progress=0.0, center=(0.5, 0.5), radius=1.0, 
                               hidden_color=(0.0, 0.0, 0.0)):
    mesh True
    shader "mystery_reveal"
    u_reveal_progress progress
    u_reveal_center center
    u_reveal_radius radius
    u_hidden_color hidden_color
    block:
        u_reveal_time 0.0
        linear 20.0 u_reveal_time 20.0
        repeat

transform animated_mystery_reveal(center=(0.5, 0.5), radius=1.0, duration=3.0):
    mesh True
    shader "mystery_reveal"
    u_reveal_center center
    u_reveal_radius radius
    u_hidden_color (0.0, 0.0, 0.0)
    parallel:
        u_reveal_progress 0.0
        linear duration u_reveal_progress 1.0
    parallel:
        u_reveal_time 0.0
        linear 20.0 u_reveal_time 20.0
        repeat

transform slow_reveal():
    mesh True
    shader "mystery_reveal"
    u_reveal_center (0.5, 0.5)
    u_reveal_radius 1.2
    u_hidden_color (0.1, 0.1, 0.15)
    parallel:
        u_reveal_progress 0.0
        linear 5.0 u_reveal_progress 1.0
    parallel:
        u_reveal_time 0.0
        linear 20.0 u_reveal_time 20.0
        repeat

transform fast_reveal():
    mesh True
    shader "mystery_reveal"
    u_reveal_center (0.5, 0.5)
    u_reveal_radius 0.8
    u_hidden_color (0.0, 0.0, 0.0)
    parallel:
        u_reveal_progress 0.0
        linear 1.5 u_reveal_progress 1.0
    parallel:
        u_reveal_time 0.0
        linear 20.0 u_reveal_time 20.0
        repeat
