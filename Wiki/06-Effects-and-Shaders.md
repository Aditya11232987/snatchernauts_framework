# Visual Effects & Shaders System

**Part II: Core Development - Chapter 6**

*A comprehensive guide to the framework's advanced visual effects system, utilizing GPU-accelerated GLSL shaders to create immersive, cinematic experiences with powerful atmospheric and interactive components.*

---

## Chapter Overview

This chapter provides complete coverage of the framework's sophisticated visual effects system, which serves as a powerful toolset for creating immersive, cinematic game experiences. Built on GPU-accelerated GLSL shader technology, the system enables developers to craft atmospheric environments, highlight interactive elements, and implement signature retro-aesthetic touches that define the framework's visual identity.

The visual effects system represents one of the framework's most distinctive technical features, providing:
- **Cinematic Atmosphere**: Film-inspired visual styling including color grading and lighting effects
- **Interactive Highlighting**: Object emphasis through sophisticated desaturation and brightness effects
- **Retro Aesthetics**: CRT simulation and other vintage display effects
- **Dynamic Environment**: Weather, time-of-day, and mood-based visual transformations
- **Performance-Optimized Implementation**: GPU-accelerated effects with minimal performance impact

**By the end of this chapter, you will master:**
- The complete architecture of the framework's shader-based effects system
- Implementation techniques for the CRT effect system with advanced customization
- The desaturation system for interactive object highlighting
- Cinematic letterbox and Neo-Noir atmospheric effects
- Performance optimization and troubleshooting for shader systems
- Creating custom effects through GLSL shader development and integration

## Understanding Shader-Based Visual Effects

The framework's visual effects system leverages the power of GPU-accelerated GLSL (OpenGL Shading Language) shaders to create sophisticated visual transformations with minimal performance impact. These shaders operate directly on the graphics hardware, allowing for complex real-time effects that would be prohibitively expensive to calculate on the CPU.

### Principles of GLSL in the Framework

**GPU-Accelerated Processing**: Shaders operate directly on graphics hardware for optimal performance:

```glsl
// Example: Basic GLSL fragment shader for color tinting
#ifdef GL_ES
precision mediump float;
#endif

uniform sampler2D tex0;  // Original texture
uniform vec4 u_tint;      // Tint color

varying vec2 v_tex_coord; // Texture coordinate

void main() {
    // Sample original pixel
    vec4 original = texture2D(tex0, v_tex_coord);
    
    // Apply tint effect
    vec4 tinted = original * u_tint;
    
    // Output final color
    gl_FragColor = tinted;
}
```

**Ren'Py Integration**: The framework provides seamless integration with Ren'Py's screen and transform systems:

```python
# Integration with Ren'Py transform system
transform noir_effect:
    shader "noir_shader"
    u_contrast 1.5
    u_brightness -0.1
    u_saturation 0.2

# Usage in screens
screen noir_scene():
    add "background.png" at noir_effect
    
    # Interactive object with different effect
    imagebutton:
        idle "clue.png"
        hover Transform("clue.png", shader="highlight_shader", u_intensity=0.8)
        action Function(examine_clue)
```

**Parameter Control System**: Dynamic adjustment of shader parameters during gameplay:

```python
# Dynamic shader parameter control
def increase_tension():
    # Gradually intensify visual effects
    for i in range(10):
        renpy.pause(0.2)
        # Update shader parameters - becomes more red and contrasty
        renpy.set_shader_parameter("tension_shader", "u_red_tint", i/10.0)
        renpy.set_shader_parameter("tension_shader", "u_contrast", 1.0 + i/5.0)
```

## Effects System Overview

The framework's visual effects are organized into several interconnected systems:

### 1. Core Shader Systems
- **CRT Effect System**: Simulates vintage cathode ray tube displays
- **Desaturation System**: Object highlighting through selective color manipulation
- **Letterbox System**: Cinematic black bars for dramatic scenes
- **Neo-Noir Atmosphere System**: Film noir-inspired visual styling

### 2. Integration Layers
- **Global Effects**: Applied to the entire scene (CRT, color grading)
- **Room Effects**: Per-room atmospheric settings
- **Object Effects**: Interactive element highlighting
- **Dialog Effects**: Cinematic framing for conversations

## CRT Shader System

