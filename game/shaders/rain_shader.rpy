# Rain Effect Shader
# Atmospheric weather effects for detective scenes
#
# Overview
# - Multiple rain layer simulation
# - Adjustable intensity and angle
# - Animated rain drops

init python hide:
    # Rain Effect - rebuilt for thick, resolution-independent diagonal streaks
    renpy.register_shader(
        "rain_effect",
        fragment_functions="""
        float hash(vec2 p){
            return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
        }
        
        // Thick streak generator. dir must be normalized (screen space), len in [0..1]
        float streak(vec2 uv, vec2 dir, float time, float density, float len, float thickness){
            // Project coordinates onto axes parallel/perp to direction
            vec2 perp = vec2(-dir.y, dir.x);
            float u = dot(uv, perp);     // columns across screen
            float v = dot(uv, dir);      // along streak direction
            
            // Column index and per-column random offset
            float columns = density * 220.0; // density -> how many columns
            float idx = floor(u * columns);
            float r = hash(vec2(idx, 0.0));
            
            // Each column falls at slightly different speed
            float speed = mix(0.6, 1.4, r);
            float phase = r * 10.0;
            
            // Position along streak, wrap with fract to repeat
            float y = fract(v * 1.0 - time * speed - phase);
            
            // Make a vertical segment (length len), shaped with smoothstep
            float seg = smoothstep(0.0, len, y) * (1.0 - smoothstep(len, len + 0.02, y));
            
            // Horizontal thickness via distance to column center
            float center = (idx + 0.5)/columns;
            float distx = abs(u - center);
            float thick = smoothstep(thickness, 0.0, distx);
            
            return seg * thick;
        }
        """,
        variables="""
        uniform float u_rain_intensity; // 0..1
        uniform float u_rain_time;
        uniform float u_rain_angle;     // radians
        uniform vec3 u_rain_color;
        uniform vec2 u_model_size;      // for aspect correction
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
        
        // Aspect-corrected screen UV in [-0.5,0.5]
        vec2 uv = v_tex_coord - 0.5;
        float aspect = u_model_size.x / u_model_size.y;
        uv.x *= aspect;
        
        // Direction of rain (downwards tilted by angle)
        vec2 dir = normalize(vec2(sin(u_rain_angle), -cos(u_rain_angle)));
        
        // Layered thick rain
        float d = clamp(u_rain_intensity, 0.0, 1.0);
        float r1 = streak(uv, dir, u_rain_time * 1.2, mix(0.6, 1.2, d), 0.35, 0.020);
        float r2 = streak(uv * 1.2 + 0.07, dir, u_rain_time * 1.6, mix(0.7, 1.5, d), 0.45, 0.024);
        float r3 = streak(uv * 0.9 - 0.11, dir, u_rain_time * 0.9, mix(0.5, 1.0, d), 0.50, 0.018);
        
        float rain = (r1 + r2 + r3);
        rain = clamp(rain, 0.0, 1.0);
        
        // Color and highlight (keep thick and visible when upscaled)
        vec3 rain_col = u_rain_color * (0.65 + 0.35 * smoothstep(0.0, 1.0, rain));
        color.rgb = mix(color.rgb, rain_col, rain * (0.35 + 0.25*d));
        
        gl_FragColor = color;
        """
    )

# Transform definitions for rain effects
transform rain_effect(intensity=0.3, angle=0.1, color=(0.8, 0.9, 1.0)):
    mesh True
    shader "rain_effect"
    u_rain_intensity intensity
    u_rain_angle angle
    u_rain_color color
    block:
        u_rain_time 0.0
        linear 15.0 u_rain_time 15.0
        repeat

transform light_drizzle():
    mesh True
    shader "rain_effect"
    u_rain_intensity 0.15
    u_rain_angle 0.05
    u_rain_color (0.85, 0.9, 0.95)
    block:
        u_rain_time 0.0
        linear 15.0 u_rain_time 15.0
        repeat

transform heavy_rain():
    mesh True
    shader "rain_effect"
    u_rain_intensity 0.6
    u_rain_angle 0.15
    u_rain_color (0.7, 0.8, 0.9)
    block:
        u_rain_time 0.0
        linear 10.0 u_rain_time 10.0
        repeat

transform storm_rain():
    mesh True
    shader "rain_effect"
    u_rain_intensity 0.8
    u_rain_angle 0.25
    u_rain_color (0.6, 0.7, 0.8)
    block:
        u_rain_time 0.0
        linear 8.0 u_rain_time 8.0
        repeat
