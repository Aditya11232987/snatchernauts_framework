# Effects & Shaders

## Overview
Snatchernauts 0.5.2 introduces a comprehensive shader system built on proper Ren'Py GLSL integration. All effects use the 300-stage pipeline with mesh True transforms for optimal performance.

## Core Effects

### CRT Shader
- **Warp**: Screen curvature simulation
- **Scanlines**: Configurable size and animation
- **Chroma**: Color separation bleeding effect
- **Vignette**: Horizontal edge darkening with live tuning
- **Animation**: Optional scanline movement

### Letterbox System (Shader-Based)
- **Implementation**: Pure GLSL shader rendering (replaces old GUI bars)
- **Animation**: Smooth height and alpha transitions via shader uniforms
- **Integration**: Automatically activates during detective conversations
- **Controls**: Disabled during normal gameplay, smooth fade in/out

### Bloom Effects
- **Color Correlation**: Adaptive bloom based on scene tones
- **Integration**: Works seamlessly with all shader effects
- **Performance**: Optimized rendering pipeline

## Atmospheric Shaders

### Individual Effects
- **Film Grain**: Procedural texture with animated patterns
- **Fog**: Multiple atmospheric presets (light/moderate/heavy/mysterious)
- **Vintage/Sepia**: Retro color grading with noir options
- **Lighting**: Dynamic lighting effects (candlelight/streetlight/moonlight)
- **Rain/Weather**: Particle effects and storm atmospheres
- **Depth of Field**: Focus effects (center/left/right/close)
- **Edge Detection**: Evidence highlighting and danger visualization
- **Color Grading**: Scene mood adjustment (cool/warm/noir/vintage)

### Detective-Specific Shaders
- **Mystery Reveal**: Progressive unveiling effects
- **Flashlight**: Investigative lighting with multiple beam types
- **Atmospheric Presets**: Crime scene, interrogation room, warehouse ambiance
- **Investigation Modes**: Evidence analysis, suspect tracking, revelation moments

## Shader Control System

### Individual Shader Hotkeys
- **Shift+G**: Film Grain cycling
- **Shift+F**: Fog effects
- **Shift+V**: Vintage/Sepia
- **Shift+L**: Lighting effects
- **Shift+W**: Weather/Rain
- **Shift+D**: Depth of Field
- **Shift+C**: Color Grading
- **Shift+E**: Edge Detection
- **Shift+M**: Mystery Reveal
- **Shift+T**: Flashlight

### Preset Systems
- **Alt+A**: Atmosphere presets (crime scene, abandoned building, etc.)
- **Alt+I**: Investigation modes (evidence analysis, suspect tracking, etc.)
- **R**: Reset all shader effects
- **H**: Toggle shader help overlay

### Reverse Cycling
All shader hotkeys support reverse cycling with **Ctrl+Shift+Key**

## Technical Implementation

### Shader Registration
```renpy
renpy.register_shader(
    "shader_name",
    variables="""...""",  # GLSL uniform declarations
    vertex_300="""...""", # Vertex shader stage
    fragment_300="""...""" # Fragment shader stage
)
```

### Transform Usage
```renpy
transform effect_transform:
    mesh True  # Required for coordinate computation
    shader "shader_name"
    # Animate shader uniforms
    ease 1.0 u_parameter 1.0
```

### Integration APIs
- `apply_room_shader_effects()`: Get current room shader transform
- `get_shader_transform_for_object()`: Object-specific shader handling
- `cycle_shader_preset()`: Programmatic shader control
- `reset_all_shaders()`: Clear all active effects

## Debug & Effects Keys

### Core System
- **i**: toggle info overlay
- **c**: toggle CRT • **a**: toggle scanline animation
- **1–4**: scanline size presets
- **[ / ]**: vignette strength • **- / =**: vignette width • **0**: reset
- **l**: toggle letterbox (shader-based)

### Shader System
- **Individual effects**: Shift+G/F/V/L/W/D/C/E/M/T
- **Atmosphere presets**: Alt+A
- **Investigation modes**: Alt+I
- **Reset/Help**: R / H

### Debug
- **Cmd+Shift+F12 / Ctrl+Shift+F12**: cycle debug overlay

## Performance Notes
- All shaders use optimized GLSL with proper coordinate handling
- Effects can be layered without significant performance impact
- Mesh True transforms enable hardware acceleration
- Developer controls allow real-time parameter tuning