### Purpose and Visual Impact
The CRT shader simulates vintage cathode ray tube monitors, complete with curvature, scanlines, and color separation. This effect is instrumental in creating the retro-cinematic aesthetic central to the framework's visual identity.

### Key Features
- **Screen Curvature**: Simulates the bulging effect of CRT screens
- **Scanlines**: Horizontal lines that mimic electron beam scanning
- **Chroma Shift**: RGB channel separation for authentic color bleeding
- **Vignette Effect**: Edge darkening for a more focused view
- **Scanline Animation**: Optional movement simulation

### Technical Implementation
The CRT system uses a two-pass GLSL shader with vertex and fragment stages:

```glsl
// Fragment shader excerpt (simplified)
vec2 curved_uv = curve(v_tex_coord);  // Apply screen curvature

// Apply scanlines
float scanline = sin(curved_uv.y * u_resolution.y * u_scanline_size);
scanline = 1.0 - (u_scanline_intensity * scanline * scanline);

// Apply chromatic aberration
vec2 r_offset = vec2(u_chroma_amount, 0.0);
vec2 g_offset = vec2(0.0, 0.0);
vec2 b_offset = vec2(-u_chroma_amount, 0.0);

float r = texture2D(tex0, curved_uv + r_offset).r;
float g = texture2D(tex0, curved_uv + g_offset).g;
float b = texture2D(tex0, curved_uv + b_offset).b;

// Apply vignette
float vignette = calculate_vignette(curved_uv, u_vignette_width, u_vignette_strength);

// Final color
vec4 color = vec4(r, g, b, 1.0) * scanline * vignette;
```

### Usage in Ren'Py

```python
# Apply CRT effect to a displayable
image background_with_crt = im.Composite(
    (1280, 720),
    (0, 0), "images/background.png",
    None, Transform(child=None, shader="crt_shader", mesh=True)
)

# Or use as a transform
transform crt_effect:
    shader "crt_shader"
    mesh True
    u_warp 0.12
    u_scanline_size 1.0
    u_scanline_intensity 0.18
    u_chroma_amount 0.003
    u_vignette_width 0.85
    u_vignette_strength 0.45
```

### Configuration Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `u_warp` | 0.0-0.5 | 0.12 | Screen curvature intensity |
| `u_scanline_size` | 0.1-4.0 | 1.0 | Size of scanlines (higher = more lines) |
| `u_scanline_intensity` | 0.0-1.0 | 0.18 | Darkness of scanlines |
| `u_chroma_amount` | 0.0-0.01 | 0.003 | Color channel separation amount |
| `u_vignette_width` | 0.5-1.0 | 0.85 | Width of visible area before vignette |
| `u_vignette_strength` | 0.0-1.0 | 0.45 | Darkness of vignette edges |

### In-Game Controls

| Key | Function |
|-----|----------|
| `C` | Toggle CRT shader on/off |
| `A` | Toggle scanline animation |
| `1-4` | Scanline size presets (small to large) |
| `[ / ]` | Decrease/increase vignette strength |
| `- / =` | Decrease/increase vignette width |
| `0` | Reset CRT parameters to defaults |

### Performance Considerations
- Adds approximately 2-3ms to render time when enabled
- Most expensive during animation (when `A` is toggled on)
- Disable for performance-critical scenes if needed

## Desaturation System

### Purpose and Visual Impact
The desaturation system replaces the traditional bloom effect for highlighting interactive objects. It manipulates saturation and brightness to draw attention to objects under the cursor or during interaction, creating a subtle yet effective visual cue.

### Key Features
- **Adaptive Highlighting**: Automatically adjusts based on object color
- **Animation Options**: Pulsing, static, or timed transitions
- **Customizable Intensity**: Multiple presets for different object types
- **Seamless Integration**: Automatic activation on hover

### Technical Implementation
Implemented using MatrixColor transforms with smooth transitions:

```python
transform object_desaturation_highlight(intensity=0.5, alpha_min=0.2, alpha_max=0.7, pulse_speed=1.0):
    matrixcolor TransformMatrix()
    ease 0.3 matrixcolor BrightnessMatrix(intensity/2)
    block:
        ease pulse_speed matrixcolor BrightnessMatrix(intensity * alpha_max)
        ease pulse_speed matrixcolor BrightnessMatrix(intensity * alpha_min)
        repeat
```

### Preset System
The framework includes 24 different desaturation presets organized in categories:

