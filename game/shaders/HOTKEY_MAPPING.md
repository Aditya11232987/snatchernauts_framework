# Complete Hotkey Mapping for Detective Game Shaders

This document outlines the comprehensive solution for managing shader hotkeys without conflicts.

## The Problem
- Limited single keys available for hotkeys
- Existing game already uses many keys (c, f, l, i, a, 1-4, [, ], -, =, 0)
- Need to control 10+ different shader effects plus presets

## The Solution: Multi-Level Hotkey System

### Level 1: Core Controls (Single Keys)
```
S - Shader Menu (main interface)
H - Quick Help Toggle
R - Reset All Shaders
```

### Level 2: Individual Shader Cycling (Shift + Key)
```
Shift+G - Film Grain        (off → subtle → moderate → heavy)
Shift+F - Fog Effects       (off → light → moderate → heavy → mysterious)  
Shift+V - Vintage/Sepia     (off → light → moderate → heavy → noir)
Shift+L - Lighting          (off → candlelight → streetlight → moonlight)
Shift+W - Weather/Rain       (off → drizzle → moderate → heavy → storm)
Shift+D - Depth of Field    (off → center → left → right → close)
Shift+C - Color Grading     (off → cool → warm → noir → vintage)
Shift+E - Edge Detection    (off → subtle → evidence → danger)
Shift+M - Mystery Reveal    (off → slow → fast)
Shift+T - Flashlight/Torch  (off → narrow → wide → police → detective)
```

### Level 3: Reverse Cycling (Ctrl+Shift + Key)
```
All same keys as Level 2, but cycles backwards through presets
```

### Level 4: Atmosphere & Investigation (Alt + Key)
```
Alt+A - Cycle Atmosphere Presets
Alt+I - Cycle Investigation Modes
```

### Level 5: Reverse Atmosphere (Ctrl+Alt + Key)  
```
Ctrl+Alt+A - Reverse Atmosphere Cycling
Ctrl+Alt+I - Reverse Investigation Mode Cycling
```

## Atmosphere Presets (Alt+A cycles through)
1. None
2. Crime Scene
3. Abandoned Building  
4. Nighttime Street
5. Laboratory
6. Interrogation Room
7. Warehouse
8. Office
9. Alley
10. Stormy Night
11. Misty Morning
12. Sunset

## Investigation Modes (Alt+I cycles through)
1. None
2. Evidence Analysis
3. Suspect Tracking
4. Memory Flashback
5. Revelation Moment

## Existing Keys (Preserved)
```
C → Shift+C - CRT Toggle (moved to avoid conflict)
F - Audio Fade (kept)
L - Letterbox Toggle (kept) 
I - Info Overlay (kept)
A - CRT Animation (kept)
1-4 - Scanline Size (kept)
[,] - Vignette Strength (kept)
-,= - Vignette Width (kept)
0 - Reset Vignette (kept)
```

## Visual Interface Components

### 1. Shader Menu (S key)
- Full graphical interface with buttons
- Shows current state of all effects
- Click to adjust individual settings
- Quick preset buttons

### 2. Quick Help (H key)
- Small overlay showing key mappings
- Always accessible
- Non-intrusive

### 3. Notifications
- Brief popup when effects change
- Shows: "Effect Name: Preset"
- Auto-disappears after 2 seconds

## Usage Examples

### Quick Access Patterns
```
# Enable film grain
Shift+G → cycles: off → subtle → moderate → heavy → back to off

# Set up noir atmosphere  
Alt+A → cycles through presets until "Alley" (noir style)

# Investigation mode
Alt+I → Evidence Analysis Mode

# Fine-tune individual effects
Shift+L → Enable lighting
Shift+V → Add vintage feel
Shift+G → Add film grain
```

### Power User Workflow
```
1. S - Open shader menu
2. Click preset buttons for base atmosphere
3. Use individual sliders for fine-tuning
4. Close menu and test
5. Use Shift+Key for quick adjustments
```

## Benefits of This System

### 🎯 Solves Hotkey Conflicts
- Uses modifier keys to multiply available combinations
- Existing keys preserved and functional
- Logical grouping prevents confusion

### 🔄 Flexible Control Levels
- **Casual**: Use S menu and click presets
- **Advanced**: Use cycling hotkeys for quick adjustments  
- **Power User**: Combine both approaches

### 🎮 Intuitive Design
- Related keys grouped (Shift+ for individual effects)
- Mnemonic mappings where possible (W=Weather, T=Torch)
- Visual feedback through notifications

### ⚡ Performance Friendly  
- Minimal UI overhead when not in use
- Efficient state management
- Smart preset combinations

## Implementation Notes

### Integration Points
1. **Room Exploration Screen**: Add `use shader_enhanced_controls`
2. **Room Background**: Use `room_background_and_objects_with_shaders`  
3. **Auto-Context**: Call `auto_apply_room_shaders()` on room entry

### Memory Management
- Shader states persist between rooms
- Reset functionality prevents accumulation
- Notification system prevents memory leaks

### Compatibility
- Works with existing CRT system
- Preserves bloom effects
- Maintains gamepad controls

## Future Expandability

The system easily supports:
- More shader effects (add to cycling lists)
- Custom user presets (extend atmosphere_presets)
- Save/load shader configurations
- Per-room shader profiles
- Dynamic context switching

This comprehensive solution transforms the limited hotkey problem into a powerful, flexible control system that enhances rather than hinders the detective game experience.
