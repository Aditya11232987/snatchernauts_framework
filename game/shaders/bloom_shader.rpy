# Custom Bloom Shader using Ren'Py Shader Parts System
# Based on the proper Ren'Py model-based rendering approach
#
# Overview
# - Registers shader parts and a model-based displayable to apply bloom.
# - This file is optional; bloom can also be achieved via filters.

init python:
    # Helper function to convert hex color to RGB tuple
    def hex_to_rgb(hex_color):
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0  
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b)
    
    # Custom bloom shader parts using proper Ren'Py system
    # Based on the shader parts documentation
    
    # Register texture coordinate vertex part (priority 200)
    renpy.register_shader("bloom.coords", variables="""
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;
        uniform sampler2D tex0;
    """, vertex_200="""
        v_tex_coord = a_tex_coord;
    """)
    
    # Register base texture fragment part (priority 200)
    renpy.register_shader("bloom.texture", variables="""
        uniform sampler2D tex0;
        varying vec2 v_tex_coord;
    """, fragment_200="""
        gl_FragColor = texture2D(tex0, v_tex_coord);
    """)
    
    # Register bloom effect fragment part (priority 400)
    renpy.register_shader("bloom.effect", variables="""
        uniform vec3 u_bloom_color;
        uniform float u_bloom_intensity;
        uniform float u_bloom_radius;
        uniform float u_bloom_threshold;
        uniform float u_bloom_softness;
        uniform float u_alpha_min;
        uniform float u_alpha_max;
        uniform float u_pulse_speed;
        uniform float u_time;
        uniform vec2 u_tex_size;
        uniform sampler2D tex0;
        varying vec2 v_tex_coord;
    """, fragment_400="""
        // Enhanced bloom blur function
        vec4 bloomBlur(vec2 uv, float radius) {
            vec4 result = vec4(0.0);
            vec2 texel_size = 1.0 / u_tex_size;
            float total_weight = 0.0;
            
            // 5x5 Gaussian blur kernel
            for (int x = -2; x <= 2; x++) {
                for (int y = -2; y <= 2; y++) {
                    vec2 offset = vec2(float(x), float(y)) * texel_size * radius;
                    float weight = exp(-0.5 * float(x*x + y*y) / 2.0);
                    result += texture2D(tex0, uv + offset) * weight;
                    total_weight += weight;
                }
            }
            return result / total_weight;
        }
        
        // Apply bloom effect to current fragment color
        vec4 original = gl_FragColor;
        float brightness = max(original.r, max(original.g, original.b)) * original.a;
        float bloom_mask = smoothstep(u_bloom_threshold - u_bloom_softness, u_bloom_threshold + u_bloom_softness, brightness);
        
        if (bloom_mask > 0.0) {
            vec4 bloom = bloomBlur(v_tex_coord, u_bloom_radius) * bloom_mask;
            bloom.rgb *= u_bloom_color;
            
            float pulse = sin(u_time * u_pulse_speed) * 0.5 + 0.5;
            float bloom_alpha = mix(u_alpha_min, u_alpha_max, pulse);
            
            gl_FragColor.rgb += bloom.rgb * u_bloom_intensity * bloom_alpha;
            gl_FragColor.a = max(original.a, bloom.a * bloom_alpha * u_bloom_softness);
        }
    """)

# Note: Transform-based shader approach has syntax issues in Ren'Py
# We'll use the Python Displayable approach instead

# Model-based shader implementation using proper Ren'Py approach
init python:
    import renpy.display.model as model
    
    class BloomShaderModel(model.Model):
        def __init__(self, bloom_color="#ffffff", bloom_intensity=0.5, bloom_radius=8.0, 
                    bloom_threshold=0.1, bloom_softness=0.7, alpha_min=0.2, 
                    alpha_max=0.8, pulse_speed=1.0):
            super(BloomShaderModel, self).__init__()
            
            # Convert hex color to RGB
            bloom_rgb = hex_to_rgb(bloom_color)
            
            # Set shader uniforms using the model system
            self.uniforms = {
                "u_bloom_color": bloom_rgb,
                "u_bloom_intensity": bloom_intensity,
                "u_bloom_radius": bloom_radius,
                "u_bloom_threshold": bloom_threshold,
                "u_bloom_softness": bloom_softness,
                "u_alpha_min": alpha_min,
                "u_alpha_max": alpha_max,
                "u_pulse_speed": pulse_speed,
                "u_tex_size": (1280.0, 720.0)
            }
            
        def update_time(self, st):
            self.uniforms["u_time"] = st
            
    class BloomShaderDisplayable(renpy.Displayable):
        def __init__(self, child, **kwargs):
            super(BloomShaderDisplayable, self).__init__()
            self.child = renpy.displayable(child)
            self.model = BloomShaderModel(**kwargs)
            
        def render(self, width, height, st, at):
            # Update time uniform
            self.model.update_time(st)
            
            # Get child render
            child_render = renpy.render(self.child, width, height, st, at)
            
            # Create render with shader applied
            render = renpy.Render(width, height)
            
            # Apply shader with model uniforms
            shader_render = renpy.display.render.render_for_model(
                self.child, self.model, "bloom_shader", width, height, st, at
            )
            
            if shader_render:
                render.blit(shader_render, (0, 0))
            else:
                # Fallback to child render if shader fails
                render.blit(child_render, (0, 0))
            
            return render
            
        def get_placement(self):
            return self.child.get_placement()
    
    def create_bloom_shader(child, **kwargs):
        return BloomShaderDisplayable(child, **kwargs)
