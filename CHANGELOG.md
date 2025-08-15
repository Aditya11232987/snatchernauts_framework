# Changelog

## 0.5.3 — 2025-08-15

### Major Features
- **Development Tools Integration**: Complete development workflow enhancement
  - Unified game launcher script (`scripts/run-game.sh`) with debugging, linting, and compilation options
  - Comprehensive development documentation in `DEVELOPMENT_TOOLS.md`
  - Custom SDK path support via `RENPY_SDK` environment variable
  - Debug mode with console output retention for troubleshooting
- **Desaturation Effects System**: Advanced replacement for bloom highlighting
  - New `game/core/desaturation_utils.rpy` with comprehensive preset system
  - 24 different desaturation presets (subtle, explosive, whisper, heartbeat, flicker, ethereal variants)
  - Backward compatibility with existing bloom configurations
  - Performance optimizations and cleaner effect calculations
- **Debug System Overhaul**: Centralized debugging infrastructure
  - New `game/debug/bloom_debug.rpy` with categorized debug output
  - Shader debug configuration system (`game/shader_debug_config.rpy`)
  - Toggle-based debug controls for different system components
  - Verbose positioning and property debugging for object interactions

### Technical Improvements
- **Shader System Refinements**: Enhanced Neo-Noir shader integration
  - Updated `letterbox_shader_v2.rpy`, `neo_noir_color_grading.rpy`, `neo_noir_lighting.rpy`
  - Improved shader layer management in `neo_noir_shader_layers.rpy`
  - Better hotkey mapping and setup documentation
- **Room System Enhancement**: Improved object interaction and configuration
  - Enhanced room logic handlers for all three example rooms
  - Better object property debugging and display calculations
  - Improved gamepad navigation integration
- **API Improvements**: Cleaner interaction and display APIs
  - Updated `interactions_api.rpy`, `room_api.rpy`, and `ui_api.rpy`
  - Better error handling and parameter validation
  - Enhanced logging integration across all API modules

### New Documentation
- **Development Workflow Guide**: Complete `DEVELOPMENT_TOOLS.md` documentation
- **Shader Setup Updates**: Enhanced shader documentation and troubleshooting
- **Room Structure Guide**: Updated `ROOM_STRUCTURE_GUIDE.md` with latest patterns
- **Wiki Improvements**: Enhanced technical documentation across all wiki pages

### Developer Experience
- **Streamlined Launch Process**: Single script handles all common development tasks
- **Better Error Messages**: Clear validation and troubleshooting guidance
- **Debug Output Control**: Fine-grained control over debug verbosity levels
- **SDK Flexibility**: Easy switching between different Ren'Py SDK versions

### Removed/Deprecated
- Consolidated shader files: removed redundant/experimental shader implementations
- Cleaned up bloom system files in favor of desaturation approach
- Removed deprecated screen files (`screens_bloom.rpy`)

### Fixed
- Room interaction timing and state management
- Shader effect stacking and performance issues
- Debug output formatting and categorization
- Development workflow reliability across different environments

## 0.5.2 — 2025-08-13

### Major Features
- **Shader-Based Letterbox System**: Complete rewrite from GUI bars to GLSL shader rendering
  - Proper Ren'Py shader registration using variables string and 300-stage pipeline
  - Smooth fade in/out animations via shader uniforms (height + alpha)
  - Letterbox disabled during normal gameplay, smoothly activates for detective conversations
  - Backward compatibility maintained for existing `show_letterbox()`/`hide_letterbox()` calls
- **Comprehensive Shader Infrastructure**: 15+ atmospheric shaders for detective ambiance
  - Film grain, fog, lighting, vintage/sepia, rain, depth-of-field, edge detection
  - Mystery reveal, flashlight, color grading with detective-specific presets
  - Hotkey system: `Shift+G/F/V/L/W` for individual effects, `Alt+A/I` for presets
  - `R` to reset all shaders, `H` for help overlay
- **Detective Interaction System**: Enhanced conversation system with proper UI clearing
  - Fixed ui.interact stack error by simplifying dialogue approach
  - Room-specific logic with dynamic interaction options
  - Character definitions and conversation state tracking

### Technical Improvements
- **Room System Restructuring**: Organized assets under modular `game/rooms/` structure
  - Room-specific sprites moved to proper directories (`game/rooms/roomN/sprites/`)
  - Enhanced configuration system with `scripts/` subdirectories
  - 3 rooms with complete logic and asset separation
- **UI Stack Management**: Comprehensive layer clearing before dialogue scenes
  - Clear transient and screens layers to prevent conflicts
  - Proper interaction menu and object state cleanup
- **Shader Integration**: All shaders work seamlessly with existing CRT and bloom systems
  - Proper mesh True transforms for coordinate computation
  - Developer controls for testing different parameters

### Assets & Documentation
- **New High-Resolution Backgrounds**: itch.io marketing assets (1920x1080, 2560x1440)
- **Detective Assets**: Character sprites, interaction graphics, room backgrounds
- **Comprehensive Shader Documentation**: `SETUP_GUIDE.md` and `HOTKEY_MAPPING.md`
- **Updated README**: Version 0.5.2 with shader system features and enhanced controls

### Fixed
- Detective dialogue no longer causes ui.interact stack errors
- Letterbox effects now use proper shader rendering instead of GUI overlays
- Room exploration returns cleanly to interaction mode after conversations
- All shader effects properly clear and don't interfere with each other

## 0.5.1 — 2025-08-13

### Changed
- Logging: guard ORIG_PRINT resolution on reload using fallback `_get_orig_print` to avoid `NameError`.
- Interactions: `on_object_interact` now returns `bool`; default handlers short-circuit when handled.
- UI: add confirmations for Exit/Main Menu; disable accidental game_menu during exploration.
- Room1: custom examines and patreon take handling; return `True` when handled.
- Minor: tooltip tweaks and logging cosmetics.

### Chore
- Save local edits; add `game/core/common_init.rpy`.

## 0.5 — 2025-08-13

### Added
- Centralized game logic hooks in `game/logic/game_logic.rpy` with per-room registry.
- Example room handler in `game/logic/rooms/room1_logic.rpy`.
- Hook wiring: `on_room_enter`, `on_object_hover`, `on_object_interact`.
- Color-coded, truncating logging with print interception and runtime toggles.
- Developer docs: `Wiki/DeveloperManual.md` and `Wiki/Modules.md`.
- Standardized module headers (Overview/Contracts/Integration) across major files.

### Changed
- `script.rpy`: calls `on_game_start()` after info overlay; calls `on_room_enter(room)` after `load_room`.
- `ui_api.handle_object_hover`: emits hook into logic.
- `interactions_api.execute_object_action`: emits hook before built-in effects.

### Removed
- `game/script.rpy.bak` backup file.

### Notes
- Legacy files moved to `game/legacy/` and marked as legacy.