```python
define DESATURATION_PRESETS = {
    # Basic presets
    "subtle": {
        "desaturation_intensity": 0.3,
        "desaturation_alpha_min": 0.2,
        "desaturation_alpha_max": 0.5,
        "desaturation_pulse_speed": 0.8,
        "desaturation_fade_duration": 0.4
    },
    "moderate": { ... },
    "intense": { ... },
    
    # EXPLOSIVE variants - fast, high-contrast highlighting
    "explosive_subtle": { ... },
    "explosive_normal": { ... },
    "explosive_intense": { ... },
    
    # WHISPER variants - very subtle, slow highlighting
    "whisper_subtle": { ... },
    
    # HEARTBEAT variants - rhythmic pulsing
    "heartbeat_normal": { ... },
    
    # FLICKER variants - rapid, erratic highlighting
    "flicker_intense": { ... },
    
    # ETHEREAL variants - dreamy, floating feel
    "ethereal_subtle": { ... }
    # ... and more
}
```

### Usage in Object Definitions

```python
# Object with custom desaturation settings
ROOM1_OBJECTS = {
    "important_clue": {
        "image": "clue.png",
        "position": (400, 300),
        "actions": ["Examine", "Take"],
        "desaturation_intensity": 0.8,
        "desaturation_pulse_speed": 1.5,
        "desaturation_preset": "explosive_intense"
    },
    "background_object": {
        "image": "bookshelf.png",
        "position": (600, 200),
        "actions": ["Examine"],
        "desaturation_preset": "whisper_subtle"
    }
}
```

### Applying Presets Programmatically

```python
def on_object_hover(room_id, obj):
    # Dynamic preset based on story progress
    if obj == "mysterious_device" and not store.player_knows_purpose:
        apply_desaturation_preset(obj, "whisper_subtle")
    elif obj == "mysterious_device" and store.player_knows_purpose:
        apply_desaturation_preset(obj, "explosive_normal")
```

## Letterbox System

### Purpose and Visual Impact
The letterbox effect adds black bars to the top and bottom of the screen, creating a cinematic aspect ratio. This is particularly effective for dramatic dialogue scenes, cutscenes, or to focus attention on specific parts of a scene.

### Key Features
- **GLSL Shader-Based**: Pure GPU implementation for optimal performance
- **Animated Transitions**: Smooth height and opacity animations
- **Adaptive UI Integration**: Automatically adjusts UI elements when active
- **Dialog Integration**: Can activate automatically during conversations

### Technical Implementation

```glsl
// Letterbox fragment shader (simplified)
uniform float u_height;    // Height of bars (0.0-0.5)
uniform float u_alpha;     // Opacity (0.0-1.0)

void main() {
    vec4 color;
    
    // Check if pixel is in letterbox region
    if (v_tex_coord.y < u_height || v_tex_coord.y > 1.0 - u_height) {
        color = vec4(0.0, 0.0, 0.0, u_alpha);
    } else {
        // Transparent for non-letterbox area
        color = vec4(0.0, 0.0, 0.0, 0.0);
    }
    
    gl_FragColor = color;
}
```

### Animation Functions

```python
# Letterbox animation transforms
transform letterbox_ease_in(duration=0.5, height=0.12):
    shader "letterbox_shader"
    u_height 0.0 u_alpha 0.0
    ease duration u_height height u_alpha 1.0

transform letterbox_ease_out(duration=0.5):
    shader "letterbox_shader"
    ease duration u_height 0.0 u_alpha 0.0
```

### Usage Examples

```python
# Manual letterbox control
def enable_cinematic_mode():
    renpy.show("letterbox_overlay", at_list=[letterbox_ease_in()])
    # Adjust UI for letterbox mode
    renpy.show_screen("letterbox_say")

def disable_cinematic_mode():
    renpy.show("letterbox_overlay", at_list=[letterbox_ease_out()])
    # Restore normal UI
    renpy.hide_screen("letterbox_say")

# Automatic integration with dialogue
def detective_conversation():
    # Enable letterbox before dialogue
    enable_cinematic_mode()
    
    detective "The evidence points to one conclusion..."
    player "What do you mean?"
    
    # Disable letterbox after dialogue
    disable_cinematic_mode()
```

### Letterbox Speed Presets

