# Visual Effects & Shaders System

## Introduction

The Snatchernauts Framework includes a comprehensive visual effects system designed to create an immersive, cinematic experience. Based on GPU-accelerated GLSL shaders, these effects enable developers to create atmospheric environments, highlight interactive objects, and add retro-aesthetic touches with minimal performance impact.

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

