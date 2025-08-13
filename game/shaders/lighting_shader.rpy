# Dynamic Lighting Shader
# Simulates moving light sources for atmospheric lighting
#
# Overview
# - Multiple animated light sources
# - Distance-based light falloff
# - Configurable ambient lighting

init -10 python:
    # Provide updater early in init so ATL can find it at compile time
    def _dl_time_updater(tr, st, at):
        tr.u_time = st
        return 0.016

init python hide:
    # Dynamic Lighting Effect - simulates moving light sources
    renpy.register_shader(
        "dynamic_lighting",
        fragment_functions="""
        float calculateLight(vec2 pos, vec2 light_pos, float intensity, float falloff) {
            float dist = distance(pos, light_pos);
            return intensity / (1.0 + falloff * dist * dist);
        }
        """,
        variables="""
        uniform vec2 u_light1_pos;
        uniform vec2 u_light2_pos;
        uniform float u_light1_intensity;
        uniform float u_light2_intensity;
        uniform float u_light_falloff;
        uniform vec3 u_light_color;
        uniform float u_ambient_strength;
        uniform float u_time;
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
        
        // Calculate animated light positions with more dynamic motion
        vec2 spiral1 = vec2(sin(u_time * 0.9 + v_tex_coord.y * 2.0), cos(u_time * 0.7 + v_tex_coord.x * 1.5)) * 0.06;
        vec2 spiral2 = vec2(cos(u_time * 1.1 + v_tex_coord.y * 1.3), sin(u_time * 0.8 + v_tex_coord.x * 2.1)) * 0.04;
        vec2 light1 = u_light1_pos + spiral1;
        vec2 light2 = u_light2_pos + spiral2;
        
        // Calculate lighting contributions
        float light_contrib1 = calculateLight(v_tex_coord, light1, u_light1_intensity, u_light_falloff);
        float light_contrib2 = calculateLight(v_tex_coord, light2, u_light2_intensity, u_light_falloff);
        
        // Subtle flicker to simulate electrical variance
        float flicker = 1.0 + (sin(u_time * 6.0) * 0.02 + cos(u_time * 4.3) * 0.015);
        
        // Combine lighting
        float total_light = (u_ambient_strength + light_contrib1 + light_contrib2) * flicker;
        total_light = clamp(total_light, 0.1, 1.6); // Prevent complete darkness or overexposure
        
        // Apply lighting with color tint and gentle color shift
        vec3 color_shift = vec3(1.0, 0.99 + 0.01*sin(u_time*0.5), 0.99 + 0.01*cos(u_time*0.4));
        color.rgb *= (u_light_color * color_shift) * total_light;
        
        gl_FragColor = color;
        """
    )

# Transform definitions for dynamic lighting
transform dynamic_lighting_effect(light1_pos=(0.3, 0.2), light2_pos=(0.7, 0.8), 
                                 light1_intensity=0.8, light2_intensity=0.6,
                                 falloff=2.0, light_color=(1.0, 0.9, 0.7), ambient=0.3):
    mesh True
    shader "dynamic_lighting"
    u_light1_pos light1_pos
    u_light2_pos light2_pos
    u_light1_intensity light1_intensity
    u_light2_intensity light2_intensity
    u_light_falloff falloff
    u_light_color light_color
    u_ambient_strength ambient
    function _dl_time_updater

transform candlelight_effect():
    mesh True
    shader "dynamic_lighting"
    u_light1_pos (0.3, 0.4)
    u_light2_pos (0.7, 0.4)
    u_light1_intensity 0.9
    u_light2_intensity 0.7
    u_light_falloff 3.0
    u_light_color (1.0, 0.8, 0.6)
    u_ambient_strength 0.2
    function _dl_time_updater

transform streetlight_effect():
    mesh True
    shader "dynamic_lighting"
    u_light1_pos (0.2, 0.1)
    u_light2_pos (0.8, 0.1)
    u_light1_intensity 1.2
    u_light2_intensity 1.0
    u_light_falloff 2.5
    u_light_color (1.0, 0.95, 0.8)
    u_ambient_strength 0.15
    function _dl_time_updater

transform moonlight_effect():
    mesh True
    shader "dynamic_lighting"
    u_light1_pos (0.5, 0.1)
    u_light2_pos (0.5, 0.1)
    u_light1_intensity 0.6
    u_light2_intensity 0.0
    u_light_falloff 1.5
    u_light_color (0.8, 0.9, 1.2)
    u_ambient_strength 0.25
    function _dl_time_updater