| Preset | In Duration | Out Duration | Description |
|--------|-------------|--------------|-------------|
| Very Slow | 2.0s | 2.0s | Gradual, dramatic transition |
| Slow | 1.2s | 1.2s | Deliberate cinematic feel |
| Normal | 0.8s | 0.8s | Balanced transition (default) |
| Fast | 0.5s | 0.5s | Quick, subtle transition |
| Very Fast | 0.3s | 0.3s | Almost immediate |

## Neo-Noir Atmospheric Effects

### Purpose and Visual Impact
The Neo-Noir system provides atmospheric color grading and lighting effects inspired by film noir and neo-noir aesthetics. These effects create mood, emphasize narrative themes, and enhance the visual storytelling.

### Color Grading Presets

| Preset | Description | Visual Effect |
|--------|-------------|---------------|
| Classic Noir | High-contrast black and white | Stark shadows, film noir aesthetic |
| Neon Night | Saturated blues and purples | Cyberpunk-inspired night scenes |
| Rain Streets | Blue-green tint with lowered saturation | Wet, rainy atmosphere |
| Smoky Bar | Warm amber tones with haze | Intimate, mysterious interior |
| Detective Office | Desaturated sepia tones | Vintage investigation scenes |
| Crime Scene | High-contrast with red emphasis | Highlights evidence and tension |
| Blade Runner | Orange and teal contrast | Futuristic dystopian feel |

### Lighting Effect Presets

| Preset | Description | Visual Effect |
|--------|-------------|---------------|
| Street Lamp | Directional yellow-orange light | Pools of light in darkness |
| Neon Signs | Pulsing colored light | Urban nightlife atmosphere |
| Window Blinds | Striped shadow pattern | Classic noir interrogation look |
| Police Lights | Alternating red and blue | Emergency situation |
| Desk Lamp | Focused warm light | Intimate investigation feel |
| Car Headlights | Strong directional white light | Dramatic confrontation |
| Interrogation | Harsh overhead light | Uncomfortable questioning |
| Sunset Window | Orange-red directional light | End of day, reflection |

### Usage in Room Definitions

```python
# Room with atmospheric presets
ROOM_DEFINITIONS = {
    "interrogation_room": {
        "background": "images/interrogation_room.png",
        "color_grade": "classic_noir",
        "lighting": "interrogation",
        "film_grain": 0.4,
        "letterbox_enabled": True
    },
    "neon_alley": {
        "background": "images/alley.png",
        "color_grade": "neon_night",
        "lighting": "neon_signs",
        "film_grain": 0.6,
        "fog_density": 0.3
    }
}
```

### Dynamic Atmosphere Control

```python
# Change atmosphere based on story events
def on_object_interact(room_id, obj, action):
    if room_id == "office" and obj == "window" and action == "Look":
        if store.time_of_day == "evening":
            # Transition to sunset lighting
            set_color_grade("detective_office")
            set_lighting("sunset_window")
            renpy.with_statement(dissolve)
            renpy.say(None, "The sun casts long shadows through the blinds.")
            return True
        elif store.time_of_day == "night":
            # Transition to night atmosphere
            set_color_grade("neon_night")
            set_lighting("street_lamp")
            renpy.with_statement(dissolve)
            renpy.say(None, "The street lamps illuminate the empty streets below.")
            return True
    return False
```

## In-Game Control System

### Keyboard Shortcuts

#### CRT Controls
- **C**: Toggle CRT effect on/off
- **A**: Toggle CRT scanline animation
- **1-4**: CRT scanline size presets
- **[ / ]**: Adjust vignette strength
- **- / =**: Adjust vignette width
- **0**: Reset CRT settings

#### Effect Controls
- **L**: Toggle letterbox effect
- **Shift+G**: Cycle film grain intensity
- **Shift+F**: Cycle fog effect
- **Shift+V**: Cycle vintage color effects
- **Shift+L**: Cycle lighting effects
- **Shift+W**: Cycle weather effects

#### Atmosphere Controls
- **Alt+A**: Cycle through atmosphere presets
- **Alt+I**: Cycle through investigation modes
- **R**: Reset all shader effects
- **H**: Show shader help overlay

#### System Controls
- **I**: Toggle info overlay
- **Cmd+Shift+F12 / Ctrl+Shift+F12**: Cycle debug overlay

### In-Game Help
Press **H** during gameplay to display an on-screen reference of all available shader controls and their current status.

## Performance Optimization

