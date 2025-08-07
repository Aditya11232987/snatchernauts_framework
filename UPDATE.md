# Snatchernauts Framework Update Guide

This comprehensive guide covers installation, configuration, and updating procedures for **Snatchernauts Framework v0.3** - a complete point-and-click adventure game framework.

## Current Version: 0.3.1

### 🎯 What's New in v0.3.1

#### Major Features Added
- **Complete Object Interaction System** with context-sensitive menus
- **Professional Info Overlay** with startup introduction and controls documentation
- **Enhanced Performance** with optimized hover system and selective redraws
- **Smart Menu Positioning** that adapts to object locations and screen boundaries
- **Advanced Animation System** with floating bubbles and pulsing selection indicators
- **Audio Integration** with smooth room transition effects
- **Professional Branding** updated throughout the framework

#### Technical Improvements
- **18+ Modular Files** for specialized functionality and maintainability
- **Factory Pattern Configuration** with merge_configs system for object creation
- **Performance Optimizations** removing costly interaction restarts from hover events
- **Debug System Integration** with comprehensive developer tools
- **Input System Overhaul** supporting mouse, keyboard, and gamepad seamlessly

## 📦 Installation Instructions

### Prerequisites
- **Ren'Py SDK** 8.0+ (latest version recommended)
- **Python 3.9+** (included with Ren'Py)
- **Git** (for version control and updates)
- **4GB RAM minimum** (for CRT shaders and bloom effects)

### Quick Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd snatchernauts_framework
   ```

2. **Launch the Framework**
   
   **Command Line Method:**
   ```bash
   # Linux/Mac
   ~/.local/bin/renpy/renpy.sh .
   
   # Windows  
   renpy.exe .
   ```
   
   **Ren'Py Launcher Method:**
   - Open Ren'Py Launcher
   - Set "Projects Directory" to parent folder
   - Select "snatchernauts_framework" from project list
   - Click "Launch Project"

3. **Verify Installation**
   - Framework starts with professional info overlay showing version 0.3
   - Click "Okay - Continue to Room1" to enter exploration mode
   - Test object interactions by hovering over detective or patreon objects
   - Press 'I' to toggle info overlay on/off during gameplay

## 🎮 Core Systems Overview

### Object Interaction System
The framework features a sophisticated interaction system:

```
Object Types & Available Actions:
├── Character: Talk, Ask About, Leave
├── Item: Examine, Take, Use, Leave
├── Door: Open, Knock, Leave
└── Container: Open, Search, Leave
```

**Menu Positioning Algorithm:**
- Automatically positions menus 10px left of object's right edge
- Places menus at upper-middle height (1/3 down from object top)
- Includes screen boundary detection to prevent off-screen menus
- Supports manual positioning overrides in object configuration

### Input System Architecture

**Keyboard Controls:**
```
Exploration Mode:
├── Arrow Keys/WASD: Navigate between objects
├── A/Enter/Space: Interact with selected object  
├── B/Escape: Cancel current action
└── Debug Keys: I, C, L, F, R, 1-4

Interaction Menu Mode:
├── Up/Down Arrows: Navigate menu options
├── Enter: Execute selected action
└── Escape: Close menu and return to exploration
```

**Gamepad Support:**
```
D-pad/Left Stick: Object navigation
A Button: Interact/Confirm actions
B Button: Cancel/Go back
Back/Select: Toggle gamepad navigation mode
```

**Mouse Integration:**
```
Hover: Highlight objects and menu options
Click: Direct interaction with objects
Optimized Performance: Selective redraws on hover
```

### Visual Effects Pipeline

**CRT Monitor Simulation:**
- **Scanline Rendering**: Resolution-independent with adjustable density
- **Screen Curvature**: Authentic CRT warp simulation  
- **Chromatic Aberration**: Color separation effects
- **Dynamic Controls**: Keys 1-4 adjust scanline thickness in real-time

**Bloom Lighting System (16 Presets):**
```
Bloom Preset Categories:
├── Whisper (subtle, normal, intense): Gentle, barely-there glow
├── Neon (subtle, normal, intense): Classic cyberpunk glow
├── Explosive (subtle, normal, intense): Dramatic, high-impact glow
├── Heartbeat (subtle, normal, intense): Pulsing, rhythmic glow
└── Legacy (subtle, moderate, intense, gentle): Compatibility presets
```

## 🛠️ Configuration System

### Object Definition Structure

The framework uses a sophisticated factory pattern for object creation:

```python
# Example: Creating a character object
"detective": merge_configs({
    # Basic Properties
    "x": 211, "y": 124,           # Position coordinates
    "width": 328, "height": 499,  # Dimensions  
    "image": "images/detective.png", # Image path
    "description": "A mysterious detective figure.",
    "object_type": "character",    # Determines available actions
    "box_position": "right",       # Description box placement
    "float_intensity": 0.5,        # Animation intensity
},
# Bloom Configuration (using preset)
create_bloom_config(BLOOM_PRESETS["neon_normal"]),
# Animation Configuration
create_animation_config({
    "hover_scale_boost": 1.02,     # Slight size increase on hover
    "hover_brightness_boost": 0.2  # Brightness increase on hover
}))
```

### Room Creation Workflow

1. **Design Phase**
   - Create background image (1280x720 recommended)
   - Plan object placement and interaction types
   - Choose appropriate bloom presets for aesthetic

2. **Configuration Phase**
   ```python
   # Add to ROOM_DEFINITIONS in room_config.rpy
   "room2": {
       "background": "images/room2.png",
       "objects": {
           "new_object": create_room_object(
               x=400, y=300,
               image="images/new_object.png",
               description="An interesting object to interact with.",
               object_type="item",
               bloom_preset="neon_subtle"
           )
       }
   }
   ```

3. **Testing Phase**
   - Use live editor (press 'E') for visual positioning
   - Test interactions with all input methods
   - Verify bloom effects and animations
   - Save changes permanently

## 🔧 Development Tools

### Live Object Editor

**Access**: Press 'E' in room exploration mode

**Controls:**
```
Movement:
├── Arrow Keys: Move by configured speed (default 5px)
├── WASD: Pixel-precise movement (1px)
├── Shift+Arrows: Fast movement (10px)
└── +/- Keys: Adjust movement speed

Scaling:
├── Q/E: Scale ±5%
├── Z/X: Precise scaling ±1%
└── R: Reset to 100% scale

Selection:
├── 1-9 Keys: Select object by number
├── Mouse Click: Select object visually
└── Object List: Click buttons to select

Operations:
├── 💾 Save to File: Persist changes to room_config.rpy
├── 🔄 Reset Room: Restore original positions
├── 🧹 Clear Persistent: Remove saved overrides
└── H: Toggle help display
```

### Debug System

**Debug Overlay** (always available in developer mode):
- **Mouse Coordinates**: Real-time cursor position
- **Room Information**: Current room, background, object count
- **Bloom Verification**: Color extraction results for hovered objects
- **Performance Metrics**: Interaction timing and redraw efficiency

**Debug Controls:**
```
I: Toggle info overlay (startup screen)
C: Toggle CRT effects on/off
L: Toggle letterbox presentation  
F: Fade out room audio
R: Refresh/restart interaction system
1-4: Adjust CRT scanline density
```

## 📁 File Structure Deep Dive

### Core Systems (4 files)
```
room_main.rpy           # Main exploration screen and input handling
object_interactions.rpy # Context menu system and action execution
room_config.rpy        # Object definitions and room configurations
script.rpy             # Startup flow and main entry point
```

### Visual Effects (6 files)
```
bloom_shader.rpy       # Custom shader implementation
bloom_utils.rpy        # Bloom calculation utilities  
bloom_colors.rpy       # Color extraction and presets
room_display.rpy       # CRT effects and rendering pipeline
letterbox_gui.rpy      # Cinematic presentation system
room_transforms.rpy    # Animation definitions
```

### UI & Input (4 files)
```
room_ui.rpy           # Hotspots, buttons, and UI controls
info_overlay.rpy      # Documentation and help system
room_editor.rpy       # Live development tools
room_descriptions.rpy # Floating description system
```

### Utilities & Configuration (6+ files)
```
room_functions.rpy    # Room management and utilities
common_utils.rpy      # Shared utility functions
config_builders.rpy   # Object creation helpers
object_factory.rpy    # Factory pattern implementation
font_config.rpy       # Typography settings
room_debug.rpy        # Debug overlay system
```

## 🎯 Performance Guide

### Optimization Strategies

**Hover System Optimization:**
- Replaced costly `renpy.restart_interaction()` with targeted redraws
- Implemented selective screen updates for menu interactions
- Reduced full-screen refreshes by 90% during mouse navigation

**Bloom Effect Optimization:**
- Color extraction cached per object to avoid repeated calculations
- Bloom parameters calculated once during object initialization
- Smart bloom rendering only when objects are hovered

**Memory Management:**
- Modular file loading reduces initial memory footprint
- Object configurations loaded on-demand for room transitions
- Persistent data cleanup prevents memory leaks during extended play

### Performance Monitoring

**Built-in Metrics:**
- Hover event timing displayed in debug overlay
- Screen redraw frequency monitoring
- Memory usage tracking for object configurations
- Bloom effect rendering performance analysis

**Troubleshooting Performance Issues:**

1. **Slow Mouse Hover Response:**
   ```python
   # Check if old restart_interaction calls remain
   # Should use: Function(renpy.restart_interaction)
   # Not: Multiple restart calls in hover events
   ```

2. **Bloom Effect Lag:**
   ```python
   # Reduce bloom intensity or disable for testing
   "bloom_enabled": False,  # Temporarily disable
   "bloom_intensity": 0.3,  # Reduce from higher values
   ```

3. **Memory Usage Growth:**
   ```python
   # Clear persistent overrides periodically
   persistent.room_overrides = {}
   # Restart game session after extensive editor use
   ```

## 🔄 Update Process

### Updating from v0.2.x to v0.3.1

**Major Changes to Account For:**

1. **Configuration System Changes:**
   ```python
   # Old v0.2.x format
   "object": {
       "x": 100, "y": 200,
       "bloom_color": "#ff0000"
   }
   
   # New v0.3.1 format with factory pattern
   "object": merge_configs({
       "x": 100, "y": 200,
   }, create_bloom_config(BLOOM_PRESETS["neon_normal"]))
   ```

2. **Interaction System Integration:**
   - Add `object_type` field to all objects
   - Update object definitions to support new interaction menus
   - Test all objects work with new context-sensitive actions

3. **Input Handling Updates:**
   - New mouse hover optimization may require testing
   - Gamepad navigation enhanced with context awareness
   - Debug key bindings expanded (check for conflicts)

**Update Steps:**

1. **Backup Current Configuration**
   ```bash
   cp game/room_config.rpy game/room_config.rpy.v02.backup
   cp game/script.rpy game/script.rpy.v02.backup
   ```

2. **Pull Latest Changes**
   ```bash
   git stash  # Save any uncommitted changes
   git pull origin main
   git stash pop  # Restore changes if needed
   ```

3. **Migrate Configuration**
   - Compare backed-up configs with new format
   - Update object definitions to use factory pattern
   - Add `object_type` fields to all interactive objects
   - Test each object with new interaction system

4. **Verify Functionality**
   - Launch framework and test startup info overlay
   - Verify all objects respond to interactions
   - Test mouse, keyboard, and gamepad navigation
   - Check performance improvements in hover system
   - Validate debug keys and developer tools

### Version Migration Checklist

- [ ] All objects have `object_type` specified
- [ ] Bloom configurations migrated to preset system
- [ ] Custom objects work with new interaction menus
- [ ] Performance improved with new hover system
- [ ] Debug tools accessible and functional
- [ ] Audio integration working during room transitions
- [ ] Info overlay displays correctly with version info

## 🚨 Troubleshooting

### Common Issues & Solutions

**Issue: Objects not responding to interactions**
```python
# Solution: Verify object configuration
1. Check object_type is set ("character", "item", "door", "container")
2. Ensure image path is correct and accessible
3. Verify width/height dimensions are positive integers
4. Test with live editor to confirm positioning
```

**Issue: Interaction menus appear off-screen**
```python
# Solution: Adjust menu positioning
1. Check object positioning relative to screen boundaries
2. Verify INTERACTION_BUTTON_CONFIG width/height settings
3. Use manual box_position setting if needed
4. Test with different object sizes and positions
```

**Issue: Mouse hover feels laggy or unresponsive**
```python
# Solution: Verify optimization implementation
1. Check for remaining renpy.restart_interaction() in hover events
2. Ensure using optimized redraw system
3. Monitor debug overlay for performance metrics
4. Test with bloom effects temporarily disabled
```

**Issue: Gamepad navigation not working**
```python
# Solution: Check gamepad configuration
1. Press Back/Select to toggle gamepad navigation mode
2. Verify controller recognized by system
3. Check Ren'Py gamepad preferences
4. Test with different controller types
```

**Issue: CRT effects not displaying**
```python
# Solution: Verify shader support
1. Check graphics card shader support
2. Test with different CRT parameter values
3. Press 'C' to toggle CRT effects on/off
4. Verify crt_enabled variable state
```

**Issue: Live editor not saving changes**
```python
# Solution: Check file permissions and paths
1. Verify write access to game directory
2. Use "Save to File" button explicitly
3. Check room_config.rpy file permissions
4. Test with administrator privileges if needed
```

### Getting Additional Help

**Debug Resources:**
- Enable developer mode in Ren'Py for detailed error messages
- Check debug overlay for real-time system information
- Review console output for warnings or errors
- Use live editor to test object positioning interactively

**Documentation:**
- Comprehensive Wiki/ directory with detailed guides
- Inline code comments explain complex functionality
- CHANGELOG.md documents all version changes
- Example configurations demonstrate best practices

**Community Support:**
- GitHub issues for bug reports and feature requests
- Code examples provided for common use cases
- Modular architecture allows easy customization
- Active development with regular updates

---

## 🎯 Next Steps After Installation

1. **Explore the Framework**: Launch and try all input methods
2. **Test Interactions**: Click or press 'A' on objects to see context menus
3. **Try the Editor**: Press 'E' to position objects visually
4. **Review Configuration**: Examine `room_config.rpy` structure
5. **Create Custom Objects**: Add your own interactive elements
6. **Experiment with Effects**: Try different bloom presets and CRT settings
7. **Build New Rooms**: Expand beyond Room1 with additional locations

*For comprehensive technical documentation, visit the Wiki/ directory or see individual file headers for detailed API documentation.*
