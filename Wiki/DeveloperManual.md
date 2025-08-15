# Snatchernauts Framework — Developer Manual

## Overview

This comprehensive developer manual provides detailed guidance for working with the Snatchernauts Framework. It covers the complete development lifecycle, from initial setup through deployment, and serves as both a reference guide and tutorial for building point-and-click adventure games with the framework.

## Table of Contents

1. [Framework Architecture](#framework-architecture)
2. [Development Environment Setup](#development-environment-setup)
3. [Directory Structure and Organization](#directory-structure-and-organization)
4. [Game Lifecycle and Flow](#game-lifecycle-and-flow)
5. [Game Logic System](#game-logic-system)
6. [API Reference and Contracts](#api-reference-and-contracts)
7. [UI System and Screen Management](#ui-system-and-screen-management)
8. [Visual Effects and Shaders](#visual-effects-and-shaders)
9. [Asset Management](#asset-management)
10. [Testing and Quality Assurance](#testing-and-quality-assurance)
11. [Debugging and Development Tools](#debugging-and-development-tools)
12. [Performance Optimization](#performance-optimization)
13. [Best Practices and Conventions](#best-practices-and-conventions)
14. [Deployment and Distribution](#deployment-and-distribution)
15. [Troubleshooting Guide](#troubleshooting-guide)

## Framework Architecture

### Design Philosophy

The Snatchernauts Framework follows several key design principles:

**Modular Architecture**: The framework is built with clearly separated concerns, allowing developers to modify or extend specific functionality without affecting other systems.

**Hook-Based Logic**: Game logic is implemented through a system of hooks that allow for both global and room-specific behavior while maintaining clean separation between UI and logic.

**API-Driven Development**: All framework functionality is exposed through well-defined APIs that provide clear contracts and consistent behavior.

**Developer Experience Focus**: The framework prioritizes ease of use, comprehensive documentation, and robust debugging tools to enhance the development experience.

### Core Systems Overview

**Room Management System**: Handles room loading, object management, and navigation between different game areas.

**Interaction System**: Manages player input, object interactions, and action menus across multiple input methods (mouse, keyboard, gamepad).

**Display System**: Controls visual presentation, background rendering, object visibility, and visual effects coordination.

**UI Framework**: Provides screen composition, overlay management, and user interface components.

**Effect System**: Implements visual effects including CRT shaders, bloom effects, and letterboxing.

**Logic Hook System**: Enables custom game behavior through a structured hook system that supports both global and room-specific logic.

## Development Environment Setup

### Prerequisites

**Required Software**:
- Ren'Py SDK 8.1.0 or later
- Python 3.9+ (included with Ren'Py SDK)
- Git for version control
- Text editor with Python/Ren'Py syntax support (VS Code recommended)

**Recommended Extensions** (VS Code):
- Ren'Py Language Support
- Python extension
- GitLens for Git integration
- Material Icon Theme for file recognition

### Initial Setup Process

**1. Clone the Framework**:
```bash
git clone https://gitlab.com/yourusername/snatchernauts-framework.git
cd snatchernauts-framework
```

**2. Environment Configuration**:
```bash
# Set up Ren'Py SDK path
export RENPY_SDK="/path/to/renpy-sdk"

# Add to shell profile for persistence
echo 'export RENPY_SDK="/path/to/renpy-sdk"' >> ~/.bashrc

# Verify setup
$RENPY_SDK/renpy.sh --version
```

**3. Project Initialization**:
```bash
# Test the framework
$RENPY_SDK/renpy.sh .

# Run linting to verify setup
$RENPY_SDK/renpy.sh . lint
```

### Development Workflow

**Daily Development Routine**:
1. Pull latest changes: `git pull origin main`
2. Run linting: `$RENPY_SDK/renpy.sh . lint`
3. Test game functionality: `$RENPY_SDK/renpy.sh .`
4. Make changes to game logic/assets
5. Test changes thoroughly
6. Commit changes: `git commit -am "Description of changes"`
7. Push changes: `git push origin feature-branch`

## Directory Structure and Organization

### Complete Directory Structure

The framework follows a structured organization that separates concerns and promotes maintainability:

```
snatchernauts-framework/
├── game/                          # Main game directory
│   ├── script.rpy                # Main entry point and game flow
│   ├── api/                       # Framework APIs
│   │   ├── room_api.rpy          # Room management functions
│   │   ├── display_api.rpy       # Display and visual functions
│   │   ├── interactions_api.rpy  # Player interaction handling
│   │   └── ui_api.rpy            # UI and screen management
│   ├── core/                      # Core framework functionality
│   │   ├── options.rpy           # Game configuration and settings
│   │   ├── common_utils.rpy      # Shared utility functions
│   │   ├── common_logging.rpy    # Logging and debug functions
│   │   ├── room_utils.rpy        # Room-specific utilities
│   │   └── rooms/                # Room configuration system
│   │       └── room_config.rpy   # Room definitions and editor
│   ├── logic/                     # Game logic implementation
│   │   └── game_logic.rpy        # Global game logic hooks
│   ├── rooms/                     # Room definitions and assets
│   │   ├── room1/                # Example room with assets and scripts
│   │   ├── room2/                # Additional example rooms
│   │   └── room3/                # Room-specific configurations
│   ├── ui/                        # User interface screens
│   │   ├── screens_room.rpy      # Room exploration screens
│   │   ├── screens_interactions.rpy # Interaction menu screens
│   │   └── room_descriptions.rpy # Description box management
│   ├── overlays/                  # Screen overlays
│   │   ├── info_overlay.rpy      # Information and help overlay
│   │   ├── debug_overlay.rpy     # Development debug overlay
│   │   ├── letterbox_gui.rpy     # Letterbox effect overlay
│   │   └── fade_overlay.rpy      # Screen transition overlays
│   ├── shaders/                   # Visual effect shaders
│   │   ├── crt_shader.rpy        # CRT monitor effect
│   │   ├── letterbox_shader_v2.rpy # Enhanced letterbox shader
│   │   └── neo_noir_*.rpy        # Neo-noir atmosphere effects
│   ├── images/                    # Game images and sprites
│   │   ├── backgrounds/          # Room background images
│   │   ├── objects/              # Interactive object sprites
│   │   └── ui/                   # UI element graphics
│   ├── audio/                     # Game audio files
│   │   ├── music/                # Background music tracks
│   │   └── sounds/               # Sound effects
│   ├── fonts/                     # Custom font files
│   └── gui/                       # Ren'Py GUI system files
├── scripts/                       # Development and automation tools
│   ├── run-game.sh               # 🎮 Unified game launcher with options
│   ├── lint.sh                   # 🔍 Ren'Py code linting
│   ├── push-both.sh              # 🚀 Push to GitLab + GitHub simultaneously
│   ├── sync-github-wiki.sh       # 📚 Manual wiki synchronization to GitHub
│   ├── github-init.sh            # 🔗 Initialize GitHub remote repository
│   └── hooks/                    # Git hooks for automation
│       └── pre-push             # ⚠️ Auto-sync wiki on push (if enabled)
├── Wiki/                          # Documentation (auto-synced to wikis)
│   ├── 01-Overview.md            # Framework introduction and concepts
│   ├── 02-Getting-Started.md     # Zero-to-hero tutorial
│   ├── 03-Architecture.md        # System design and best practices
│   ├── 04-Logic-Hooks.md         # Game logic system documentation
│   ├── 05-API-*.md               # Complete API reference library
│   ├── 06-Screens-and-UI.md     # UI system documentation
│   ├── 07-Effects-and-Shaders.md # Visual effects manual
│   ├── 08-Build-and-Distribute.md # Production deployment guide
│   ├── 09-Examples.md            # Extensive code examples
│   ├── 10-Troubleshooting.md     # Problem-solving guide
│   └── DeveloperManual.md        # This document
├── .gitlab-ci.yml                # GitLab CI/CD configuration (auto-wiki sync)
├── CHANGELOG.md                  # Version history and release notes
├── README.md                     # Comprehensive framework guide
├── LICENSE                       # MIT license
└── project.json                  # Ren'Py project configuration
```

### File Organization Principles

**API Layer (`game/api/`)**: Contains all public-facing functions that game developers should use. These files define the contract between the framework and game-specific code.

**Core Layer (`game/core/`)**: Internal framework functionality that supports the APIs. Game developers typically shouldn't need to modify these files directly.

**Logic Layer (`game/logic/`)**: Where game-specific behavior is implemented using the framework's hook system.

**Presentation Layer (`game/ui/`, `game/overlays/`)**: Handles all visual presentation and user interface concerns.

**Assets (`game/images/`, `game/audio/`)**: Organized by type and usage context for easy management.

### Directory Layout

- `game/script.rpy`: Entry points (`label start`, `label play_room`). Calls `load_room(room)` then `on_room_enter(room)`.
- `game/logic/`
  - `game_logic.rpy`: Global hooks and room handler registry.
  - `rooms/room1_logic.rpy`: Example per-room handler registration and hooks.
- `game/api/`
  - `room_api.rpy`: Room lifecycle (toggle CRT, parameter setters, navigate, etc.).
  - `display_api.rpy`: Background and object visibility helpers.
  - `ui_api.rpy`: Hotspots, hover/unhover, editor/exit button customization.
  - `interactions_api.rpy`: Interaction menu, actions, execution.
- `game/core/`
  - `common_utils.rpy`: Shared helpers (fonts, dev mode checks, mouse position).
  - `common_logging.rpy`: Color-coded, truncating logs; function wrapping; print interception.
  - `config_builders.rpy`, `object_factory.rpy`: Build room/object configs.
  - `bloom_utils.rpy`, `bloom_colors.rpy`: Bloom logic and presets.
  - `room_utils.rpy`: Misc room-related utilities.
  - `rooms/`: `room_config.rpy` & editor.
  - `options.rpy`: Project options and defaults (log toggles).
- `game/ui/`
  - `screens_room.rpy`: Room background + object composition and bloom.
  - `screens_interactions.rpy`: Interaction UI and bindings.
  - `screens_bloom.rpy`: Bloom overlays.
  - `room_descriptions.rpy`: Floating description boxes.
  - `room_ui.rpy`, `room_transforms.rpy`, `screens.rpy`: Additional screens and transforms.
- `game/overlays/`
  - `letterbox_gui.rpy`, `info_overlay.rpy`, `debug_overlay.rpy`, `fade_overlay.rpy`.
- `game/shaders/`
  - `crt_shader.rpy`, `bloom_shader.rpy`.

## Lifecycle

1. `label start` → info overlay flow → `call play_room`.
2. `label play_room(room, music)`:
   - `load_room(room)` → populates `store.room_objects`.
   - Calls `on_room_enter(room)` (global hook + per-room handler) for logic.
   - `call screen room_exploration` for the interactive loop.
3. Hovering objects → `ui_api.handle_object_hover(obj)`:
   - Sets `store.current_hover_object`.
   - Calls `on_object_hover(room_id, obj)` hook.
4. Opening/using interactions → `interactions_api.execute_object_action(obj, action)`:
   - Calls `on_object_interact(room_id, obj, action)` hook before built-in side effects.

## Game Logic Hooks

- `on_game_start()`: One-time init after overlays (optional, call from script if used).
- `on_room_enter(room_id)`: Called after `load_room`; initialize per-room state.
- `on_object_hover(room_id, obj_name)`: Lightweight reactions to hover changes.
- `on_object_interact(room_id, obj_name, action_id)`: Central place to branch gameplay.

Room-specific logic
- Create `game/logic/rooms/<room_id>_logic.rpy` with a handler class and register via `register_room_logic('<room_id>', Handler())`.
- Only implement the hooks you need; the global hooks still run.

## Public API Contracts

- room_api:
  - `toggle_crt_effect()`, `set_crt_parameters(warp, scan, chroma, scanline_size)`
  - `move_object(name, dx, dy)`, `scale_object(name, scale_change)`
  - `get_object_list_for_navigation()`, `gamepad_navigate(dir)`
- display_api:
  - `get_room_background()`, `get_fallback_background()`
  - `should_display_object(obj)`, `is_object_hidden(obj)`
- ui_api:
  - `handle_object_hover(name)`, `handle_object_unhover()`
- interactions_api:
  - `show_interaction_menu(name)`, `execute_object_action(name, action_id)`

All APIs return simple values or update `store` and will log ENTER/EXIT with truncated arguments by default.

## UI & Interactions

- Screen `room_exploration` composes background, objects, bloom, hotspots, overlays, and input handlers.
- Interaction flow:
  - `show_interaction_menu(obj)` sets menu state and selection.
  - Input navigates via `navigate_interaction_menu` and executes via `execute_selected_action()` → `execute_object_action(obj, action_id)`.
  - Before executing the built-in action, the logic hook `on_object_interact(room, obj, action_id)` is called for custom behavior.

## Effects

- CRT: `crt_shader.rpy` with scanlines, chromatic aberration, and horizontal vignette; toggles/params in `room_api`.
- Bloom: `screens_bloom.rpy` and `bloom_utils.rpy`; applied to hovered objects.
- Letterbox: `letterbox_gui.rpy` overlay.

## Debugging & Logging

- Debug overlay (Cmd+Shift+F12 / Ctrl+Shift+F12): hidden → compact → verbose → hidden.
- Logging:
  - `sn_log_enabled`, `sn_log_color`, `sn_log_intercept_prints` toggles (Shift+O to set at runtime).
  - Built-in `print` is intercepted; logs are color-coded, prefixed with `::`, and truncated.

## Conventions & Best Practices

- Only call `game/api/*` from logic.
- Keep UI screens “dumb” — emit events to hooks and render state.
- Add doc headers to new modules with Overview, Contracts, and Examples.
- Keep room assets under `game/images/` matching object ids.
- Run `renpy.sh . lint` before PRs.

