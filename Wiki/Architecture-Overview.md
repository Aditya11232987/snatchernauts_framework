# Architecture Overview

This document provides a comprehensive overview of the **Snatchernauts Framework v0.3** architecture, explaining how the 18+ modular components work together to create a complete point-and-click adventure game framework.

## 🏗️ System Architecture

### High-Level Design Principles

**Modular Architecture**: Each system is contained in separate files with clear responsibilities
**Factory Pattern**: Standardized object creation with `merge_configs()` and helper functions  
**Event-Driven Design**: Input events flow through specialized handlers to appropriate systems
**Performance First**: Optimized rendering pipeline with selective redraws and smart caching
**Extensibility**: Clean interfaces allow easy addition of new features without breaking existing code

### Core System Flow

```
Game Start → Info Overlay → Room Exploration → Object Interaction → Action Execution
    ↓              ↓              ↓                    ↓               ↓
script.rpy → info_overlay.rpy → room_main.rpy → object_interactions.rpy → [Action Handlers]
```

## 🎯 Component Architecture

### Layer 1: Core Systems (Foundation)
These files provide the essential framework functionality:

#### `room_main.rpy` - Central Orchestrator
- **Purpose**: Main exploration screen that coordinates all other systems
- **Key Functions**: Input handling, screen composition, system integration
- **Dependencies**: All other major systems
- **Performance**: Optimized input routing with context-aware controls

```python
# Core screen structure
screen room_exploration():
    use room_background_and_objects  # Visual layer
    use room_bloom_effects          # Lighting effects
    use object_hotspots            # Interactive elements
    use floating_description_box    # Hover descriptions
    use room_ui_buttons            # UI controls
    use debug_overlay              # Development tools
    use info_overlay               # Documentation system
```

#### `object_interactions.rpy` - Interaction Engine
- **Purpose**: Context-sensitive menus and action execution
- **Key Features**: Smart positioning, multi-input support, visual feedback
- **Performance**: Optimized hover with selective redraws
- **Extensibility**: Easy to add new object types and actions

```python
# Interaction system architecture
INTERACTION_ACTIONS = {
    "character": [Talk, Ask About, Leave],
    "item": [Examine, Take, Use, Leave], 
    "door": [Open, Knock, Leave],
    "container": [Open, Search, Leave]
}
```

#### `room_config.rpy` - Configuration Hub
- **Purpose**: Centralized object and room definitions
- **Pattern**: Factory pattern with `merge_configs()` for clean composition
- **Flexibility**: Easy object creation with preset combinations
- **Maintainability**: Clear separation of data from logic

```python
# Object factory pattern example
"detective": merge_configs(
    # Basic properties
    {"x": 211, "y": 124, "object_type": "character"},
    # Bloom configuration from preset
    create_bloom_config(BLOOM_PRESETS["neon_normal"]),
    # Animation settings
    create_animation_config({"hover_scale_boost": 1.02})
)
```

### Layer 2: Visual Effects (Presentation)
Specialized systems for graphics and visual feedback:

#### Bloom Lighting System (4 files)
- **`bloom_shader.rpy`**: Custom shader implementation with Ren'Py integration
- **`bloom_utils.rpy`**: Calculation utilities and parameter management  
- **`bloom_colors.rpy`**: Color extraction and 16 preset definitions
- **`bloom_utils.rpy`**: Factory functions and bloom effect management

**Architecture Flow:**
```
Object Hover → Color Extraction → Bloom Parameters → Shader Application → Visual Feedback
```

#### CRT & Display System
- **`room_display.rpy`**: CRT shader integration and rendering pipeline
- **`letterbox_gui.rpy`**: Cinematic presentation with UI-aware positioning
- **`room_transforms.rpy`**: Animation definitions and visual transforms

**Rendering Pipeline:**
```
Room Content → CRT Shader → Bloom Effects → Letterbox → Final Output
```

### Layer 3: Input & UI (Interaction)
Systems handling user input and interface elements:

#### `room_ui.rpy` - Interface Layer
- **Hotspot Generation**: Dynamic interactive areas for all objects
- **Button Management**: Exit and editor mode controls with letterbox awareness
- **Event Handling**: Mouse hover optimization with performance monitoring

#### `info_overlay.rpy` - Documentation System
- **Dual Mode**: Startup introduction and in-game reference
- **Version Display**: Dynamic framework version integration
- **Control Reference**: Complete input documentation for all methods

#### `room_editor.rpy` - Development Tools
- **Live Editing**: Real-time object positioning with visual feedback
- **Multi-Input Control**: Keyboard shortcuts for precise positioning
- **Persistence**: Save changes directly to configuration files

### Layer 4: Utilities & Support (Foundation)
Helper systems providing shared functionality:

#### Configuration & Factory Pattern
- **`config_builders.rpy`**: Helper functions for object creation
- **`object_factory.rpy`**: Factory pattern implementation
- **`common_utils.rpy`**: Shared utilities across all systems

#### Room & Function Management  
- **`room_functions.rpy`**: Room loading, management, and utilities
- **`room_debug.rpy`**: Debug overlay with performance metrics
- **`font_config.rpy`**: Typography and text rendering settings

## 🔄 Data Flow Architecture

### Object Interaction Flow
```
1. Mouse/Input Event → room_ui.rpy (hotspot detection)
2. Object Selection → object_interactions.rpy (menu creation)  
3. Menu Display → room_main.rpy (screen composition)
4. Action Selection → object_interactions.rpy (action execution)
5. Result Handling → [specific action handler] (game logic)
6. State Update → room_config.rpy (persistence if needed)
```

