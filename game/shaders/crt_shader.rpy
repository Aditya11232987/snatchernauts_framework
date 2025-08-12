# CRT Shader Integration

init python hide:
    renpy.register_shader(
        "chroma_crt",
        fragment_functions="""
        vec2 uuv(float wp, vec2 tex_coord)
    {
    vec2 uvv = tex_coord;
    vec2 dc = 0.5-uvv;
    dc *= dc;
    uvv -= .5; uvv *= 1.+(dc.yx*wp); uvv += .5;
    return uvv;
    }
""", variables="""
    uniform float u_warp;
    uniform float u_scan;
    uniform float u_chroma;
    uniform float u_scanline_size;
    uniform float u_scanline_offset;
    uniform float u_vignette_strength;
    uniform float u_vignette_width;
    uniform vec2 u_model_size;
    uniform sampler2D tex0;
    attribute vec2 a_tex_coord;
    attribute vec4 a_position;
    varying vec2 v_tex_coord;
""", vertex_300="""
    v_tex_coord = a_position.xy/u_model_size;
""", fragment_300="""
    vec2 uv = uuv(u_warp, v_tex_coord);
    #define PI 3.14159265359
    if (uv.x < 0.0 || uv.x > 1.0 || uv.y < 0.0 || uv.y > 1.0) {
        gl_FragColor = vec4(0.0);
    } else {
        vec2 texra = texture2D(tex0, uv).ra;
        vec2 texga = texture2D(tex0, uuv(u_warp*u_chroma, v_tex_coord)).ga;
        vec2 texba = texture2D(tex0, uuv(u_warp*u_chroma*u_chroma, v_tex_coord)).ba;
        vec4 pure = vec4(texra.x, texga.x, texba.x, (texra.y+texga.y+texba.y)/3.);
        float scanline_density = 200.0;
        float normalized_y = (uv.y * scanline_density) + u_scanline_offset;
        float scanline_pattern = sin(normalized_y * PI * u_scanline_size);
        float apply = pow(abs(scanline_pattern) * u_scan, 2.);
        vec4 color = mix(pure, vec4(0.0), apply);

        // Horizontal vignette: darken left/right edges
        float edge = min(uv.x, 1.0 - uv.x);
        float width = max(u_vignette_width, 0.0001);
        float t = clamp(edge / width, 0.0, 1.0);
        float vignette = mix(1.0 - u_vignette_strength, 1.0, smoothstep(0.0, 1.0, t));
        color.rgb *= vignette;
        gl_FragColor = color;
    }
"""
)

transform chroma_crt(warp=.2, scan=.5, chroma=.9, scanline_size=1.0, vignette_strength=.35, vignette_width=.25):
    mesh True
    shader "chroma_crt"
    u_warp warp
    u_scan scan
    u_chroma chroma
    u_scanline_size scanline_size
    u_scanline_offset 0.0
    u_vignette_strength vignette_strength
    u_vignette_width vignette_width

transform animated_chroma_crt(base_warp=.2, base_scan=.5, base_chroma=.9, base_scanline_size=1.0, animation_intensity=0.1, animation_speed=2.0, vignette_strength=.35, vignette_width=.25):
    mesh True
    shader "chroma_crt"
    u_warp base_warp
    u_scan base_scan
    u_chroma base_chroma
    u_scanline_size base_scanline_size
    u_vignette_strength vignette_strength
    u_vignette_width vignette_width
    block:
        u_scanline_offset 0.0
        linear animation_speed u_scanline_offset (200.0 * animation_intensity)
        repeat

transform static_chroma_crt(warp=.2, scan=.5, chroma=.9, scanline_size=1.0, vignette_strength=.35, vignette_width=.25):
    mesh True
    shader "chroma_crt"
    u_warp warp
    u_scan scan
    u_chroma chroma
    u_scanline_size scanline_size
    u_scanline_offset 0.0
    u_vignette_strength vignette_strength
    u_vignette_width vignette_width

transform black_chroma_crt(child, warp=.2, scan=.5, chroma=.9, scanline_size=1.0, vignette_strength=.35, vignette_width=.25):
    contains:
        "black"
    contains:
        At(child, chroma_crt(warp, scan, chroma, scanline_size, vignette_strength, vignette_width))