### System Requirements
- **Minimum**: OpenGL 2.0+ compatible GPU
- **Recommended**: Dedicated GPU with 2GB+ VRAM
- **Mobile**: Most effects work on modern mobile GPUs with reduced quality

### Performance Impact

| Effect | Performance Cost | Notes |
|--------|------------------|-------|
| CRT | 2-3ms | Higher with animation enabled |
| Desaturation | 0.5-1ms | Only active on hovered objects |
| Letterbox | <0.5ms | Negligible impact |
| Color Grading | 1-2ms | Consistent cost when enabled |
| Lighting | 1-2ms | Cost varies with complexity |
| Film Grain | 1ms | Cost increases with intensity |
| Fog | 1-2ms | Varies with density and animation |

### Optimization Tips

1. **Selective Usage**: Only enable effects when narratively appropriate
2. **Preset Combinations**: Test preset combinations for performance
3. **Mobile Considerations**: Use `is_mobile = renpy.mobile` to detect and adjust shader complexity
4. **Debug Mode**: Enable `shader_debug_enabled` to see performance metrics

```python
# Example performance-aware shader application
init python:
    def apply_performance_appropriate_effects():
        if renpy.mobile:
            # Simplified effects for mobile
            set_color_grade("detective_office_mobile")
            film_grain_enabled = False
        elif renpy.get_renderer_info()["renderer"] == "sw":
            # Software renderer fallbacks
            use_simplified_effects()
        else:
            # Full effects for desktop
            set_color_grade("detective_office")
            set_lighting("desk_lamp")
            film_grain_enabled = True
```

## Extending the Shader System

### Creating Custom Color Grades

```python
# Define a new color grade preset
transform color_grade_cyberpunk:
    matrixcolor ContrastMatrix(1.2) * \
                SaturationMatrix(1.4) * \
                ColorizeMatrix("#0066ff", "#ff00aa", 0.25) * \
                BrightnessMatrix(0.05)

# Register the new preset
init python:
    color_grade_presets["cyberpunk"] = color_grade_cyberpunk
```

### Custom Lighting Effects

```python
# Create custom lighting effect
transform lighting_emergency:
    # Base transform
    transform_anchor True
    
    # Lighting parameters
    shader "lighting_shader"
    u_light_direction (0.5, -1.0)
    u_light_color (0.9, 0.1, 0.1)
    u_light_intensity 0.8
    u_ambient_intensity 0.2
    
    # Animation
    block:
        ease 0.7 u_light_color (0.9, 0.1, 0.1)
        ease 0.7 u_light_color (0.1, 0.1, 0.9)
        repeat
```

### Shader Development Best Practices

1. **Test Across Devices**: Ensure compatibility with different GPUs and mobile
2. **Optimize Early**: Monitor performance from the start of development
3. **Provide Fallbacks**: Include non-shader alternatives for unsupported platforms
4. **Document Parameters**: Keep clear notes on what each uniform parameter affects
5. **Incremental Development**: Add features one at a time, testing thoroughly

## Troubleshooting

### Common Issues

#### Shader Compilation Errors
- **Symptoms**: Black screen, missing effects, error in log
- **Fix**: Check syntax in GLSL code, ensure compatibility with OpenGL ES 3.0

#### Performance Problems
- **Symptoms**: Low framerate, stuttering
- **Fix**: Reduce shader complexity, disable animated effects, check for uniform update spam

#### Visual Artifacts
- **Symptoms**: Flickering, incorrect colors, z-fighting
- **Fix**: Check transform order, ensure proper mesh True settings, validate shader math

#### Mobile Compatibility
- **Symptoms**: Effects not working on mobile devices
- **Fix**: Use simpler shader variants, avoid complex math, reduce texture lookups

### Diagnostic Tools

```python
# Enable shader debugging
define config.log_gl_shaders = True
define shader_debug_enabled = True

# Performance tracking
define shader_performance_logging = True
```

Activate the debug overlay (Ctrl+Shift+F12) to view real-time shader performance metrics and status.

## Reference Tables

### Effect Combinations for Common Scenes

| Scene Type | Color Grade | Lighting | Additional Effects |
|------------|-------------|----------|-------------------|
| Office Investigation | detective_office | desk_lamp | film_grain=0.3 |
| Night Street | neon_night | street_lamp | film_grain=0.4, fog=0.2 |
| Interrogation | classic_noir | interrogation | letterbox=True |
| Flashback | vintage | soft_diffuse | bloom=0.4, desaturation=0.3 |
| Crime Scene | crime_scene | police_lights | film_grain=0.5 |
| Tense Confrontation | blade_runner | car_headlights | letterbox=True, film_grain=0.3 |

