# Framework Overview

## Introduction

The Snatchernauts Framework is a comprehensive extension to Ren'Py 8.4.x designed to create interactive point-and-click visual novels with the tactile, exploratory gameplay reminiscent of classic titles like *Snatcher* and *Policenauts*. This framework transforms traditional visual novel storytelling by adding structured room-based exploration, contextual interactions, and cinematic effects.

## Design Philosophy

The framework is built on four core principles:

### 1. Interactivity First
Every element in a scene can be an interactive object with pixel-accurate hotspots. Players navigate using mouse, keyboard, or gamepad controls with contextual action menus for natural exploration.

### 2. Clean Architecture
Code organization follows clear separation of concerns:
- **Logic Layer**: Game behavior in centralized hook functions
- **UI Layer**: Screen composition and visual presentation
- **API Layer**: Reusable helper modules for common operations
- **Effects Layer**: Cinematic shaders and overlays

### 3. Cinematic Presentation
Built-in visual effects system provides:
- CRT simulation with configurable scanlines and distortion
- Bloom and desaturation effects for object highlighting
- Letterbox shader system for dramatic scenes
- Film grain, lighting, and atmospheric effects

### 4. Developer-Friendly
Sensible defaults with extensive customization options:
- Runtime debugging with categorized output
- Hot-reloadable configurations
- Comprehensive error handling and validation
- Modular component system

## Key Features

### Room-Based Exploration
- **Object System**: Define interactive elements with custom properties, actions, and visual effects
- **Navigation**: Seamless movement between objects using keyboard, mouse, or gamepad
- **Hotspots**: Pixel-accurate click detection using image alpha channels
- **State Management**: Room and object states persist across sessions

### Advanced Visual Effects
- **Shader Pipeline**: GLSL-based effects for professional visual quality
- **Color Grading**: Multiple preset atmospheres (noir, neon, vintage, etc.)
- **Dynamic Lighting**: Real-time lighting effects with animation support
- **Particle Effects**: Film grain, fog, and atmospheric overlays

### Centralized Logic System
- **Event Hooks**: Respond to game events through simple Python functions
- **Room Handlers**: Per-room logic classes for organized code structure
- **API Integration**: Pre-built functions for common operations
- **State Tracking**: Automatic persistence of game progress and choices

### Development Tools
- **Unified Launcher**: Single script for running, debugging, and linting
- **Debug Overlays**: Real-time performance monitoring and state inspection
- **Logging System**: Categorized output with runtime toggles
- **Error Handling**: Clear validation messages and troubleshooting guidance

## Target Audience

This framework is designed for:
- **Visual Novel Developers** seeking to add interactive exploration elements
- **Adventure Game Creators** wanting Ren'Py's scripting convenience
- **Indie Developers** needing a complete framework for story-driven games
- **Hobbyists** interested in creating retro-style interactive fiction

## System Requirements

- **Ren'Py**: Version 8.4.x or later
- **Python**: 2.7+ or 3.6+ (included with Ren'Py)
- **Operating System**: Windows, macOS, or Linux
- **Graphics**: OpenGL 2.0+ support for shader effects
- **Development**: Text editor and basic command-line familiarity
