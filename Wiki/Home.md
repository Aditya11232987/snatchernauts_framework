# Snatchernauts Framework Wiki

Welcome to the comprehensive documentation for **Snatchernauts Framework v0.3** - a powerful, modular point-and-click adventure game framework built on Ren'Py.

## 🎮 What is Snatchernauts Framework?

Snatchernauts Framework is a complete interactive point-and-click system featuring:

- **Advanced Visual Effects**: CRT monitor simulation, bloom lighting, letterbox presentation
- **Professional Interaction System**: Context-sensitive menus with smooth animations
- **Multi-Input Support**: Mouse, keyboard, and gamepad navigation
- **Live Development Tools**: Real-time object editor with visual feedback
- **Modular Architecture**: 18+ specialized files for maintainability and extensibility

## 🚀 Quick Start

1. **Installation**: Clone the repository and ensure Ren'Py is installed
2. **Launch**: Run `renpy.sh .` from the project directory
3. **Explore**: Press "Okay" on the info screen to enter Room1
4. **Interact**: Hover over objects and press A/Enter/Space to interact

## 📋 Table of Contents

### Core Documentation
- **[Architecture Overview](Architecture-Overview.md)** - System design and component relationships
- **[Input System](Input-System.md)** - Complete keyboard, mouse, and gamepad controls
- **[Object Interaction System](Object-Interaction-System.md)** - Context menus and action handling
- **[Visual Effects](Visual-Effects.md)** - CRT shaders, bloom effects, and animations

### Development Guides  
- **[Room Creation](Room-Creation.md)** - How to create and configure new rooms
- **[Object Configuration](Object-Configuration.md)** - Defining interactive objects and their properties
- **[Live Editor](Live-Editor.md)** - Using the built-in object positioning tools
- **[Configuration System](Configuration-System.md)** - Understanding the factory pattern and merge_configs

### Technical Reference
- **[File Structure](File-Structure.md)** - Complete breakdown of all 18+ framework files
- **[API Reference](API-Reference.md)** - Functions, variables, and configuration options  
- **[Performance Guide](Performance-Guide.md)** - Optimization techniques and best practices
- **[Shader System](Shader-System.md)** - CRT effects and bloom implementation details

### Advanced Topics
- **[Extending the Framework](Extending-Framework.md)** - Adding new features and systems
- **[Bloom Presets](Bloom-Presets.md)** - Complete reference of all 16 bloom effect presets
- **[Animation System](Animation-System.md)** - Floating effects and transform details
- **[Debug System](Debug-System.md)** - Development tools and debugging techniques

## 🎯 Key Features Overview

### Object Interaction System
- **4 Object Types**: Character, Item, Door, Container with unique action sets
- **Smart Positioning**: Menus appear intelligently relative to objects
- **Multi-Input**: Full mouse, keyboard, and gamepad support
- **Visual Feedback**: Floating animations with pulsing selection indicators

### Visual Effects Pipeline
- **CRT Monitor Simulation**: Authentic scanlines, chromatic aberration, screen curvature
- **Bloom Lighting System**: 16 presets from whisper-subtle to explosive-intense
- **Letterbox Presentation**: Cinematic widescreen with UI-aware positioning  
- **Smooth Animations**: Fade-in effects, floating bubbles, breathing objects

### Development Tools
- **Live Object Editor**: Real-time positioning and scaling with visual feedback
- **Debug Overlay**: Mouse coordinates, room info, bloom color verification
- **Performance Monitoring**: Efficient hover system with targeted redraws
- **Hot Reload**: Instant updates during development

### Input System
```
Keyboard Controls:
├── Navigation: Arrow Keys/WASD/D-pad  
├── Interaction: A/Enter/Space
├── Cancel: B/Escape
├── Debug: I (info), C (CRT), L (letterbox), F (fade audio), R (refresh)
└── CRT: 1-4 (scanline adjustment)

Gamepad Controls:
├── D-pad/Left Stick: Object navigation
├── A Button: Interact/Confirm
├── B Button: Cancel/Back  
└── Back/Select: Toggle gamepad mode

Mouse Controls:
├── Hover: Highlight objects and menu options
├── Click: Interact with objects
└── Smooth Performance: Optimized redraw system
```