### Object Highlighting for Different Item Types

| Item Type | Recommended Preset | Intensity | Notes |
|-----------|-------------------|-----------|-------|
| Critical Evidence | explosive_intense | 0.8-1.0 | Strong pulsing effect |
| Key Items | heartbeat_normal | 0.6-0.8 | Regular pulsating highlight |
| Interactive Objects | moderate | 0.4-0.6 | Standard highlighting |
| Background Items | whisper_subtle | 0.2-0.4 | Very subtle effect |
| Hidden Objects | flicker_subtle | 0.3-0.5 | Slight flickering effect |

## Advanced Shader Techniques

The framework supports advanced shader patterns for complex visual effects that go beyond the standard presets. These techniques enable sophisticated visual storytelling and immersive atmospheric control.

### Multi-Pass Effects

Combine multiple shader effects using a layered rendering approach:

```python
# Complex multi-pass shader system
transform noir_scene_composite:
    # Base layer: Color grading
    matrixcolor SaturationMatrix(0.3) * ContrastMatrix(1.3)
    
    # Pass 1: Film grain overlay
    child ("film_grain_texture")
    blend "multiply"
    alpha 0.4
    
    # Pass 2: Lighting overlay
    shader "directional_light"
    u_light_angle 45.0
    u_light_intensity 0.7
    
    # Pass 3: Atmospheric effects
    shader "fog_overlay"
    u_fog_density 0.2
    u_fog_color (0.8, 0.8, 1.0)
    
    # Pass 4: Vignette
    matrixcolor TintMatrix("#000040") * BrightnessMatrix(-0.1)
```

### State-Responsive Visual Effects

Create effects that respond to game state, player actions, or narrative progression:

```python
# Dynamic tension system
define tension_levels = [
    {
        "name": "calm",
        "desaturation": 0.1,
        "contrast": 1.0,
        "film_grain": 0.0,
        "letterbox": False
    },
    {
        "name": "suspicious",
        "desaturation": 0.3,
        "contrast": 1.2,
        "film_grain": 0.2,
        "letterbox": False
    },
    {
        "name": "dangerous",
        "desaturation": 0.6,
        "contrast": 1.4,
        "film_grain": 0.4,
        "letterbox": True,
        "color_tint": (1.0, 0.8, 0.8)  # Slight red tint
    }
]

# Apply tension-based effects
def set_tension_level(level_name):
    level_config = next((l for l in tension_levels if l["name"] == level_name), None)
    if level_config:
        # Apply desaturation
        renpy.set_shader_parameter("atmosphere_shader", "u_desaturation", level_config["desaturation"])
        
        # Apply contrast
        renpy.set_shader_parameter("atmosphere_shader", "u_contrast", level_config["contrast"])
        
        # Toggle letterbox if needed
        if level_config["letterbox"]:
            enable_cinematic_mode()
        else:
            disable_cinematic_mode()
        
        # Optional color tint
        if "color_tint" in level_config:
            renpy.set_shader_parameter("atmosphere_shader", "u_tint", level_config["color_tint"])
```

### Time-Based and Weather Effects

Implement dynamic environmental effects that change over time:

```python
# Time of day shader system
transform time_of_day_atmosphere(hour):
    if hour >= 6 and hour < 12:  # Morning
        shader "morning_light"
        u_sun_position (0.2, 0.8)
        u_light_color (1.0, 0.95, 0.8)
        u_light_intensity 0.9
    elif hour >= 12 and hour < 17:  # Afternoon
        shader "afternoon_light"
        u_sun_position (0.8, 0.9)
        u_light_color (1.0, 0.9, 0.7)
        u_light_intensity 1.0
    elif hour >= 17 and hour < 20:  # Evening
        shader "evening_light"
        u_sun_position (-0.2, 0.6)
        u_light_color (1.0, 0.6, 0.4)
        u_light_intensity 0.7
    else:  # Night
        shader "night_atmosphere"
        u_ambient_color (0.1, 0.15, 0.3)
        u_light_intensity 0.3

# Weather effects
transform weather_rain(intensity=0.5):
    # Rain shader with droplet effects
    shader "weather_rain"
    u_rain_intensity intensity
    u_rain_speed 2.0
    u_droplet_size 1.5
    
    # Atmospheric effects
    matrixcolor SaturationMatrix(0.7) * TintMatrix("#88AACC") * BrightnessMatrix(-0.15)
    
    # Rain animation
    block:
        ease 3.0 u_rain_offset 1.0
        ease 0.0 u_rain_offset 0.0
        repeat

# Usage in scenes
label afternoon_investigation:
    $ current_hour = 14
    scene office_background at time_of_day_atmosphere(current_hour)
    
    if weather == "rain":
        show rain_overlay at weather_rain(0.7)
    
    "The afternoon light streams through the blinds..."
```

