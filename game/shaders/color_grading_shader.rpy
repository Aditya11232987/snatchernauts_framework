# Color Grading Shader
# Professional color correction for cinematic appearance
#
# Overview
# - Brightness, contrast, saturation adjustments
# - Gamma correction and temperature control
# - Color tinting for mood setting

init python hide:
    # Color Grading - professional color correction
    renpy.register_shader(
        "color_grading",
        fragment_functions="""
        vec3 adjustContrast(vec3 color, float contrast) {
            return (color - 0.5) * contrast + 0.5;
        }
        
        vec3 adjustSaturation(vec3 color, float saturation) {
            float gray = dot(color, vec3(0.299, 0.587, 0.114));
            return mix(vec3(gray), color, saturation);
        }
        
        vec3 adjustGamma(vec3 color, float gamma) {
            return pow(color, vec3(1.0 / gamma));
        }
        
        vec3 adjustTemperature(vec3 color, float temperature) {
            // Simple temperature adjustment (blue/orange shift)
            if (temperature > 0.0) {
                color.r = mix(color.r, min(1.0, color.r + temperature * 0.3), temperature);
                color.b = mix(color.b, max(0.0, color.b - temperature * 0.2), temperature);
            } else {
                color.b = mix(color.b, min(1.0, color.b - temperature * 0.3), -temperature);
                color.r = mix(color.r, max(0.0, color.r + temperature * 0.2), -temperature);
            }
            return color;
        }
        """,
        variables="""
        uniform float u_brightness;
        uniform float u_contrast;
        uniform float u_saturation;
        uniform float u_gamma;
        uniform float u_temperature;
        uniform vec3 u_color_tint;
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
        
        // Apply color grading pipeline
        color.rgb += u_brightness;
        color.rgb = adjustContrast(color.rgb, u_contrast);
        color.rgb = adjustSaturation(color.rgb, u_saturation);
        color.rgb = adjustGamma(color.rgb, u_gamma);
        color.rgb = adjustTemperature(color.rgb, u_temperature);
        color.rgb *= u_color_tint;
        
        // Clamp to valid range
        color.rgb = clamp(color.rgb, 0.0, 1.0);
        
        gl_FragColor = color;
        """
    )

# Transform definitions for color grading
transform color_grading_effect(brightness=0.0, contrast=1.0, saturation=1.0, 
                              gamma=1.0, temperature=0.0, tint=(1.0, 1.0, 1.0)):
    mesh True
    shader "color_grading"
    u_brightness brightness
    u_contrast contrast
    u_saturation saturation
    u_gamma gamma
    u_temperature temperature
    u_color_tint tint

transform cool_grading():
    mesh True
    shader "color_grading"
    u_brightness -0.05
    u_contrast 1.2
    u_saturation 0.9
    u_gamma 1.0
    u_temperature -0.3
    u_color_tint (0.9, 0.95, 1.1)

transform warm_grading():
    mesh True
    shader "color_grading"
    u_brightness 0.05
    u_contrast 1.1
    u_saturation 1.1
    u_gamma 0.95
    u_temperature 0.3
    u_color_tint (1.1, 1.05, 0.9)

transform noir_grading():
    mesh True
    shader "color_grading"
    u_brightness -0.1
    u_contrast 1.5
    u_saturation 0.7
    u_gamma 1.2
    u_temperature -0.1
    u_color_tint (0.95, 0.95, 1.0)

transform vintage_grading():
    mesh True
    shader "color_grading"
    u_brightness -0.02
    u_contrast 1.3
    u_saturation 0.8
    u_gamma 1.1
    u_temperature 0.2
    u_color_tint (1.05, 1.0, 0.9)
