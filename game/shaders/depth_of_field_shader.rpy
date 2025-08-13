# Depth of Field Shader
# Focus attention on important elements through selective blur
#
# Overview
# - Selective focus based on distance from focus point
# - Gaussian blur for out-of-focus areas
# - Smooth transition between sharp and blurred regions

init python hide:
    # Depth of Field Effect - focus attention on important elements
    renpy.register_shader(
        "depth_of_field",
        fragment_functions="""
        vec4 sampleBlur(sampler2D tex, vec2 uv, float radius, vec2 tex_size) {
            vec4 result = vec4(0.0);
            float total_weight = 0.0;
            vec2 texel_size = 1.0 / tex_size;
            
            // 9-tap blur kernel
            for (int x = -1; x <= 1; x++) {
                for (int y = -1; y <= 1; y++) {
                    vec2 offset = vec2(float(x), float(y)) * texel_size * radius;
                    float weight = 1.0; // Uniform weight for simplicity
                    result += texture2D(tex, uv + offset) * weight;
                    total_weight += weight;
                }
            }
            return result / total_weight;
        }
        
        float calculateFocus(vec2 uv, vec2 focus_point, float focus_range) {
            float dist = distance(uv, focus_point);
            return smoothstep(focus_range * 0.5, focus_range, dist);
        }
        """,
        variables="""
        uniform vec2 u_focus_point;
        uniform float u_focus_range;
        uniform float u_blur_strength;
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
        vec4 sharp = texture2D(tex0, v_tex_coord);
        vec4 blurred = sampleBlur(tex0, v_tex_coord, u_blur_strength, u_model_size);
        
        float focus_factor = calculateFocus(v_tex_coord, u_focus_point, u_focus_range);
        gl_FragColor = mix(sharp, blurred, focus_factor);
        """
    )

# Transform definitions for depth of field
transform depth_of_field_effect(focus_point=(0.5, 0.5), focus_range=0.3, blur_strength=2.0):
    mesh True
    shader "depth_of_field"
    u_focus_point focus_point
    u_focus_range focus_range
    u_blur_strength blur_strength

transform center_focus():
    mesh True
    shader "depth_of_field"
    u_focus_point (0.5, 0.5)
    u_focus_range 0.25
    u_blur_strength 1.5

transform left_focus():
    mesh True
    shader "depth_of_field"
    u_focus_point (0.3, 0.5)
    u_focus_range 0.3
    u_blur_strength 2.0

transform right_focus():
    mesh True
    shader "depth_of_field"
    u_focus_point (0.7, 0.5)
    u_focus_range 0.3
    u_blur_strength 2.0

transform close_focus():
    mesh True
    shader "depth_of_field"
    u_focus_point (0.5, 0.7)
    u_focus_range 0.2
    u_blur_strength 2.5