### Interactive Shader Parameters

Create effects that respond directly to player actions:

```python
# Mouse-responsive lighting effect
transform interactive_lighting:
    shader "mouse_light"
    
    # Use mouse position for light direction
    u_light_x (renpy.get_mouse_pos()[0] / config.screen_width)
    u_light_y (renpy.get_mouse_pos()[1] / config.screen_height)
    u_light_intensity 0.8
    u_light_radius 300.0

# Stress-responsive visual effects
def on_object_interact(room_id, obj, action):
    global player_stress
    
    if action == "Examine" and obj in stress_inducing_objects:
        player_stress += 10
        
        # Apply stress-based visual distortion
        stress_level = min(player_stress / 100.0, 1.0)
        
        renpy.set_shader_parameter("stress_shader", "u_distortion", stress_level * 0.05)
        renpy.set_shader_parameter("stress_shader", "u_red_shift", stress_level * 0.3)
        renpy.set_shader_parameter("stress_shader", "u_vignette", stress_level * 0.6)
        
        # Optional screen shake
        if stress_level > 0.7:
            renpy.show("screen_shake", at_list=[screen_shake_transform(stress_level)])
```

## Custom Shader Development Workflow

### GLSL Shader Structure

The framework expects shaders to follow a specific structure for integration with Ren'Py:

```glsl
// Vertex shader (effects.vert)
attribute vec2 a_position;
attribute vec2 a_tex_coord;

uniform mat4 u_transform;

varying vec2 v_tex_coord;

void main() {
    gl_Position = u_transform * vec4(a_position, 0.0, 1.0);
    v_tex_coord = a_tex_coord;
}
```

```glsl
// Fragment shader (effects.frag)
#ifdef GL_ES
precision mediump float;
#endif

uniform sampler2D tex0;

// Framework-provided uniforms
uniform vec2 u_resolution;
uniform float u_time;

// Custom uniforms
uniform float u_custom_parameter;

varying vec2 v_tex_coord;

void main() {
    vec4 original_color = texture2D(tex0, v_tex_coord);
    
    // Apply your custom effect
    vec4 modified_color = apply_custom_effect(original_color, u_custom_parameter);
    
    gl_FragColor = modified_color;
}
```

### Shader Integration Process

1. **Development**: Create GLSL shaders in the `game/shaders/` directory
2. **Registration**: Register shaders in `00-shader-registry.rpy`:

```python
# Register custom shader
init python:
    renpy.register_shader("custom_effect", 
                         vertex="shaders/custom_effect.vert",
                         fragment="shaders/custom_effect.frag")
    
    # Define default parameters
    custom_effect_defaults = {
        "u_custom_parameter": 0.5,
        "u_intensity": 1.0,
        "u_blend_mode": 0
    }
```

3. **Transform Creation**: Create Ren'Py transforms for easy use:

```python
transform custom_effect(parameter_value=0.5):
    shader "custom_effect"
    u_custom_parameter parameter_value
    u_intensity 1.0
```

4. **Integration**: Use in screens and displayables:

```python
screen custom_scene():
    add "background.png" at custom_effect(0.8)
```

### Testing and Validation

```python
# Shader testing framework
init python:
    def test_shader_compatibility():
        """Test shader compatibility across different devices."""
        test_results = {}
        
        for shader_name in registered_shaders:
            try:
                # Test compilation
                renpy.test_shader_compilation(shader_name)
                # Test parameter setting
                renpy.test_shader_parameters(shader_name, get_shader_defaults(shader_name))
                # Test performance
                performance = renpy.benchmark_shader(shader_name, frames=60)
                
                test_results[shader_name] = {
                    "compatible": True,
                    "performance": performance
                }
            except Exception as e:
                test_results[shader_name] = {
                    "compatible": False,
                    "error": str(e)
                }
        
        return test_results
```

