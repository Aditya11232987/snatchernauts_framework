# Detective Atmospheric Shaders
# Visual effects designed for detective/mystery game atmosphere
#
# Overview
# - Film grain, vintage effects, atmospheric fog, dynamic lighting
# - Integrates with existing CRT and bloom systems
# - Uses Ren'Py's shader parts system for proper performance

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
        float grain_factor = grain(v_tex_coord * 800.0, u_grain_time, u_grain_strength);
        
        // Apply grain with contrast adjustment
        color.rgb *= grain_factor;
        color.rgb = mix(color.rgb, vec3(0.5), -u_grain_contrast);
        
        gl_FragColor = color;
        """
    )

    # Atmospheric Fog Effect - creates depth and mystery
    renpy.register_shader(
        "atmospheric_fog",
        fragment_functions="""
        vec3 applyFog(vec3 color, float depth, vec3 fog_color, float fog_density) {
            float fog_factor = exp(-fog_density * depth);
            fog_factor = clamp(fog_factor, 0.0, 1.0);
            return mix(fog_color, color, fog_factor);
        }
        """,
        variables="""
        uniform vec3 u_fog_color;
        uniform float u_fog_density;
        uniform float u_fog_height;
        uniform float u_fog_time;
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
        
        // Calculate depth based on Y position and time-based variation
        float depth = (1.0 - v_tex_coord.y) * u_fog_height;
        depth += sin(u_fog_time + v_tex_coord.x * 3.14159) * 0.1;
        
        // Apply atmospheric fog
        color.rgb = applyFog(color.rgb, depth, u_fog_color, u_fog_density);
        
        gl_FragColor = color;
        """
    )

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
        
        // Calculate animated light positions
        vec2 light1 = u_light1_pos + vec2(sin(u_time * 0.5), cos(u_time * 0.3)) * 0.05;
        vec2 light2 = u_light2_pos + vec2(cos(u_time * 0.7), sin(u_time * 0.4)) * 0.03;
        
        // Calculate lighting contributions
        float light_contrib1 = calculateLight(v_tex_coord, light1, u_light1_intensity, u_light_falloff);
        float light_contrib2 = calculateLight(v_tex_coord, light2, u_light2_intensity, u_light_falloff);
        
        // Combine lighting
        float total_light = u_ambient_strength + light_contrib1 + light_contrib2;
        total_light = clamp(total_light, 0.1, 1.5); // Prevent complete darkness or overexposure
        
        // Apply lighting with color tint
        color.rgb *= u_light_color * total_light;
        
        gl_FragColor = color;
        """
    )

    # Rain Effect - for atmospheric weather
    renpy.register_shader(
        "rain_effect",
        fragment_functions="""
        float rainDrop(vec2 uv, float time) {
            float y = fract((uv.y + time * 0.3) * 10.0);
            float x = fract(uv.x * 50.0);
            return smoothstep(0.0, 0.02, y) * smoothstep(0.02, 0.0, y - 0.01) * 
                   smoothstep(0.48, 0.52, x);
        }
        """,
        variables="""
        uniform float u_rain_intensity;
        uniform float u_rain_time;
        uniform float u_rain_angle;
        uniform vec3 u_rain_color;
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
        
        // Apply rain angle transformation
        vec2 rain_uv = v_tex_coord;
        rain_uv.x += rain_uv.y * u_rain_angle;
        
        // Generate multiple rain layers
        float rain = 0.0;
        rain += rainDrop(rain_uv + vec2(0.1, 0.3), u_rain_time);
        rain += rainDrop(rain_uv + vec2(0.7, 0.1), u_rain_time * 1.3);
        rain += rainDrop(rain_uv + vec2(0.3, 0.8), u_rain_time * 0.7);
        
        // Blend rain with scene
        rain *= u_rain_intensity;
        color.rgb = mix(color.rgb, u_rain_color, rain * 0.3);
        color.rgb += u_rain_color * rain * 0.2; // Add rain highlights
        
        gl_FragColor = color;
        """
    )

# Transform definitions for easy use
transform film_grain_effect(strength=0.1, contrast=0.2):
    mesh True
    shader "film_grain"
    u_grain_strength strength
    u_grain_contrast contrast
    block:
        u_grain_time 0.0
        linear 60.0 u_grain_time 60.0
        repeat

transform atmospheric_fog_effect(color=(0.5, 0.5, 0.6), density=0.3, height=2.0):
    mesh True
    shader "atmospheric_fog"
    u_fog_color color
    u_fog_density density  
    u_fog_height height
    block:
        u_fog_time 0.0
        linear 30.0 u_fog_time 6.28318530718  # 2*PI for smooth loop
        repeat

transform vintage_sepia_effect(strength=0.7, contrast=1.2, vignette=1.5):
    mesh True
    shader "vintage_sepia"
    u_sepia_strength strength
    u_sepia_contrast contrast
    u_vignette_intensity vignette

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
    block:
        u_time 0.0
        linear 20.0 u_time 20.0
        repeat

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

# Combined effect transforms for common detective atmosphere combinations
transform detective_noir_atmosphere(grain_strength=0.15, sepia_strength=0.4, vignette=1.8):
    contains:
        At(Null(), film_grain_effect(grain_strength, 0.3))
    contains:
        At(Null(), vintage_sepia_effect(sepia_strength, 1.1, vignette))

transform foggy_night_scene(fog_density=0.4, light1_pos=(0.2, 0.1), light2_pos=(0.8, 0.3)):
    contains:
        At(Null(), atmospheric_fog_effect((0.1, 0.1, 0.2), fog_density, 1.8))
    contains:  
        At(Null(), dynamic_lighting_effect(light1_pos, light2_pos, 0.9, 0.5, 3.0, (1.0, 0.8, 0.6), 0.2))

transform rainy_detective_scene(rain_intensity=0.4, fog_density=0.2):
    contains:
        At(Null(), rain_effect(rain_intensity, 0.05, (0.7, 0.8, 0.9)))
    contains:
        At(Null(), atmospheric_fog_effect((0.4, 0.4, 0.5), fog_density, 1.2))
    contains:
        At(Null(), film_grain_effect(0.08, 0.15))