## 🏗️ Architecture Highlights

### Modular Design (18+ Files)
```
Framework Structure:
├── Core Systems
│   ├── room_main.rpy (Main exploration screen)
│   ├── object_interactions.rpy (Interaction menus)  
│   └── room_config.rpy (Object definitions)
├── Visual Effects
│   ├── bloom_*.rpy (4 files - Bloom system)
│   ├── room_display.rpy (CRT shaders)
│   └── letterbox_gui.rpy (Cinematic presentation)
├── Input & UI
│   ├── room_ui.rpy (Hotspots and buttons)
│   ├── info_overlay.rpy (Documentation system)
│   └── room_editor.rpy (Development tools)
└── Utilities
    ├── room_functions.rpy (Room management)
    ├── common_utils.rpy (Shared utilities)
    └── config_builders.rpy (Configuration helpers)
```

### Performance Optimizations
- **Selective Redraws**: Targeted screen updates instead of full refreshes
- **Efficient Hover System**: Removed costly `renpy.restart_interaction()` calls
- **Modular Loading**: Component-based file structure for faster startup
- **Smart Caching**: Object configurations cached for rapid access

### Configuration System
```python
# Example object definition using factory pattern
"detective": merge_configs({
    # Basic properties
    "x": 211, "y": 124, "width": 328, "height": 499,
    "image": "images/detective.png",
    "description": "A mysterious detective figure.",
    "object_type": "character",
}, 
# Bloom configuration
create_bloom_config(BLOOM_PRESETS["neon_normal"]),
# Animation configuration  
create_animation_config({"hover_scale_boost": 1.02}))
```

## 🎨 Visual Examples

### Object Types & Actions
- **Character**: Talk, Ask About, Leave
- **Item**: Examine, Take, Use, Leave  
- **Door**: Open, Knock, Leave
- **Container**: Open, Search, Leave

### Bloom Presets (16 Available)
- **Whisper Series**: subtle, normal, intense (gentle glow)
- **Neon Series**: subtle, normal, intense (classic glow)
- **Explosive Series**: subtle, normal, intense (dramatic glow)  
- **Heartbeat Series**: subtle, normal, intense (pulsing glow)
- **Legacy**: subtle, moderate, intense, gentle (compatibility)

### CRT Effects
- **Scanline Density**: Adjustable via keys 1-4
- **Screen Curvature**: Authentic CRT warp simulation  
- **Chromatic Aberration**: Color separation effects
- **Resolution Independent**: Consistent appearance across window sizes

## 🛠️ Development Workflow

1. **Design Objects**: Use the live editor to position and scale objects visually
2. **Configure Properties**: Define interactions, descriptions, and effects in `room_config.rpy`
3. **Test Interactions**: Use debug keys to verify behavior and performance
4. **Optimize Effects**: Adjust bloom presets and CRT settings for desired aesthetic
5. **Save Changes**: Use the "Save to File" button to persist modifications

## 📈 Version History

- **v0.3** (Current): Complete interaction system, professional UI, performance optimizations
- **v0.2**: Core exploration, gamepad support, visual effects, live editor
- **v0.1**: CRT shaders, bloom system, letterbox presentation, basic interaction

## 🎯 Getting Started

Ready to dive in? Start with these essential guides:

1. **[Architecture Overview](Architecture-Overview.md)** - Understand the system design
2. **[Input System](Input-System.md)** - Master all control methods  
3. **[Object Configuration](Object-Configuration.md)** - Create your first interactive object
4. **[Live Editor](Live-Editor.md)** - Use the visual development tools

## 🤝 Contributing

The framework is designed for extensibility. See [Extending the Framework](Extending-Framework.md) for guidance on adding new features while maintaining the modular architecture.

---

*This documentation covers Snatchernauts Framework v0.3. For the latest updates, see [CHANGELOG.md](../CHANGELOG.md).*
