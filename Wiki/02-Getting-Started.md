# Getting Started Guide

## Prerequisites

Before working with the Snatchernauts Framework, ensure you have:

### Required Software
- **Ren'Py SDK 8.4.x or later**: Download from [renpy.org](https://www.renpy.org/)
- **Text Editor**: VS Code, Atom, or any editor with Python syntax support
- **Git** (recommended): For version control and updates

### System Setup

#### 1. Install Ren'Py SDK

Download and extract the Ren'Py SDK to a convenient location:

**Linux/macOS:**
```bash
# Extract to home directory
cd ~
wget https://www.renpy.org/dl/8.4.1/renpy-8.4.1-sdk.tar.bz2
tar -xjf renpy-8.4.1-sdk.tar.bz2
```

**Windows:**
1. Download the SDK zip file
2. Extract to `C:\renpy-8.4.1-sdk` or similar location

#### 2. Set Environment Variables

Configuring the `RENPY_SDK` environment variable enables the framework's launcher script:

**Linux/macOS (bash/zsh):**
```bash
# Add to ~/.bashrc or ~/.zshrc
export RENPY_SDK=~/renpy-8.4.1-sdk

# Apply immediately
source ~/.bashrc  # or source ~/.zshrc
```

**Windows (Command Prompt):**
```cmd
# Temporary (current session)
set RENPY_SDK=C:\renpy-8.4.1-sdk

# Permanent (requires admin)
setx RENPY_SDK "C:\renpy-8.4.1-sdk"
```

**Windows (PowerShell):**
```powershell
# Add to PowerShell profile
$env:RENPY_SDK = "C:\renpy-8.4.1-sdk"
```

## Running the Framework

### Method 1: Unified Launcher Script (Recommended)

The framework includes a comprehensive launcher script with debugging and linting capabilities:

```bash
# Basic launch
scripts/run-game.sh

# Launch with debug console
scripts/run-game.sh --debug

# Run lint check before launching
scripts/run-game.sh --lint

# Compile and launch
scripts/run-game.sh --compile

# Show all available options
scripts/run-game.sh --help
```

### Method 2: Direct Ren'Py Launch

For manual control or troubleshooting:

```bash
# Basic launch
$RENPY_SDK/renpy.sh .

# With debugging
$RENPY_SDK/renpy.sh . --debug

# Compile only
$RENPY_SDK/renpy.sh . --compile
```

## Development Workflow

### 1. Code Development
- Edit game files in the `game/` directory
- Focus on logic files in `game/logic/` for gameplay implementation
- Use API modules in `game/api/` for common operations

### 2. Testing and Debugging
```bash
# Quick test with debug output
scripts/run-game.sh --debug

# Full development cycle
scripts/run-game.sh --lint --debug
```

### 3. Code Quality
```bash
# Lint checking
scripts/run-game.sh --lint

# Manual lint (alternative)
$RENPY_SDK/renpy.sh . lint
```

## Project Structure

Understanding the framework's organization:

```
snatchernauts_framework/
├── game/                    # Main game content
│   ├── logic/              # Game behavior and event handling
│   │   ├── game_logic.rpy  # Global game hooks
│   │   └── rooms/          # Per-room logic handlers
│   ├── api/                # Helper functions and utilities
│   │   ├── room_api.rpy    # Room and object management
│   │   ├── ui_api.rpy      # User interface helpers
│   │   ├── interactions_api.rpy # Player interaction handling
│   │   └── display_api.rpy # Visual effects control
│   ├── ui/                 # Screen definitions and layouts
│   ├── overlays/           # Special effect overlays
│   ├── shaders/            # GLSL shader effects
│   ├── core/               # Framework core functionality
│   └── rooms/              # Room-specific assets and configuration
├── scripts/                # Development and build scripts
├── Wiki/                   # Documentation (this manual)
└── README.md              # Project overview
```

### Key Directories Explained

#### `game/logic/`
**Purpose**: Contains your game's behavioral logic
- Implement event handlers like `on_room_enter()`, `on_object_interact()`
- Register per-room logic classes for organized code
- Handle game state changes and story progression

#### `game/api/`
**Purpose**: Pre-built functions for common operations
- Room loading and object management
- UI creation and interaction handling
- Effect control and visual enhancements
- Avoid duplicating code across different parts of your game

#### `game/ui/`
**Purpose**: Screen definitions for user interface
- Room exploration screens
- Interaction menus and dialogs
- Description boxes and tooltips
- Visual transforms and animations

#### `game/core/`
**Purpose**: Framework configuration and utilities
- Game options and settings
- Logging and debugging systems
- Room configuration management
- Common utility functions

## Building and Distribution

For creating distributable versions of your game:

### Using Ren'Py Launcher
1. Open Ren'Py Launcher
2. Select your project
3. Click "Build & Distribute"
4. Choose target platforms (Windows, Mac, Linux)
5. Configure build options as needed

### Command Line Building
```bash
# Build all platforms
$RENPY_SDK/renpy.sh . distribute

# Build specific platform
$RENPY_SDK/renpy.sh . distribute --package win
```

## Next Steps

After completing this setup:

1. **[Architecture Overview](03-Architecture.md)**: Understand how the framework components work together
2. **[Logic Hooks](04-Logic-Hooks.md)**: Learn to implement game behavior through event handlers
3. **[API Reference](05-API-Room.md)**: Explore the available helper functions
4. **[Examples](09-Examples.md)**: Study working code samples

## Troubleshooting Common Issues

### "RENPY_SDK not found"
- Verify the SDK is installed at the expected path
- Check that the environment variable is set correctly
- Use absolute paths if relative paths cause issues

### "Permission denied" on Linux/macOS
```bash
# Make launcher script executable
chmod +x scripts/run-game.sh
chmod +x $RENPY_SDK/renpy.sh
```

### Lint failures
- Review error messages carefully
- Check for syntax errors in .rpy files
- Ensure proper indentation and Ren'Py syntax

### Game won't start
- Run with `--debug` flag to see detailed error output
- Check console for Python exceptions
- Verify all required assets are present

