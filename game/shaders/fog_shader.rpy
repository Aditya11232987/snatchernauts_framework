# Atmospheric Fog Shader
# Creates depth and mystery through atmospheric effects
#
# Overview
# - Distance-based fog calculation
# - Animated fog movement
# - Customizable density and color

init python hide:
    # Atmospheric Fog Effect - creates depth and mystery
    renpy.register_shader(
        "atmospheric_fog",
        fragment_functions="""
        // Basic fog blend
        vec3 applyFog(vec3 color, float depth, vec3 fog_color, float fog_density) {
            float fog_factor = exp(-fog_density * depth);
            fog_factor = clamp(fog_factor, 0.0, 1.0);
            return mix(fog_color, color, fog_factor);
        }
        
        // Value noise and fbm for wispy variation
        float hash(vec2 p) {
            return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
        }
        
        float noise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            float a = hash(i);
            float b = hash(i + vec2(1.0, 0.0));
            float c = hash(i + vec2(0.0, 1.0));
            float d = hash(i + vec2(1.0, 1.0));
            vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.y * u.x;
        }
        
        float fbm(vec2 p) {
            float v = 0.0;
            float a = 0.5;
            for (int i = 0; i < 5; i++) {
                v += a * noise(p);
                p *= 2.0;
                a *= 0.5;
            }
            return v;
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
        vec2 uv = v_tex_coord;
        
        // Base depth by height
        float depth = (1.0 - uv.y) * u_fog_height;
        
        // Large-scale drift
        depth += sin(u_fog_time * 0.6 + uv.x * 6.28318) * 0.12;
        depth += cos(u_fog_time * 0.4 + uv.y * 4.71239) * 0.10;
        
        // Flow field (curl-like) to create feathery advection
        float base = fbm(uv * 2.2 + vec2(u_fog_time * 0.05, -u_fog_time * 0.04));
        float eps = 0.003;
        float dx = fbm((uv + vec2(eps, 0.0)) * 2.2) - fbm((uv - vec2(eps, 0.0)) * 2.2);
        float dy = fbm((uv + vec2(0.0, eps)) * 2.2) - fbm((uv - vec2(0.0, eps)) * 2.2);
        vec2 flow = normalize(vec2(dy, -dx) + 1e-5) * 0.02;
        vec2 adv_uv = uv + flow * (0.5 + 0.5 * sin(u_fog_time * 0.6));

        // Soft, feathery cloud structure
        float soft1 = fbm(adv_uv * 2.8 + vec2(u_fog_time * 0.06, 0.0));
        float soft2 = fbm(adv_uv * 5.0 - vec2(0.0, u_fog_time * 0.07));
        float cloudRaw = mix(soft1, soft2, 0.5);
        // Feather edges using smoothstep
        float cloud = smoothstep(0.35, 0.85, cloudRaw);

        // Use cloud field to modulate density for billowy patches
        float effective_density = u_fog_density * (0.75 + 1.1 * cloud);
        float variation = 0.8 + 0.6 * cloud;
        depth *= variation;
        
        // Compute fogged color with cloud-modulated density, then gate by source alpha
        vec3 fogged = applyFog(color.rgb, depth, u_fog_color, effective_density);
        color.rgb = mix(color.rgb, fogged, color.a);
        
        // Subtle forward-scatter glow for dense clouds (feathered)
        color.rgb += u_fog_color * pow(cloud, 2.0) * 0.035;
        
        gl_FragColor = color;
        """
    )

# Transform definitions for atmospheric fog
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

transform light_fog():
    mesh True
    shader "atmospheric_fog"
    u_fog_color (0.75, 0.78, 0.85)
    u_fog_density 0.28
    u_fog_height 1.6
    block:
        u_fog_time 0.0
        linear 14.0 u_fog_time 12.56637061436
        repeat

transform heavy_fog():
    mesh True
    shader "atmospheric_fog"
    u_fog_color (0.28, 0.3, 0.38)
    u_fog_density 0.85
    u_fog_height 2.6
    block:
        u_fog_time 0.0
        linear 12.0 u_fog_time 12.56637061436
        repeat

transform mysterious_fog():
    mesh True
    shader "atmospheric_fog"
    u_fog_color (0.22, 0.22, 0.32)
    u_fog_density 0.6
    u_fog_height 2.2
    block:
        u_fog_time 0.0
        linear 16.0 u_fog_time 12.56637061436
        repeat
