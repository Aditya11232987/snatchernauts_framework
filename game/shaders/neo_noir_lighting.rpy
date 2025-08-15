# Neo-Noir Dynamic Lighting Shader
# Advanced lighting system for 80s neo-noir atmosphere
# Features 10 distinct lighting presets for different scenes and moods

init python:
    # Dynamic lighting shader with multiple light sources
    renpy.register_shader("neo_noir_lighting", variables="""
        uniform sampler2D tex0;
        uniform float u_lod_bias;
        
        // Primary light source
        uniform vec2 u_light_pos;
        uniform vec3 u_light_color;
        uniform float u_light_intensity;
        uniform float u_light_radius;
        
        // Secondary light source (for rim lighting)
        uniform vec2 u_light2_pos;
        uniform vec3 u_light2_color;
        uniform float u_light2_intensity;
        uniform float u_light2_radius;
        
        // Ambient lighting
        uniform vec3 u_ambient_color;
        uniform float u_ambient_intensity;
        
        // Shadow parameters
        uniform float u_shadow_softness;
        uniform float u_shadow_intensity;
        
        // Specular highlights
        uniform float u_specular_intensity;
        uniform float u_specular_size;
        
        // Fog/atmosphere
        uniform float u_fog_density;
        uniform vec3 u_fog_color;
        
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
    """, vertex_300="""
        v_tex_coord = a_tex_coord;
    """, fragment_300="""
        vec2 coord = v_tex_coord;
        vec4 color = texture2D(tex0, coord, u_lod_bias);
        
        // Calculate distances from light sources
        float dist1 = distance(coord, u_light_pos);
        float dist2 = distance(coord, u_light2_pos);
        
        // Primary light attenuation
        float atten1 = 1.0 - smoothstep(0.0, u_light_radius, dist1);
        atten1 = pow(atten1, 2.0 - u_shadow_softness);
        
        // Secondary light attenuation
        float atten2 = 1.0 - smoothstep(0.0, u_light2_radius, dist2);
        atten2 = pow(atten2, 2.0 - u_shadow_softness);
        
        // Calculate luminance for specular
        float lum = dot(color.rgb, vec3(0.299, 0.587, 0.114));
        
        // Specular highlights (fake, but effective for 2D)
        float spec1 = pow(atten1 * lum, u_specular_size) * u_specular_intensity;
        float spec2 = pow(atten2 * lum, u_specular_size) * u_specular_intensity;
        
        // Combine lighting
        vec3 lit = color.rgb * u_ambient_color * u_ambient_intensity;
        lit += color.rgb * u_light_color * atten1 * u_light_intensity;
        lit += color.rgb * u_light2_color * atten2 * u_light2_intensity;
        lit += u_light_color * spec1;
        lit += u_light2_color * spec2;
        
        // Apply shadows (darken unlit areas)
        float shadow = 1.0 - (1.0 - max(atten1, atten2)) * u_shadow_intensity;
        lit *= shadow;
        
        // Apply fog effect for atmosphere
        float fogFactor = exp(-u_fog_density * max(dist1, dist2));
        lit = mix(u_fog_color, lit, fogFactor);
        
        // Ensure we stay in valid range
        color.rgb = clamp(lit, 0.0, 1.0);
        
        gl_FragColor = color;
    """)

# Base transform for dynamic lighting
transform neo_noir_lighting(
    light_pos=(0.5, 0.3), light_color=(1.0, 1.0, 1.0), light_intensity=1.0, light_radius=0.8,
    light2_pos=(0.8, 0.7), light2_color=(1.0, 1.0, 1.0), light2_intensity=0.5, light2_radius=0.6,
    ambient_color=(1.0, 1.0, 1.0), ambient_intensity=0.3,
    shadow_softness=0.5, shadow_intensity=0.7,
    specular_intensity=0.0, specular_size=2.0,
    fog_density=0.0, fog_color=(0.5, 0.5, 0.6)):
    mesh True
    shader "neo_noir_lighting"
    u_light_pos light_pos
    u_light_color light_color
    u_light_intensity light_intensity
    u_light_radius light_radius
    u_light2_pos light2_pos
    u_light2_color light2_color
    u_light2_intensity light2_intensity
    u_light2_radius light2_radius
    u_ambient_color ambient_color
    u_ambient_intensity ambient_intensity
    u_shadow_softness shadow_softness
    u_shadow_intensity shadow_intensity
    u_specular_intensity specular_intensity
    u_specular_size specular_size
    u_fog_density fog_density
    u_fog_color fog_color

# 10 Neo-Noir Lighting Presets

# 1. Street Lamp - Single overhead yellow light with dark shadows
transform lighting_street_lamp():
    neo_noir_lighting(
        light_pos=(0.5, 0.2),
        light_color=(1.0, 0.9, 0.7),
        light_intensity=1.2,
        light_radius=0.6,
        light2_pos=(0.5, 0.8),
        light2_color=(0.4, 0.4, 0.5),
        light2_intensity=0.2,
        light2_radius=0.3,
        ambient_color=(0.3, 0.3, 0.4),
        ambient_intensity=0.2,
        shadow_softness=0.3,
        shadow_intensity=0.8,
        specular_intensity=0.1,
        specular_size=3.0,
        fog_density=0.3,
        fog_color=(0.2, 0.2, 0.3)
    )

# 2. Neon Signs - Multiple colored lights from sides
transform lighting_neon_signs():
    neo_noir_lighting(
        light_pos=(0.1, 0.3),
        light_color=(1.0, 0.3, 0.6),
        light_intensity=0.9,
        light_radius=0.5,
        light2_pos=(0.9, 0.4),
        light2_color=(0.3, 0.8, 1.0),
        light2_intensity=0.8,
        light2_radius=0.5,
        ambient_color=(0.4, 0.3, 0.5),
        ambient_intensity=0.3,
        shadow_softness=0.6,
        shadow_intensity=0.6,
        specular_intensity=0.2,
        specular_size=2.0,
        fog_density=0.2,
        fog_color=(0.3, 0.2, 0.4)
    )

# 3. Window Blinds - Slanted light through venetian blinds
transform lighting_window_blinds():
    neo_noir_lighting(
        light_pos=(0.7, 0.3),
        light_color=(0.9, 0.95, 1.0),
        light_intensity=1.1,
        light_radius=0.7,
        light2_pos=(0.3, 0.6),
        light2_color=(0.6, 0.65, 0.8),
        light2_intensity=0.3,
        light2_radius=0.4,
        ambient_color=(0.4, 0.45, 0.5),
        ambient_intensity=0.25,
        shadow_softness=0.2,
        shadow_intensity=0.85,
        specular_intensity=0.15,
        specular_size=2.5,
        fog_density=0.4,
        fog_color=(0.3, 0.35, 0.4)
    )

# 4. Police Lights - Alternating red and blue emergency lights
transform lighting_police_lights():
    neo_noir_lighting(
        light_pos=(0.3, 0.5),
        light_color=(1.0, 0.0, 0.2),
        light_intensity=1.0,
        light_radius=0.6,
        light2_pos=(0.7, 0.5),
        light2_color=(0.0, 0.3, 1.0),
        light2_intensity=1.0,
        light2_radius=0.6,
        ambient_color=(0.2, 0.2, 0.3),
        ambient_intensity=0.15,
        shadow_softness=0.4,
        shadow_intensity=0.7,
        specular_intensity=0.25,
        specular_size=2.0,
        fog_density=0.1,
        fog_color=(0.2, 0.2, 0.3)
    )

# 5. Desk Lamp - Focused warm light from one corner
transform lighting_desk_lamp():
    neo_noir_lighting(
        light_pos=(0.75, 0.6),
        light_color=(1.0, 0.95, 0.8),
        light_intensity=1.3,
        light_radius=0.45,
        light2_pos=(0.2, 0.2),
        light2_color=(0.3, 0.35, 0.4),
        light2_intensity=0.2,
        light2_radius=0.3,
        ambient_color=(0.35, 0.33, 0.3),
        ambient_intensity=0.2,
        shadow_softness=0.25,
        shadow_intensity=0.75,
        specular_intensity=0.12,
        specular_size=3.5,
        fog_density=0.5,
        fog_color=(0.4, 0.38, 0.35)
    )

# 6. Car Headlights - Strong directional beams
transform lighting_car_headlights():
    neo_noir_lighting(
        light_pos=(0.2, 0.5),
        light_color=(1.0, 1.0, 0.95),
        light_intensity=1.5,
        light_radius=0.8,
        light2_pos=(0.8, 0.5),
        light2_color=(1.0, 1.0, 0.95),
        light2_intensity=1.5,
        light2_radius=0.8,
        ambient_color=(0.2, 0.2, 0.25),
        ambient_intensity=0.1,
        shadow_softness=0.15,
        shadow_intensity=0.9,
        specular_intensity=0.3,
        specular_size=1.5,
        fog_density=0.6,
        fog_color=(0.25, 0.25, 0.3)
    )

# 7. Interrogation Room - Harsh overhead fluorescent
transform lighting_interrogation():
    neo_noir_lighting(
        light_pos=(0.5, 0.5),
        light_color=(0.95, 1.0, 0.95),
        light_intensity=1.4,
        light_radius=0.9,
        light2_pos=(0.5, 0.5),
        light2_color=(0.95, 1.0, 0.95),
        light2_intensity=0.0,
        light2_radius=0.1,
        ambient_color=(0.8, 0.85, 0.8),
        ambient_intensity=0.4,
        shadow_softness=0.1,
        shadow_intensity=0.95,
        specular_intensity=0.2,
        specular_size=1.0,
        fog_density=0.0,
        fog_color=(1.0, 1.0, 1.0)
    )

# 8. Sunset Through Window - Golden hour side lighting
transform lighting_sunset_window():
    neo_noir_lighting(
        light_pos=(0.85, 0.4),
        light_color=(1.0, 0.7, 0.4),
        light_intensity=1.2,
        light_radius=0.9,
        light2_pos=(0.15, 0.3),
        light2_color=(0.8, 0.5, 0.3),
        light2_intensity=0.4,
        light2_radius=0.5,
        ambient_color=(0.6, 0.45, 0.35),
        ambient_intensity=0.35,
        shadow_softness=0.5,
        shadow_intensity=0.65,
        specular_intensity=0.18,
        specular_size=2.5,
        fog_density=0.3,
        fog_color=(0.7, 0.5, 0.4)
    )

# 9. Dark Alley - Minimal lighting with deep shadows
transform lighting_dark_alley():
    neo_noir_lighting(
        light_pos=(0.3, 0.1),
        light_color=(0.6, 0.6, 0.7),
        light_intensity=0.6,
        light_radius=0.4,
        light2_pos=(0.8, 0.9),
        light2_color=(0.4, 0.4, 0.5),
        light2_intensity=0.3,
        light2_radius=0.3,
        ambient_color=(0.15, 0.15, 0.2),
        ambient_intensity=0.15,
        shadow_softness=0.35,
        shadow_intensity=0.95,
        specular_intensity=0.05,
        specular_size=4.0,
        fog_density=0.8,
        fog_color=(0.1, 0.1, 0.15)
    )

# 10. Television Glow - Flickering blue-white light
transform lighting_tv_glow():
    neo_noir_lighting(
        light_pos=(0.5, 0.6),
        light_color=(0.8, 0.9, 1.0),
        light_intensity=0.9,
        light_radius=0.7,
        light2_pos=(0.5, 0.6),
        light2_color=(0.7, 0.8, 1.0),
        light2_intensity=0.3,
        light2_radius=0.5,
        ambient_color=(0.3, 0.35, 0.45),
        ambient_intensity=0.25,
        shadow_softness=0.7,
        shadow_intensity=0.5,
        specular_intensity=0.1,
        specular_size=2.0,
        fog_density=0.2,
        fog_color=(0.35, 0.4, 0.5)
    )

# Default neutral lighting
transform lighting_neutral():
    neo_noir_lighting(
        light_pos=(0.5, 0.5),
        light_color=(1.0, 1.0, 1.0),
        light_intensity=1.0,
        light_radius=1.0,
        light2_pos=(0.5, 0.5),
        light2_color=(1.0, 1.0, 1.0),
        light2_intensity=0.0,
        light2_radius=0.1,
        ambient_color=(1.0, 1.0, 1.0),
        ambient_intensity=1.0,
        shadow_softness=1.0,
        shadow_intensity=0.0,
        specular_intensity=0.0,
        specular_size=1.0,
        fog_density=0.0,
        fog_color=(1.0, 1.0, 1.0)
    )

# Store current lighting preset
default current_lighting = "neutral"
default lighting_presets = [
    ("neutral", "Neutral", lighting_neutral),
    ("street_lamp", "Street Lamp", lighting_street_lamp),
    ("neon_signs", "Neon Signs", lighting_neon_signs),
    ("window_blinds", "Window Blinds", lighting_window_blinds),
    ("police_lights", "Police Lights", lighting_police_lights),
    ("desk_lamp", "Desk Lamp", lighting_desk_lamp),
    ("car_headlights", "Car Headlights", lighting_car_headlights),
    ("interrogation", "Interrogation Room", lighting_interrogation),
    ("sunset_window", "Sunset Window", lighting_sunset_window),
    ("dark_alley", "Dark Alley", lighting_dark_alley),
    ("tv_glow", "Television Glow", lighting_tv_glow)
]

init python:
    def cycle_lighting(direction=1):
        """Cycle through lighting presets"""
        global current_lighting
        current_index = 0
        for i, (preset_id, _, _) in enumerate(store.lighting_presets):
            if preset_id == store.current_lighting:
                current_index = i
                break
        
        new_index = (current_index + direction) % len(store.lighting_presets)
        store.current_lighting = store.lighting_presets[new_index][0]
        preset_name = store.lighting_presets[new_index][1]
        renpy.notify(f"Lighting: {preset_name}")
        renpy.restart_interaction()
    
    def set_lighting(preset_id):
        """Set a specific lighting preset"""
        global current_lighting
        store.current_lighting = preset_id
        for pid, pname, _ in store.lighting_presets:
            if pid == preset_id:
                renpy.notify(f"Lighting: {pname}")
                break
        renpy.restart_interaction()
    
    # Animated lighting effects
    def animate_police_lights():
        """Create animated police light effect"""
        # This would be called to create the alternating red/blue effect
        pass
