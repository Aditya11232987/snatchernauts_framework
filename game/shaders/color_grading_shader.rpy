# Color Grading Shader
# Provides color temperature and mood adjustments

init python:
    # Color grading shader registration
    renpy.register_shader("color_grading_shader", variables="""
        uniform float u_lod_bias;
        uniform float u_temperature;
        uniform float u_tint;
        uniform float u_saturation;
        uniform float u_contrast;
        uniform float u_brightness;
        uniform vec3 u_color_filter;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """, vertex_300="""
        v_tex_coord = a_tex_coord;
    """, fragment_300="""
        vec2 uv = v_tex_coord;
        vec4 color = texture2D(tex0, uv);
        
        // Temperature adjustment (warm/cool)
        color.r *= 1.0 + u_temperature * 0.3;
        color.b *= 1.0 - u_temperature * 0.3;
        
        // Tint adjustment (magenta/green)
        color.r *= 1.0 + u_tint * 0.2;
        color.g *= 1.0 - abs(u_tint) * 0.1;
        color.b *= 1.0 - u_tint * 0.2;
        
        // Brightness and contrast
        color.rgb = (color.rgb - 0.5) * u_contrast + 0.5 + u_brightness;
        
        // Saturation adjustment
        float luminance = dot(color.rgb, vec3(0.299, 0.587, 0.114));
        color.rgb = mix(vec3(luminance), color.rgb, u_saturation);
        
        // Color filter
        color.rgb *= u_color_filter;
        
        gl_FragColor = color;
    """)

# Color grading effect transforms
transform color_grading_effect(temperature=0.0, tint=0.0, saturation=1.0, contrast=1.0, brightness=0.0, color_filter=(1.0, 1.0, 1.0)):
    mesh True
    shader "color_grading_shader"
    u_temperature temperature
    u_tint tint
    u_saturation saturation
    u_contrast contrast
    u_brightness brightness
    u_color_filter color_filter

# Preset transforms for different color grades
transform color_grading_off():
    color_grading_effect(0.0, 0.0, 1.0, 1.0, 0.0, (1.0, 1.0, 1.0))

transform color_grading_cool():
    color_grading_effect(-0.3, 0.0, 1.1, 1.1, -0.05, (0.95, 1.0, 1.1))

transform color_grading_warm():
    color_grading_effect(0.3, 0.0, 1.1, 1.1, 0.05, (1.1, 1.0, 0.9))

transform color_grading_noir():
    color_grading_effect(-0.1, 0.1, 0.7, 1.3, -0.1, (0.9, 0.9, 1.0))

transform color_grading_vintage():
    color_grading_effect(0.2, -0.1, 0.8, 1.2, -0.05, (1.0, 0.95, 0.85))
