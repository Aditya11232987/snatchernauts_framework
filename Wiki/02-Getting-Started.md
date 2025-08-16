# Getting Started Guide

**Part I: Getting Started - Chapter 2**

*A comprehensive guide to installing, configuring, and setting up your development environment for the Snatchernauts Framework, with step-by-step instructions for all supported platforms.*

---

## Chapter Overview

This chapter provides complete instructions for establishing a functional development environment for the Snatchernauts Framework. Whether you're a seasoned Ren'Py developer or completely new to interactive visual novel development, this guide ensures you'll have all necessary tools properly configured and ready for productive development.

By the end of this chapter, you will have:
- A complete Ren'Py SDK installation with proper environment configuration
- The Snatchernauts Framework installed and verified as functional
- Essential development tools configured for optimal productivity
- Your first framework project created and running
- Understanding of the development workflow and best practices

## Essential Prerequisites

Successful framework development requires several foundational components. This section details each requirement and provides specific version recommendations based on extensive compatibility testing.

### Core Software Requirements

**Ren'Py SDK 8.4.x or Later**: The framework leverages advanced features introduced in Ren'Py 8.4.x, including improved shader support, enhanced Python integration, and optimized performance systems. Earlier versions lack essential capabilities and are not compatible.

**Recommended Version**: Ren'Py 8.4.1 or latest stable release  
**Download Source**: [Official Ren'Py Website](https://www.renpy.org/)  
**Installation Size**: Approximately 250MB for complete SDK

**Professional Text Editor**: While any text editor works for basic development, a feature-rich editor significantly improves development efficiency and code quality:

**Highly Recommended Options**:
- **Visual Studio Code**: Free, excellent Python support, integrated terminal, Git integration
- **PyCharm Community**: Advanced Python features, debugging support, project management
- **Sublime Text**: Fast, lightweight, extensive plugin ecosystem
- **Vim/Neovim**: For experienced terminal users, highly customizable

**Minimum Requirements**: Syntax highlighting for Python and basic file management capabilities

**Version Control System**: Git provides essential functionality for framework development:
- **Framework Updates**: Easy integration of framework improvements and bug fixes
- **Project Management**: Track changes, manage branches, collaborate with teams
- **Backup and Recovery**: Distributed version control protects against data loss
- **Community Integration**: Seamless interaction with GitLab, GitHub, and other platforms

### Additional Development Tools

**Command Line Interface**: Framework development benefits significantly from command-line familiarity:
- **Windows**: PowerShell (recommended) or Command Prompt
- **macOS**: Terminal with bash or zsh
- **Linux**: Any terminal emulator with bash, zsh, or fish

**Graphics Software** (Optional but Recommended):
- **Asset Creation**: GIMP, Krita, or Photoshop for creating interactive objects and backgrounds
- **Sprite Editing**: Aseprite for pixel art, specialized sprite creation tools
- **Image Optimization**: Tools for reducing file sizes while maintaining visual quality

## Complete System Setup Guide

This section provides step-by-step installation procedures for all supported platforms, including troubleshooting guidance and verification steps.

### Step 1: Ren'Py SDK Installation

The Ren'Py SDK forms the foundation of all framework development. Proper installation ensures optimal performance and compatibility.

#### Linux Installation

**Prerequisites**: Ensure `wget` and `tar` are available on your system. Most distributions include these by default.

```bash
# Navigate to your preferred installation directory
cd ~/Development  # or any suitable location

# Download the latest stable SDK
wget https://www.renpy.org/dl/8.4.1/renpy-8.4.1-sdk.tar.bz2

# Extract the SDK
tar -xjf renpy-8.4.1-sdk.tar.bz2

# Verify extraction completed successfully
ls -la renpy-8.4.1-sdk/

# Optional: Clean up download file
rm renpy-8.4.1-sdk.tar.bz2
```

**Installation Verification**: The extracted directory should contain `renpy.sh`, `renpy/`, `sdk-fonts/`, and other core components.

#### macOS Installation

**Prerequisites**: macOS 10.15 (Catalina) or later recommended for optimal compatibility.

```bash
# Create development directory if it doesn't exist
mkdir -p ~/Development
cd ~/Development

# Download using curl (alternative to wget)
curl -O https://www.renpy.org/dl/8.4.1/renpy-8.4.1-sdk.tar.bz2

# Extract the SDK
tar -xjf renpy-8.4.1-sdk.tar.bz2

# Make the launcher executable
chmod +x renpy-8.4.1-sdk/renpy.sh

# Test the installation
./renpy-8.4.1-sdk/renpy.sh --version
```

**Security Note**: macOS may display a security warning when first running Ren'Py. Go to System Preferences > Security & Privacy > General and click "Allow Anyway" if this occurs.

#### Windows Installation

**Method 1: Direct Download (Recommended)**

1. Visit [renpy.org](https://www.renpy.org/) and download the Windows SDK
2. Extract the zip file to a permanent location:
   - **Recommended**: `C:\Development\renpy-8.4.1-sdk`
   - **Alternative**: `%USERPROFILE%\Development\renpy-8.4.1-sdk`
3. Ensure the extraction path contains no spaces or special characters

**Method 2: PowerShell Automated Installation**

```powershell
# Create development directory
New-Item -ItemType Directory -Path "C:\Development" -Force
Set-Location "C:\Development"

# Download SDK (requires PowerShell 3.0+)
Invoke-WebRequest -Uri "https://www.renpy.org/dl/8.4.1/renpy-8.4.1-sdk.zip" -OutFile "renpy-sdk.zip"

# Extract using built-in cmdlet
Expand-Archive -Path "renpy-sdk.zip" -DestinationPath "."

# Clean up
Remove-Item "renpy-sdk.zip"

# Verify installation
.\renpy-8.4.1-sdk\renpy.exe --version
```

### Step 2: Environment Configuration

Proper environment setup enables seamless framework development and simplifies command-line operations.

#### Linux Environment Setup

**For Bash Users** (most common):

```bash
# Open your shell configuration file
nano ~/.bashrc  # or use your preferred editor

# Add these lines at the end of the file:
export RENPY_SDK="$HOME/Development/renpy-8.4.1-sdk"
export PATH="$RENPY_SDK:$PATH"

# Apply changes immediately
source ~/.bashrc

# Verify configuration
echo $RENPY_SDK
which renpy.sh
```

**For Zsh Users** (default on macOS and some Linux distributions):

```bash
# Edit Zsh configuration
nano ~/.zshrc

# Add the same environment variables:
export RENPY_SDK="$HOME/Development/renpy-8.4.1-sdk"
export PATH="$RENPY_SDK:$PATH"

# Apply changes
source ~/.zshrc
```

**For Fish Shell Users**:

```fish
# Add to Fish configuration
set -Ux RENPY_SDK ~/Development/renpy-8.4.1-sdk
fish_add_path $RENPY_SDK
```

#### macOS Environment Setup

Modern macOS versions use Zsh by default, but some users may still use Bash:

```bash
# Check your current shell
echo $SHELL

# For Zsh (default on macOS Catalina+)
nano ~/.zshrc

# For Bash (older macOS versions)
nano ~/.bash_profile

# Add these lines (adjust path if you used a different location):
export RENPY_SDK="$HOME/Development/renpy-8.4.1-sdk"
export PATH="$RENPY_SDK:$PATH"

# Apply changes based on your shell
source ~/.zshrc     # for Zsh
source ~/.bash_profile  # for Bash
```

#### Windows Environment Setup

**Method 1: System Environment Variables (Persistent)**

1. Right-click "This PC" and select "Properties"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Set Variable name: `RENPY_SDK`
6. Set Variable value: `C:\Development\renpy-8.4.1-sdk`
7. Click "OK" and restart your terminal

**Method 2: PowerShell Profile (Recommended for Developers)**

```powershell
# Check if profile exists
Test-Path $PROFILE

# Create profile if it doesn't exist
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -Type File -Force
}

# Edit the profile
notepad $PROFILE

# Add this line to the profile:
$env:RENPY_SDK = "C:\Development\renpy-8.4.1-sdk"
$env:PATH += ";$env:RENPY_SDK"

# Reload profile
. $PROFILE
```

**Method 3: Command Prompt (Session-specific)**

```cmd
# Set for current session only
set RENPY_SDK=C:\Development\renpy-8.4.1-sdk
set PATH=%RENPY_SDK%;%PATH%

# Set permanently (requires administrator privileges)
setx RENPY_SDK "C:\Development\renpy-8.4.1-sdk"
setx PATH "%PATH%;%RENPY_SDK%"
```

### Step 3: Framework Installation

Obtain and configure the Snatchernauts Framework for development.

#### Option A: Git Clone (Recommended)

```bash
# Clone the framework repository
git clone https://github.com/snatchernauts/snatchernauts_framework.git
cd snatchernauts_framework

# Verify framework structure
ls -la game/
ls -la scripts/
```

#### Option B: Download Archive

1. Download the framework archive from the project repository
2. Extract to your desired project location
3. Navigate to the extracted directory

### Step 4: Installation Verification

Confirm that all components are properly installed and configured.

#### Environment Verification

```bash
# Check Ren'Py SDK accessibility
renpy.sh --version  # Linux/macOS
renpy.exe --version  # Windows

# Verify environment variable
echo $RENPY_SDK  # Linux/macOS/PowerShell
echo %RENPY_SDK%  # Windows Command Prompt

# Test framework launcher
scripts/run-game.sh --help  # Linux/macOS
```

#### First Launch Test

```bash
# Launch the framework demo
scripts/run-game.sh

# Alternative direct launch
$RENPY_SDK/renpy.sh .  # Linux/macOS
%RENPY_SDK%\renpy.exe .  # Windows
```

**Expected Result**: The Ren'Py launcher should open, showing the Snatchernauts Framework project. Clicking "Launch Project" should start the framework's demo content.

## Launching and Running the Framework

The framework provides multiple methods for launching projects, each suited to different development scenarios.

### Primary Launch Methods

#### Method 1: Enhanced Launcher Script (Recommended)

The framework includes a sophisticated launcher script that provides development-oriented features beyond basic Ren'Py functionality:

```bash
# Basic project launch
scripts/run-game.sh

# Launch with comprehensive debugging output
scripts/run-game.sh --debug

# Perform code quality checks before launch
scripts/run-game.sh --lint

# Compile project files and then launch
scripts/run-game.sh --compile

# Combine multiple flags for complete development workflow
scripts/run-game.sh --lint --compile --debug

# Display all available options and usage information
scripts/run-game.sh --help
```

**Launcher Script Advantages**:
- **Integrated Development Workflow**: Combines linting, compilation, and debugging in one command
- **Error Detection**: Identifies common issues before they cause runtime problems
- **Development Optimization**: Provides shortcuts for frequent development tasks
- **Consistent Environment**: Ensures proper environment setup regardless of platform

#### Method 2: Direct Ren'Py Execution

For situations requiring manual control or when troubleshooting launcher script issues:

```bash
# Standard launch (Linux/macOS)
$RENPY_SDK/renpy.sh .

# Standard launch (Windows)
%RENPY_SDK%\renpy.exe .

# Launch with debug console enabled
$RENPY_SDK/renpy.sh . --debug

# Compile project without launching
$RENPY_SDK/renpy.sh . --compile

# Force recompilation of all files
$RENPY_SDK/renpy.sh . --compile --clean

# Launch with specific logging level
$RENPY_SDK/renpy.sh . --log-level debug
```

#### Method 3: Ren'Py Launcher GUI

Suitable for developers who prefer graphical interfaces:

1. Navigate to your Ren'Py SDK directory
2. Run the launcher executable (`renpy.sh` on Linux/macOS, `renpy.exe` on Windows)
3. The framework project should appear in the projects list
4. Select the project and click "Launch Project"

**GUI Advantages**:
- **Visual Project Management**: Easy project selection and switching
- **Integrated Tools**: Access to built-in editors, distribution tools, and documentation
- **Beginner-Friendly**: Familiar interface for users new to command-line development

### Development Workflow Integration

Optimal development requires a structured approach that integrates coding, testing, and quality assurance.

#### Standard Development Cycle

**Phase 1: Code Development**

```bash
# Open your preferred editor
code .  # Visual Studio Code
# or
pycharm .  # PyCharm
# or
vim game/logic/  # Vim/Neovim
```

**Key Development Areas**:
- **Game Logic**: Edit files in `game/logic/` to implement game behavior
- **Room Definitions**: Create and modify room configurations in `game/rooms/`
- **UI Components**: Design interfaces in `game/ui/` for player interaction
- **Asset Integration**: Manage images, sounds, and other media assets

**Phase 2: Code Quality and Testing**

```bash
# Comprehensive pre-launch validation
scripts/run-game.sh --lint --compile --debug

# Focused lint checking for syntax and style issues
scripts/run-game.sh --lint

# Manual Ren'Py lint (alternative approach)
$RENPY_SDK/renpy.sh . lint
```

**Phase 3: Iterative Testing**

```bash
# Quick launch for immediate testing
scripts/run-game.sh

# Debug launch for detailed error analysis
scripts/run-game.sh --debug

# Performance testing with compilation
scripts/run-game.sh --compile
```

#### Advanced Development Workflows

**Continuous Integration Approach**:

```bash
#!/bin/bash
# development-cycle.sh - Automated development workflow

echo "Starting development cycle..."

# Stage 1: Code quality validation
echo "Checking code quality..."
scripts/run-game.sh --lint
if [ $? -ne 0 ]; then
    echo "Lint errors detected. Please fix before proceeding."
    exit 1
fi

# Stage 2: Compilation verification
echo "Compiling project..."
scripts/run-game.sh --compile
if [ $? -ne 0 ]; then
    echo "Compilation failed. Please check for errors."
    exit 1
fi

# Stage 3: Test launch
echo "Launching for testing..."
scripts/run-game.sh --debug
```

**Hot-Reload Development** (for rapid iteration):

```bash
# Use filesystem monitoring tools for automatic reloading
# Linux/macOS with inotify/fsevents
while inotifywait -r -e modify game/; do
    clear
    echo "Files changed, reloading..."
    scripts/run-game.sh --compile
done
```

## Framework Architecture and Project Organization

Understanding the framework's structure is essential for effective development and maintenance.

### Complete Directory Structure

```
snatchernauts_framework/
├── game/                           # Main Ren'Py game directory
│   ├── logic/                      # Game behavior implementation
│   │   ├── game_logic.rpy          # Global event handlers and hooks
│   │   ├── room_logic_base.rpy     # Base class for room-specific logic
│   │   └── rooms/                  # Per-room logic implementations
│   │       ├── room_001.rpy        # Logic for Room 001
│   │       ├── room_002.rpy        # Logic for Room 002
│   │       └── ...                 # Additional room logic files
│   ├── api/                        # Framework API and utility functions
│   │   ├── room_api.rpy            # Room loading and management
│   │   ├── ui_api.rpy              # User interface creation helpers
│   │   ├── interactions_api.rpy    # Player interaction handling
│   │   ├── display_api.rpy         # Visual effects and display control
│   │   ├── audio_api.rpy           # Sound and music management
│   │   └── save_api.rpy            # Save/load functionality
│   ├── ui/                         # Screen definitions and UI layouts
│   │   ├── exploration_screen.rpy  # Main room exploration interface
│   │   ├── interaction_menus.rpy   # Object interaction menus
│   │   ├── description_boxes.rpy   # Text display components
│   │   ├── effects_screens.rpy     # Visual effect overlays
│   │   └── debug_screens.rpy       # Development and debugging interfaces
│   ├── overlays/                   # Special visual effect layers
│   │   ├── particle_effects.rpy    # Particle system definitions
│   │   ├── weather_effects.rpy     # Environmental effects
│   │   └── transition_effects.rpy  # Scene transition animations
│   ├── shaders/                    # GLSL shader programs
│   │   ├── blur_effects.glsl       # Blur and focus effects
│   │   ├── color_filters.glsl      # Color manipulation shaders
│   │   └── distortion_effects.glsl # Visual distortion effects
│   ├── core/                       # Framework core functionality
│   │   ├── options.rpy             # Game configuration and settings
│   │   ├── logging.rpy             # Debugging and logging systems
│   │   ├── room_config.rpy         # Room configuration management
│   │   ├── object_definitions.rpy  # Interactive object definitions
│   │   └── utilities.rpy           # Common utility functions
│   ├── rooms/                      # Room-specific content and assets
│   │   ├── room_001/               # Assets and config for Room 001
│   │   │   ├── room_config.json    # Room layout and object definitions
│   │   │   ├── backgrounds/        # Background images
│   │   │   ├── objects/            # Interactive object sprites
│   │   │   └── audio/              # Room-specific sounds
│   │   ├── room_002/               # Assets and config for Room 002
│   │   └── ...                     # Additional room directories
│   ├── images/                     # Global image assets
│   │   ├── ui/                     # User interface graphics
│   │   ├── effects/                # Visual effect sprites
│   │   └── common/                 # Shared graphical elements
│   ├── audio/                      # Global audio assets
│   │   ├── music/                  # Background music files
│   │   ├── sfx/                    # Sound effects
│   │   └── ambient/                # Ambient audio loops
│   ├── saves/                      # Save game storage (generated)
│   └── cache/                      # Compiled files (generated)
├── scripts/                        # Development and utility scripts
│   ├── run-game.sh                 # Enhanced project launcher
│   ├── build-game.sh               # Automated build script
│   ├── validate-assets.sh          # Asset validation utility
│   └── development-tools/          # Additional development utilities
├── Wiki/                           # Documentation and manual
│   ├── 01-Introduction.md          # Framework introduction
│   ├── 02-Getting-Started.md       # This setup guide
│   ├── 03-Architecture.md          # Framework architecture details
│   └── ...                         # Additional documentation files
├── README.md                       # Project overview and quick start
├── LICENSE                         # Software license information
└── .gitignore                      # Version control ignore rules
```

### Core Component Responsibilities

#### `game/logic/` - Behavioral Implementation

**Primary Purpose**: Contains the interactive behavior that defines your game's unique functionality.

**Key Files and Their Roles**:
- **`game_logic.rpy`**: Global event handlers that respond to framework-wide events
  - `on_game_start()`: Initialize game state when the game begins
  - `on_room_enter(room_id)`: Handle player entering any room
  - `on_object_interact(object_id)`: Process interactions with any object
  - `on_game_save()`: Custom save data preparation
  - `on_game_load()`: Custom save data restoration

- **`room_logic_base.rpy`**: Base class providing structure for room-specific logic
  - Standard event handler templates
  - Common room functionality
  - Inheritance patterns for consistent behavior

- **`rooms/*.rpy`**: Individual room behavior implementations
  - Room-specific event handlers
  - Custom object interactions unique to each room
  - Room state management and progression logic

**Development Pattern**: Create one logic file per room for organized, maintainable code. Each room logic class inherits from `RoomLogicBase` and overrides relevant event handlers.

#### `game/api/` - Framework Utilities

**Primary Purpose**: Provides pre-built, tested functions for common game development tasks, reducing code duplication and development time.

**Key API Modules**:

- **`room_api.rpy`**: Room and environment management
  - `load_room(room_id)`: Transition to a new room with proper cleanup
  - `get_room_objects()`: Retrieve list of interactive objects in current room
  - `set_room_background(image)`: Change room background with transition effects
  - `add_room_object(object_def)`: Dynamically add interactive objects

- **`ui_api.rpy`**: User interface creation and management
  - `create_description_box(text)`: Display formatted text descriptions
  - `show_interaction_menu(options)`: Present player choice menus
  - `create_tooltip(object_id, text)`: Add hover tooltips to objects
  - `show_effect_overlay(effect_type)`: Display visual effects over the scene

- **`interactions_api.rpy`**: Player interaction processing
  - `register_interaction(object_id, callback)`: Define object click behaviors
  - `handle_object_hover(object_id)`: Process mouse hover events
  - `validate_interaction(object_id)`: Check if interaction is currently allowed
  - `queue_interaction(interaction_data)`: Schedule delayed interactions

- **`display_api.rpy`**: Visual effects and display control
  - `apply_screen_filter(filter_type)`: Add visual filters (blur, color, etc.)
  - `create_particle_effect(effect_def)`: Generate particle-based effects
  - `animate_object(object_id, animation)`: Apply animations to objects
  - `manage_screen_transitions(transition_type)`: Control scene transitions

#### `game/ui/` - Interface Definitions

**Primary Purpose**: Defines the visual layout and interactive components of the game's user interface.

**Key Screen Components**:

- **`exploration_screen.rpy`**: Main gameplay interface
  - Room background display
  - Interactive object positioning and click handling
  - Navigation controls and menus
  - Status indicators and player feedback

- **`interaction_menus.rpy`**: Player choice and action interfaces
  - Object interaction option menus
  - Inventory management interfaces
  - Dialogue and conversation systems
  - Context-sensitive action buttons

- **`description_boxes.rpy`**: Text display and narrative components
  - Formatted text display with word wrapping
  - Multiple text styling options
  - Animated text reveal effects
  - Image and text combination layouts

#### `game/core/` - Framework Foundation

**Primary Purpose**: Provides essential functionality that supports all other framework components.

**Critical Core Files**:

- **`options.rpy`**: Game configuration and settings
  - Window size and display options
  - Audio and performance settings
  - Development mode toggles
  - Framework behavior customization

- **`room_config.rpy`**: Room definition and management systems
  - Room configuration loading and parsing
  - Object definition validation
  - Asset path resolution
  - Room state persistence

#### `game/rooms/` - Content and Assets

**Primary Purpose**: Houses all room-specific content, including configuration files, images, and audio assets.

**Room Directory Structure** (example: `room_001/`):

- **`room_config.json`**: Room layout and behavior definition
  ```json
  {
    "room_id": "room_001",
    "name": "Example Room",
    "background": "backgrounds/room_001_bg.png",
    "objects": [
      {
        "id": "door",
        "image": "objects/door.png",
        "position": [100, 200],
        "interaction_type": "examine"
      }
    ]
  }
  ```

- **`backgrounds/`**: Room background images in various resolutions
- **`objects/`**: Interactive object sprites and animation frames
- **`audio/`**: Room-specific ambient sounds and effects

## Building and Distribution

The framework supports comprehensive building and distribution workflows suitable for both development testing and commercial release.

### Development Builds

Quick builds for testing and development iteration:

```bash
# Compile current project state
scripts/run-game.sh --compile

# Alternative direct compilation
$RENPY_SDK/renpy.sh . --compile

# Force complete recompilation (clears cache)
$RENPY_SDK/renpy.sh . --compile --clean
```

### Distribution Builds

#### Using Ren'Py Launcher (GUI Method)

1. **Launch Ren'Py**: Start the Ren'Py Launcher application
2. **Select Project**: Choose your framework project from the list
3. **Access Build Tools**: Click "Build & Distribute" in the project menu
4. **Configure Build Options**:
   - **Platforms**: Select Windows, macOS, Linux, Android, or web
   - **Package Type**: Choose between full installer or portable archive
   - **Compression**: Configure file compression settings
   - **Digital Signing**: Add code signing certificates if available
5. **Execute Build**: Click "Build" and wait for completion
6. **Locate Packages**: Built packages appear in the project's `dists/` directory

#### Command Line Building (Advanced)

**Multi-Platform Distribution**:

```bash
# Build for all supported platforms
$RENPY_SDK/renpy.sh . distribute

# Build for specific platforms
$RENPY_SDK/renpy.sh . distribute --package win    # Windows only
$RENPY_SDK/renpy.sh . distribute --package mac    # macOS only
$RENPY_SDK/renpy.sh . distribute --package linux  # Linux only

# Build with specific options
$RENPY_SDK/renpy.sh . distribute --package win --dest ./builds/
```

**Automated Build Script**:

```bash
#!/bin/bash
# build-release.sh - Automated release building

set -e  # Exit on any error

echo "Starting automated build process..."

# Clean previous builds
rm -rf dists/

# Validate project before building
echo "Validating project..."
$RENPY_SDK/renpy.sh . lint
if [ $? -ne 0 ]; then
    echo "Project validation failed. Aborting build."
    exit 1
fi

# Build for all platforms
echo "Building distribution packages..."
$RENPY_SDK/renpy.sh . distribute

# Verify build results
echo "Build completed. Packages created:"
ls -la dists/

echo "Build process finished successfully."
```

### Build Customization

**Advanced Distribution Options**:

- **Custom Build Scripts**: Extend `scripts/build-game.sh` for project-specific requirements
- **Asset Optimization**: Implement image compression and audio optimization
- **Platform-Specific Builds**: Configure different settings per target platform
- **Automated Testing**: Integrate automated testing before distribution builds

## Comprehensive Troubleshooting Guide

This section addresses common issues encountered during framework setup and development, providing detailed solutions and prevention strategies.

### Installation and Environment Issues

#### "RENPY_SDK not found" or "Command not found"

**Cause**: Environment variables not properly configured or Ren'Py SDK not installed correctly.

**Solution Steps**:

1. **Verify SDK Installation**:
   ```bash
   # Check if SDK directory exists
   ls -la ~/Development/renpy-8.4.1-sdk/  # Linux/macOS
   dir C:\Development\renpy-8.4.1-sdk\    # Windows
   ```

2. **Validate Environment Variables**:
   ```bash
   # Check environment variable setting
   echo $RENPY_SDK  # Linux/macOS/PowerShell
   echo %RENPY_SDK%  # Windows Command Prompt
   ```

3. **Reconfigure Environment** (if variable is unset):
   ```bash
   # Linux/macOS - Add to shell profile
   export RENPY_SDK="/full/path/to/renpy-8.4.1-sdk"
   
   # Windows PowerShell
   $env:RENPY_SDK = "C:\full\path\to\renpy-8.4.1-sdk"
   ```

4. **Use Absolute Paths** (temporary workaround):
   ```bash
   # Direct execution with full path
   /home/user/Development/renpy-8.4.1-sdk/renpy.sh .  # Linux
   C:\Development\renpy-8.4.1-sdk\renpy.exe .        # Windows
   ```

#### Permission Denied Errors (Linux/macOS)

**Cause**: Execute permissions not set on launcher scripts or Ren'Py executables.

**Solution**:

```bash
# Make framework launcher executable
chmod +x scripts/run-game.sh

# Make Ren'Py SDK executable
chmod +x $RENPY_SDK/renpy.sh

# Make all scripts in the scripts directory executable
chmod +x scripts/*

# Verify permissions
ls -la scripts/run-game.sh
ls -la $RENPY_SDK/renpy.sh
```

#### macOS Security Warnings

**Cause**: macOS Gatekeeper preventing execution of unsigned applications.

**Solution**:

1. **Allow in Security Preferences**:
   - Go to System Preferences → Security & Privacy → General
   - Click "Allow Anyway" next to the blocked application message
   - Re-run the application

2. **Alternative Command-Line Override**:
   ```bash
   # Remove quarantine attribute
   xattr -dr com.apple.quarantine $RENPY_SDK/
   ```

### Development and Runtime Issues

#### Lint Failures and Syntax Errors

**Common Causes and Solutions**:

**Python Indentation Issues**:
```python
# Incorrect - mixed spaces and tabs
init python:
    variable = "value"  # spaces
	other_var = 123     # tab - causes error

# Correct - consistent indentation
init python:
    variable = "value"
    other_var = 123
```

**Ren'Py Syntax Violations**:
```renpy
# Incorrect - missing colon
label start
    "Hello, world!"
    return

# Correct - proper label syntax
label start:
    "Hello, world!"
    return
```

**File Encoding Issues**:
```bash
# Check file encoding
file game/logic/game_logic.rpy

# Convert to UTF-8 if necessary
iconv -f ISO-8859-1 -t UTF-8 game/logic/game_logic.rpy > temp_file
mv temp_file game/logic/game_logic.rpy
```

#### Game Won't Start or Crashes

**Diagnostic Steps**:

1. **Enable Debug Mode**:
   ```bash
   scripts/run-game.sh --debug
   ```

2. **Check Console Output**:
   - Look for Python tracebacks
   - Identify missing files or assets
   - Note configuration errors

3. **Validate Asset Paths**:
   ```bash
   # Check for missing background images
   find game/rooms/ -name "*.json" -exec grep -l "backgrounds/" {} \;
   
   # Verify referenced images exist
   scripts/validate-assets.sh  # if available
   ```

4. **Test with Minimal Configuration**:
   - Temporarily rename custom logic files
   - Test with framework defaults only
   - Gradually re-enable custom components

#### Performance and Memory Issues

**Optimization Strategies**:

1. **Image Optimization**:
   ```bash
   # Compress large background images
   find game/rooms/ -name "*.png" -size +1M -exec pngcrush {} {}.compressed \;
   
   # Convert to WebP for smaller file sizes (if supported)
   find game/rooms/ -name "*.png" -exec cwebp {} -o {}.webp \;
   ```

2. **Audio Compression**:
   ```bash
   # Convert to OGG Vorbis for smaller files
   find game/audio/ -name "*.wav" -exec oggenc {} \;
   ```

3. **Code Optimization**:
   - Minimize frequent screen updates
   - Cache expensive calculations
   - Use appropriate data structures
   - Profile performance with Ren'Py's built-in tools

### Platform-Specific Issues

#### Windows-Specific Problems

**Path Length Limitations**:
```bash
# Windows has a 260-character path limit
# Use shorter directory names or enable long path support
# Enable via Group Policy or Registry:
# HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
# Set LongPathsEnabled to 1
```

**PowerShell Execution Policy**:
```powershell
# Check current execution policy
Get-ExecutionPolicy

# Allow local scripts (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Linux-Specific Problems

**Missing Dependencies**:
```bash
# Install common missing packages
sudo apt-get install python3-dev libffi-dev libssl-dev  # Debian/Ubuntu
sudo yum install python3-devel libffi-devel openssl-devel  # CentOS/RHEL
sudo pacman -S python libffi openssl  # Arch Linux
```

**Sound System Issues**:
```bash
# Install ALSA/PulseAudio development packages
sudo apt-get install libasound2-dev pulseaudio-dev  # Debian/Ubuntu
```

### Advanced Debugging Techniques

#### Log File Analysis

```bash
# Enable detailed logging
export RENPY_LOG_LEVEL=debug
scripts/run-game.sh --debug > debug.log 2>&1

# Analyze log for patterns
grep -i error debug.log
grep -i exception debug.log
grep -i traceback debug.log
```

#### Memory and Performance Profiling

```python
# Add to game/core/debug.rpy
init python:
    import psutil
    import time
    
    def log_performance():
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent()
        
        renpy.log.write(f"Memory: {memory_mb:.1f}MB, CPU: {cpu_percent:.1f}%")
    
    # Call periodically during development
    config.periodic_callback = log_performance
    config.periodic_interval = 5.0  # Every 5 seconds
```

## Navigation and Next Steps

With your development environment properly configured and the framework successfully running, you're ready to advance to more specialized topics.

### Immediate Next Steps

**Essential Reading Order**:

1. **[Framework Architecture](03-Architecture)** - Understand the complete system design, component relationships, and data flow patterns that enable the framework's functionality.

2. **[Logic Hooks System](04-Logic-Hooks)** - Master the event-driven architecture that allows you to implement custom game behavior through standardized callback functions.

3. **[Room API Reference](05-API-Room)** - Explore the comprehensive room management system, including loading, configuration, and object manipulation capabilities.

4. **[UI API Reference](06-API-UI)** - Learn to create sophisticated user interfaces using the framework's pre-built components and customization options.

5. **[Interaction System](07-API-Interactions)** - Implement complex player interactions, object behaviors, and environmental responses.

### Advanced Topics (After Mastering Basics)

**Specialized Development Areas**:

- **[Visual Effects and Shaders](08-API-Effects)**: Create stunning visual effects using GLSL shaders and the framework's effect system
- **[Audio Integration](08-API-Audio)**: Implement dynamic audio systems with positional sound, music management, and effect layering
- **[Save/Load Systems](08-API-Save)**: Design robust save game functionality with custom data serialization and state management
- **[Performance Optimization](10-Performance)**: Optimize your game for smooth performance across different platforms and hardware configurations

### Practical Application

**Hands-On Learning Path**:

1. **Examine the Demo Content**: Study the included example rooms and logic implementations
2. **Create a Simple Room**: Build your first custom room with basic objects and interactions
3. **Implement Custom Logic**: Add unique behavior using the logic hooks system
4. **Experiment with APIs**: Try different API functions to understand their capabilities
5. **Build a Complete Scene**: Combine multiple rooms into a cohesive gameplay experience

### Community and Support

**Getting Help**:

- **Documentation**: This manual provides comprehensive coverage of all framework features
- **Example Code**: Study the `game/logic/rooms/` directory for implementation patterns
- **Community Forums**: Join discussions with other framework developers
- **Issue Reporting**: Report bugs and request features through the project's issue tracker

### Development Best Practices

**Recommendations for Success**:

- **Start Small**: Begin with simple rooms and gradually add complexity
- **Follow Patterns**: Use the established conventions demonstrated in example code
- **Test Frequently**: Use the debug mode and linting tools regularly during development
- **Document Your Work**: Comment your code and maintain notes about your design decisions
- **Version Control**: Use Git to track changes and experiment safely with new features

---

**Navigation**:

← [**Previous: Introduction**](01-Introduction) | [**Next: Architecture Overview**](03-Architecture) →

---

*This completes Chapter 2 of the Snatchernauts Framework Manual. You now have a fully configured development environment and understanding of the basic development workflow. Continue to the Architecture Overview to learn how the framework's components work together to create engaging interactive experiences.*