### Visual Effect Flow
```
1. Object Configuration → room_config.rpy (bloom/animation settings)
2. Hover Detection → room_ui.rpy (mouse/input handling)
3. Effect Calculation → bloom_utils.rpy (parameter calculation)
4. Color Extraction → bloom_colors.rpy (image analysis)
5. Shader Application → bloom_shader.rpy (GPU rendering)
6. Display Integration → room_display.rpy (CRT + letterbox)
```

### Performance Optimization Flow
```
1. Input Event → Selective Event Handling (avoid full refreshes)
2. State Change → Targeted Redraws (specific screen components)
3. Visual Update → Smart Caching (reuse calculated values)
4. Render Pipeline → Efficient Composition (minimize GPU calls)
```

## ⚡ Performance Architecture

### Optimization Strategies

**Selective Redraws**: 
- Replaced `renpy.restart_interaction()` with targeted screen updates
- Menu hover uses `renpy.restart_interaction()` only when necessary
- Object hover updates specific components rather than full screen

**Smart Caching**:
- Bloom color extraction cached per object to avoid repeated calculations
- Configuration objects cached during room loading
- Animation parameters calculated once during initialization

**Efficient Input Handling**:
- Context-aware input routing prevents unnecessary processing
- Mouse hover optimization with performance monitoring
- Gamepad navigation uses efficient state management

### Memory Management

**Modular Loading**:
- Components loaded on-demand to reduce initial memory footprint
- Room configurations cached intelligently during transitions
- Persistent data cleanup prevents memory leaks

**Resource Optimization**:
- Image scaling handled efficiently through Ren'Py pipeline
- Shader parameters optimized for GPU memory usage
- Object definitions use shared references where possible

## 🧩 Extensibility Architecture

### Adding New Object Types

1. **Define Actions**: Add to `INTERACTION_ACTIONS` in `object_interactions.rpy`
2. **Create Handlers**: Implement action functions (e.g., `handle_custom_action`)
3. **Test Integration**: Verify with existing input systems
4. **Document Usage**: Update configuration examples

### Adding New Visual Effects

1. **Create Shader**: Register new shader in `bloom_shader.rpy`
2. **Add Utilities**: Create calculation functions in appropriate utility file
3. **Integrate Display**: Connect to rendering pipeline in `room_display.rpy`
4. **Add Presets**: Create preset configurations for easy use

### Adding New Input Methods

1. **Define Bindings**: Add key/input mappings in `room_main.rpy`
2. **Create Handlers**: Implement handler functions in appropriate system
3. **Update Context**: Ensure context-aware behavior for different modes
4. **Test Integration**: Verify compatibility with existing input methods

## 🎛️ Configuration Architecture

### Factory Pattern Implementation

The framework uses a sophisticated factory pattern for clean object composition:

```python
# Base configuration template
DEFAULT_OBJECT_CONFIG = {
    "float_intensity": 0.5,
    "box_position": "auto"
}

# Preset-based configuration
"object_name": merge_configs(
    {"x": 100, "y": 200},                    # Basic properties
    DEFAULT_OBJECT_CONFIG,                   # Base template
    create_bloom_config(preset),             # Bloom effects
    create_animation_config(overrides)       # Animation settings
)
```

### Configuration Hierarchy

```
1. Default Templates (base settings for all objects)
2. Preset Configurations (bloom, animation presets)
3. Object-Specific Overrides (custom settings per object)
4. Runtime Modifications (editor changes, user preferences)
```

## 🔧 Development Architecture

### Debug System Integration

**Multi-Layer Debugging**:
- **Debug Overlay**: Real-time system information display
- **Performance Monitoring**: Interaction timing and redraw frequency
- **Configuration Validation**: Object definition verification
- **Visual Debugging**: Bloom color extraction verification

**Developer Tools**:
- **Live Editor**: Real-time object positioning with immediate feedback
- **Hot Reload**: Configuration changes without restart (where possible)
- **Debug Keys**: Instant access to system toggles and adjustments

### Error Handling Architecture

**Graceful Degradation**:
- Bloom effects fall back to simple display if shader fails
- Input systems continue working if one method fails
- Object interactions provide fallback actions for undefined types

**Error Recovery**:
- Configuration errors display helpful messages with corrections
- Missing assets handled with appropriate fallbacks
- Performance issues automatically switch to optimized modes

## 🎯 Integration Points

### Key System Interfaces

**Room Loading**: `load_room(room_id)` - Central function for room transitions
**Object Creation**: `create_room_object()` - Factory function for standardized objects
**Interaction Handling**: `show_interaction_menu()` - Entry point for object interactions
**Effect Application**: `apply_bloom_to_object()` - Centralized visual effect application

### Event System Integration

**Input Events**: Centralized routing through `room_main.rpy` with context awareness
**State Changes**: Automatic propagation to relevant systems (visual, audio, persistence)
**Performance Events**: Monitoring and optimization triggers throughout the pipeline

## 📊 System Dependencies

### Dependency Graph
```
room_main.rpy (Central Hub)
├── object_interactions.rpy (requires room_config.rpy)
├── room_display.rpy (requires bloom_*.rpy, letterbox_gui.rpy)
├── room_ui.rpy (requires common_utils.rpy)
├── info_overlay.rpy (standalone)
├── room_editor.rpy (requires room_functions.rpy)
└── Debug Systems (room_debug.rpy + common_utils.rpy)
```

### Minimal System Requirements
- **Core Functionality**: room_main.rpy, room_config.rpy, room_ui.rpy
- **Visual Effects**: bloom_*.rpy files, room_display.rpy  
- **Interaction System**: object_interactions.rpy
- **Development Tools**: room_editor.rpy, room_debug.rpy

---

This architecture enables the framework to be both powerful and maintainable, with clear separation of concerns and well-defined interfaces between systems. The modular design allows developers to understand and modify individual components without affecting the entire system.

*For implementation details of specific systems, see the individual component documentation pages.*