## Best Practices and Design Guidelines

### Visual Consistency

1. **Establish Visual Language**: Create a consistent set of effects that support your game's aesthetic
2. **Purposeful Usage**: Each effect should serve a narrative or gameplay purpose
3. **Subtle Integration**: Effects should enhance rather than distract from the story
4. **Performance Budget**: Limit simultaneous effects to maintain smooth performance

### Accessibility Considerations

```python
# Accessibility settings for visual effects
define accessibility_settings = {
    "reduce_motion": False,        # Disable animated effects
    "high_contrast": False,       # Increase contrast for visibility
    "no_flashing": False,         # Disable rapid flashing effects
    "simplified_effects": False   # Use simpler shader variants
}

# Apply accessibility-aware effects
def apply_accessible_effect(effect_name, **parameters):
    if accessibility_settings["simplified_effects"]:
        effect_name = effect_name + "_simple"
    
    if accessibility_settings["reduce_motion"]:
        parameters["animation_speed"] = 0.0
    
    if accessibility_settings["no_flashing"]:
        parameters["pulse_enabled"] = False
    
    apply_shader_effect(effect_name, **parameters)
```

### Code Organization

```
/game/
├── shaders/
│   ├── core/               # Core framework shaders
│   │   ├── crt.frag
│   │   ├── desaturation.frag
│   │   └── letterbox.frag
│   ├── atmospheric/        # Atmospheric effects
│   │   ├── noir.frag
│   │   ├── rain.frag
│   │   └── fog.frag
│   ├── lighting/          # Lighting effects
│   │   ├── directional.frag
│   │   └── point_light.frag
│   └── custom/            # Game-specific shaders
│       └── investigation.frag
├── 00-shader-registry.rpy  # Shader registration
├── 01-effect-presets.rpy   # Effect preset definitions
├── 02-shader-controls.rpy  # Control and animation functions
└── 03-performance.rpy      # Performance optimization
```

### Testing Strategies

1. **Multi-Device Testing**: Test on different GPUs, mobile devices, and performance levels
2. **Edge Case Testing**: Test with extreme parameter values and rapid changes
3. **Performance Profiling**: Monitor frame rates and GPU usage during complex scenes
4. **User Testing**: Gather feedback on visual clarity and narrative effectiveness

## Recommended Learning Path

### Phase 1: Foundation (Understanding Built-in Effects)
- [ ] Experiment with CRT effect settings and observe visual changes
- [ ] Test desaturation presets with different object types
- [ ] Practice letterbox timing for dramatic scenes
- [ ] Apply Neo-Noir presets to establish scene atmosphere

### Phase 2: Integration (Combining Effects with Story)
- [ ] Design effect combinations for key story moments
- [ ] Implement state-responsive visual changes
- [ ] Create smooth transitions between different atmospheric states
- [ ] Optimize effect usage for consistent performance

### Phase 3: Customization (Creating Original Effects)
- [ ] Modify existing shader parameters for unique looks
- [ ] Create custom color grading and lighting presets
- [ ] Develop simple custom GLSL shaders
- [ ] Implement interactive or time-based effect systems

### Phase 4: Advanced (Complex Visual Systems)
- [ ] Design multi-pass rendering systems
- [ ] Create accessibility-aware effect alternatives
- [ ] Develop performance optimization strategies
- [ ] Build comprehensive testing and validation frameworks

---

## Next Steps

With a thorough understanding of the visual effects system, you're prepared to create atmospheric, cinematic experiences that enhance your interactive storytelling. The next chapters will build upon this foundation:

- **Chapter 7: Audio and Music Integration** - Synchronizing visual effects with audio cues and dynamic music systems
- **Chapter 8: Input Handling and Player Agency** - Creating responsive interactions that trigger appropriate visual feedback
- **Chapter 9: State Management** - Managing complex visual state changes across save/load cycles
- **Chapter 10: Performance and Optimization** - Advanced optimization techniques for maintaining smooth performance with complex visual systems

The visual effects system provides the foundation for the framework's distinctive cinematic aesthetic. Master these tools to create memorable, immersive experiences that blur the line between games and interactive cinema.

---

**Continue to:** [Chapter 7: Audio and Music Integration](07-Audio-and-Music.md)

