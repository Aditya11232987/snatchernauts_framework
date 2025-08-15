# Lighting Shader
# Creates dynamic lighting effects (candlelight, streetlight, moonlight)

init python:
    # Lighting shader registration
    renpy.register_shader("lighting_shader", variables="""
        uniform float u_lod_bias;
        uniform float u_time;
        uniform float u_light_intensity;
        uniform vec2 u_light_position;
        uniform vec3 u_light_color;
        uniform float u_light_radius;
        uniform float u_flicker_amount;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """, vertex_300="""
        v_tex_coord = a_tex_coord;
    """, fragment_300="""
        vec2 uv = v_tex_coord;
        vec4 color = texture2D(tex0, uv);
        
        // Calculate distance from light source
        float dist = length(uv - u_light_position);
        
        // Create falloff
        float attenuation = 1.0 / (1.0 + dist * dist / u_light_radius);
        
        // Add flickering for candlelight effect
        float flicker = 1.0 + sin(u_time * 8.0) * u_flicker_amount * 0.1;
        flicker += sin(u_time * 12.0 + 1.5) * u_flicker_amount * 0.05;
        
        // Apply lighting
        float light_strength = attenuation * u_light_intensity * flicker;
        vec3 lighting = u_light_color * light_strength;
        
        // Blend with original color
        color.rgb = mix(color.rgb, color.rgb + lighting, light_strength);
        
        gl_FragColor = color;
    """)

# Lighting effect transforms
transform lighting_effect(intensity=0.0, position=(0.5, 0.3), color=(1.0, 1.0, 1.0), radius=0.5, flicker=0.0):
    mesh True
    shader "lighting_shader"
    u_light_intensity intensity
    u_light_position position
    u_light_color color
    u_light_radius radius
    u_flicker_amount flicker
    u_time 0.0
    
    # Animate time for flickering
    linear 10.0 u_time 10.0
    repeat

# Preset transforms for different lighting types
transform lighting_off():
    lighting_effect(0.0, (0.5, 0.3), (1.0, 1.0, 1.0), 0.5, 0.0)

transform lighting_candlelight():
    lighting_effect(0.6, (0.5, 0.4), (1.0, 0.8, 0.6), 0.3, 1.0)

transform lighting_streetlight():
    lighting_effect(0.8, (0.5, 0.2), (1.0, 0.9, 0.7), 0.6, 0.2)

transform lighting_moonlight():
    lighting_effect(0.4, (0.5, 0.1), (0.8, 0.8, 1.0), 1.0, 0.0)
