# Flashlight Effect Shader
# Illumination spotlight for dark detective scenes
#
# Overview
# - Cone-based light projection
# - Distance and angle attenuation
# - Adjustable beam width and intensity

init python hide:
    # Flashlight Effect - illumination spotlight
    renpy.register_shader(
        "flashlight_effect",
        fragment_functions="""
        float calculateFlashlightCone(vec2 pos, vec2 flashlight_pos, vec2 direction, 
                                     float cone_angle, float range) {
            vec2 to_pos = pos - flashlight_pos;
            float dist = length(to_pos);
            
            // Distance attenuation
            float dist_atten = 1.0 - smoothstep(0.0, range, dist);
            
            // Cone angle attenuation
            vec2 normalized_to_pos = normalize(to_pos);
            float dot_product = dot(normalized_to_pos, direction);
            float angle_atten = smoothstep(cos(cone_angle), 1.0, dot_product);
            
            return dist_atten * angle_atten;
        }
        """,
        variables="""
        uniform vec2 u_flashlight_pos;
        uniform vec2 u_flashlight_direction;
        uniform float u_flashlight_cone_angle;
        uniform float u_flashlight_range;
        uniform float u_flashlight_intensity;
        uniform vec3 u_flashlight_color;
        uniform float u_ambient_darkness;
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
        
        // Calculate flashlight illumination
        float illumination = calculateFlashlightCone(
            v_tex_coord, u_flashlight_pos, u_flashlight_direction,
            u_flashlight_cone_angle, u_flashlight_range
        );
        
        // Apply flashlight effect
        float total_illumination = u_ambient_darkness + illumination * u_flashlight_intensity;
        total_illumination = clamp(total_illumination, 0.0, 1.0);
        
        // Tint with flashlight color in illuminated areas
        vec3 illuminated_color = mix(original.rgb, original.rgb * u_flashlight_color, 
                                   illumination * 0.3);
        
        gl_FragColor = vec4(illuminated_color * total_illumination, original.a);
        """
    )

# Transform definitions for flashlight effects
transform flashlight_effect(pos=(0.5, 0.5), direction=(0.0, -1.0), cone_angle=0.5, 
                           light_range=0.8, intensity=1.0, color=(1.0, 0.95, 0.8), 
                           darkness=0.2):
    mesh True
    shader "flashlight_effect"
    u_flashlight_pos pos
    u_flashlight_direction direction
    u_flashlight_cone_angle cone_angle
    u_flashlight_range light_range
    u_flashlight_intensity intensity
    u_flashlight_color color
    u_ambient_darkness darkness

transform narrow_flashlight():
    mesh True
    shader "flashlight_effect"
    u_flashlight_pos (0.5, 0.8)
    u_flashlight_direction (0.0, -1.0)
    u_flashlight_cone_angle 0.3
    u_flashlight_range 0.7
    u_flashlight_intensity 1.2
    u_flashlight_color (1.0, 0.9, 0.7)
    u_ambient_darkness 0.1

transform wide_flashlight():
    mesh True
    shader "flashlight_effect"
    u_flashlight_pos (0.5, 0.8)
    u_flashlight_direction (0.0, -1.0)
    u_flashlight_cone_angle 0.8
    u_flashlight_range 0.9
    u_flashlight_intensity 0.8
    u_flashlight_color (1.0, 0.95, 0.85)
    u_ambient_darkness 0.15

transform police_flashlight():
    mesh True
    shader "flashlight_effect"
    u_flashlight_pos (0.5, 0.9)
    u_flashlight_direction (0.0, -1.0)
    u_flashlight_cone_angle 0.4
    u_flashlight_range 0.8
    u_flashlight_intensity 1.5
    u_flashlight_color (1.0, 1.0, 1.0)
    u_ambient_darkness 0.05

transform detective_flashlight():
    mesh True
    shader "flashlight_effect"
    u_flashlight_pos (0.3, 0.7)
    u_flashlight_direction (0.5, -0.5)
    u_flashlight_cone_angle 0.5
    u_flashlight_range 0.6
    u_flashlight_intensity 1.0
    u_flashlight_color (1.0, 0.9, 0.8)
    u_ambient_darkness 0.2
