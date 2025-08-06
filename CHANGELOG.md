# Changelog

All notable changes to the Snatchernauts Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-07

### Added
- **CRT Shader Effects** - Authentic retro CRT monitor simulation with customizable scanlines
- **Advanced Bloom System** - Enhanced matrix-based bloom effects with color tinting and brightness
- **CRT Integration with Bloom** - Bloom effects properly integrated within CRT shader rendering
- **Resolution-Independent Scanlines** - Consistent CRT scanline appearance across all window sizes
- **Dynamic CRT Controls** - Keyboard shortcuts for toggling CRT and adjusting scanline thickness
- **Improved Room Display System** - Unified background and object rendering on same layer
- **Fade-In Effects** - Smooth room entrance animations for backgrounds and objects
- **Enhanced Visual Pipeline** - Better integration between CRT shaders and bloom effects

### Changed
- **Room Rendering Architecture** - Combined background and objects into single layer for better CRT effects
- **Bloom Color System** - Added debug output for bloom color verification
- **CRT Shader Parameters** - Optimized default values for better visual quality
- **Transform System** - Improved conditional fade-in effects for room elements

### Technical Improvements
- **Shader Registration System** - Proper CRT shader initialization and management
- **Matrix Color Operations** - Enhanced bloom effects using TintMatrix and BrightnessMatrix
- **Frame-Based Rendering** - Better organization of visual effects within rendering pipeline
- **Conditional Rendering Logic** - Smart display decisions based on CRT enablement state

### Fixed
- **CRT-Bloom Integration** - Resolved issues with bloom effects not appearing correctly with CRT shaders
- **Scanline Consistency** - Fixed resolution-dependent scanline thickness variations
- **Transform Conflicts** - Eliminated conflicts between room fade-in and CRT effects
- **Layer Management** - Proper separation of CRT and non-CRT rendering paths

## [1.0.0] - 2025-01-07

### Added
- **Core Room Exploration System** - Point-and-click interface with hover descriptions
- **Full Gamepad Support** - D-pad and analog stick navigation with A button selection
- **Advanced Visual Effects System** - GPU-accelerated bloom effects with customizable parameters
- **Smart Description Box System** - Automatic positioning with collision detection
- **Live Editor Mode** - In-game object positioning and scaling tools with persistent saving
- **Pixel-Perfect Font Rendering** - Quaver font integration with 8-pixel aligned sizes
- **Modular Architecture** - Organized code structure with separated concerns
- **Bloom Color System** - Per-object customizable glow colors and effects
- **Animation System** - Hover animations with breathe, breath, and pulse effects
- **Persistent State Management** - Object positions saved across game sessions
- **Cross-Platform Input** - Seamless mouse and gamepad integration
- **Asset Management System** - Smart image loading and scaling
- **Configuration Builders** - Helper functions for creating object definitions
- **Room Management** - Dynamic room loading and switching capabilities

### Technical Features
- **Shader-Based Bloom Effects** - Real-time glow rendering
- **Object Factory Pattern** - Streamlined object creation workflow
- **Configuration Inheritance** - Hierarchical configuration merging
- **Debug Overlay System** - Development tools and information display
- **Memory-Efficient Rendering** - Optimized display pipeline
- **Event-Driven Architecture** - Clean separation of UI and logic
- **Utility Function Library** - Common operations and helpers

### Documentation
- Comprehensive README with usage examples
- MIT License for open source distribution
- Project structure documentation
- Asset creation guidelines
- Configuration reference
- Contributing guidelines

### Assets Included
- Quaver pixel font for retro aesthetics
- Example room background (1280x720)
- Sample interactive objects (detective, patreon logo)
- UI button graphics and styles

### Supported Platforms
- Windows (Ren'Py supported)
- macOS (Ren'Py supported)  
- Linux (Ren'Py supported)
- Android (Ren'Py supported, touch controls)

## [Unreleased]

### Planned Features
- Multiple room support with transitions
- Save/load system integration
- Audio system integration
- Mobile touch controls optimization
- Animation timeline system
- Particle effects system
- Dialogue system integration
- Inventory management system
- Quest/objective tracking
- Accessibility features (screen reader, colorblind support)

---

**Legend:**
- `Added` for new features
- `Changed` for changes in existing functionality  
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes
