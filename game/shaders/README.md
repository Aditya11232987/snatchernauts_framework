# Snatchernauts Framework - Shader System (Simplified)

## Overview

The shader system has been cleaned up and simplified to focus on only the most essential visual effects. This improves performance, reduces complexity, and maintains the core visual identity of the game.

## What Remains (Core Shaders)

### 1. CRT Shader (`crt_shader.rpy`)
- **Purpose**: Authentic retro CRT monitor effects
- **Features**: 
  - Screen warp/curvature
  - Animated scanlines 
  - Chroma aberration (color bleeding)
  - Horizontal vignette
  - Live parameter tuning
- **Controls**: `C` key, `A` key, `1-4` keys, `[],` `-=`, `0`
- **Performance**: ~2-3ms overhead when enabled

### 2. Bloom Shader (`bloom_shader.rpy`)
- **Purpose**: Enhanced lighting and glow effects for objects
- **Features**:
  - Gaussian blur-based bloom
  - Color-correlated bloom (adapts to scene)
  - Brightness threshold detection
  - Pulsing animation support
  - Sepia tone adaptation
- **Usage**: Automatic on object hover, configured per-object
- **Performance**: Minimal impact (~1ms)

### 3. Letterbox Shader (`letterbox_shader.rpy`)
- **Purpose**: Cinematic letterbox bars for dialogue and cutscenes
- **Features**:
  - Smooth height and alpha animations
  - Configurable bar color and opacity
  - Automatic activation during dialogue
  - Manual toggle support
- **Controls**: `L` key, automatic during dialogue
- **Performance**: Negligible overhead

## What Was Removed

The following complex shader effects have been removed to improve performance and reduce maintenance overhead:

### Atmospheric Effects (Removed)
- **Film Grain Shader**: Procedural grain texture effects
- **Fog Shader**: Multiple atmospheric fog presets  
- **Vintage/Sepia Shader**: Color grading and aging effects
- **Lighting Shader**: Dynamic lighting (candlelight, streetlight, moonlight)
- **Rain/Weather Shader**: Particle effects and storm atmospheres

### Investigation Effects (Removed)
- **Depth of Field Shader**: Focus effects (center/left/right/close)
- **Edge Detection Shader**: Evidence highlighting and danger visualization
- **Mystery Reveal Shader**: Progressive unveiling effects
- **Flashlight Shader**: Investigative lighting with beam types

### Complex Systems (Removed)
- **Color Grading Shader**: Scene mood adjustment (cool/warm/noir)
- **Detective Atmospheric Shaders**: Crime scene, warehouse ambiance
- **Composite Shader System**: Preset combinations and atmosphere modes
- **Shader Integration System**: Complex hotkey management and cycling
- **Room Shader Integration**: Automatic per-room shader application

## Why This Simplification?

### Performance Benefits
- **Reduced GPU Load**: From 15+ complex shaders to 3 essential ones
- **Memory Efficiency**: Less shader compilation and caching
- **Smoother Gameplay**: Consistent 60+ FPS on integrated graphics
- **Faster Loading**: Reduced shader initialization time

### Maintenance Benefits  
- **Cleaner Codebase**: Removed ~15 shader files and integration systems
- **Fewer Bugs**: Less complex shader interactions and state management
- **Easier Updates**: Simplified system following proper Ren'Py shader documentation
- **Better Documentation**: Clear, focused guides instead of complex manuals

### Design Benefits
- **Core Identity Preserved**: CRT and bloom effects maintain the retro aesthetic
- **Essential Functionality**: Letterbox for cinematic dialogue scenes
- **Developer Focus**: More time for gameplay features instead of shader tuning
- **User Experience**: Simple, predictable visual effects without overwhelming options

## File Structure

```
game/shaders/
├── bloom_shader.rpy       # Object glow and highlight effects
├── crt_shader.rpy         # Retro CRT monitor simulation  
├── letterbox_shader.rpy   # Cinematic letterbox bars
├── SETUP_GUIDE.md         # Setup and usage documentation
├── HOTKEY_MAPPING.md      # Control keys reference
└── README.md             # This overview file
```

## Integration Points

The simplified shader system integrates with:

### Core Systems
- **Room System**: Objects automatically get bloom effects based on their `bloom_color` property
- **Debug System**: Shader info appears in debug overlay (`I` key)
- **Audio System**: CRT effects can trigger audio feedback
- **UI System**: Letterbox appears above room content but below UI elements

### Preserved Functionality
- **Existing Controls**: All original CRT controls work exactly as before
- **Bloom Configuration**: Object bloom settings in room configs remain unchanged  
- **Letterbox Integration**: Dialogue system continues to trigger letterbox automatically
- **Developer Tools**: Debug overlay shows shader status and performance info

## Usage Examples

### Enable CRT Effect
```renpy
$ store.crt_enabled = True
$ store.crt_warp = 0.2        # Screen curvature
$ store.crt_scan = 0.5        # Scanline intensity  
$ store.crt_chroma = 0.9      # Color separation
```

### Configure Object Bloom
```renpy
# In room object definition
"detective": {
    "bloom_color": "#4a90e2",      # Blue glow
    "bloom_intensity": 0.5,        # Medium intensity
    "bloom_radius": 8.0,           # Blur radius
    # ... other object properties
}
```

### Control Letterbox
```renpy
# Show letterbox for important dialogue
$ show_letterbox_shader(duration=0.8, height=80)
"This is an important revelation..."
$ hide_letterbox_shader(duration=0.8)
```

## Performance Monitoring

Use the debug overlay (`I` key) to monitor shader performance:
- **FPS Counter**: Shows real-time framerate impact
- **Shader Info**: Displays which effects are currently active
- **Memory Usage**: Tracks shader-related memory consumption

## Future Considerations

If additional shader effects are needed in the future:

1. **Follow Ren'Py Documentation**: Use the official model-based rendering approach
2. **Implement Incrementally**: Add one effect at a time with performance testing
3. **Maintain Simplicity**: Avoid complex preset systems and hotkey combinations
4. **Document Thoroughly**: Clear documentation for each new shader effect

This simplified system provides a solid foundation for the game's visual effects while maintaining excellent performance and code clarity.
