# Installation Guide

This guide will help you set up the Snatchernauts Framework in your Ren'Py project and get your first room running.

## 📋 Prerequisites

Before installing the framework, ensure you have:

### Required
- **Ren'Py 8.3.7 or later** - [Download from renpy.org](https://www.renpy.org/latest.html)
- **Basic Ren'Py knowledge** - Understanding of screens, labels, and Python basics
- **Graphics card** - For bloom effects (integrated graphics OK)

### Recommended
- **Code editor** - VS Code, Sublime Text, or similar with Ren'Py syntax support
- **Git** - For version control and easy updates
- **Image editor** - For creating custom assets (GIMP, Photoshop, Aseprite, etc.)

## 🚀 Installation Methods

### Method 1: Clone the Repository (Recommended)

1. **Clone the framework:**
   ```bash
   git clone https://gitlab.com/yourusername/snatchernauts_framework.git
   cd snatchernauts_framework
   ```

2. **Open in Ren'Py:**
   - Launch the Ren'Py SDK
   - Click "Projects" → "Select Project Directory"  
   - Navigate to the cloned `snatchernauts_framework` folder
   - Click "Launch Project" to run the demo

3. **Test the installation:**
   - The demo room should load with a detective and Patreon logo
   - Try mouse hover to see descriptions
   - Test gamepad navigation with a connected controller

### Method 2: Download and Extract

1. **Download the latest release:**
   - Visit the [GitLab Releases page](../../releases)
   - Download the latest `.zip` or `.tar.gz` file
   - Extract to your desired location

2. **Open in Ren'Py:**
   - Follow the same steps as Method 1, step 2

### Method 3: Integration into Existing Project

If you want to add the framework to an existing Ren'Py project:

1. **Copy framework files:**
   ```bash
   # Copy core framework files to your project
   cp -r snatchernauts_framework/game/room_*.rpy your_project/game/
   cp -r snatchernauts_framework/game/bloom_*.rpy your_project/game/
   cp -r snatchernauts_framework/game/common_utils.rpy your_project/game/
   cp -r snatchernauts_framework/game/config_builders.rpy your_project/game/
   cp -r snatchernauts_framework/game/object_factory.rpy your_project/game/
   cp -r snatchernauts_framework/game/font_config.rpy your_project/game/
   ```

2. **Copy assets:**
   ```bash
   # Copy fonts and example images
   cp -r snatchernauts_framework/game/fonts/ your_project/game/
   cp -r snatchernauts_framework/game/images/ your_project/game/
   ```

3. **Add to your main script:**
   ```python
   # Add to your script.rpy or main menu
   label start:
       # Your existing code...
       
       # Jump to room exploration
       call explore_room
       
       return
   ```

## 🔧 Configuration

### Basic Configuration

The framework comes with sensible defaults, but you can customize it:

1. **Edit room configuration:**
   ```python
   # In game/room_config.rpy
   default current_room_id = "room1"          # Starting room
   default gamepad_navigation_enabled = True  # Enable gamepad
   default move_speed = 5                     # Editor movement speed
   ```

2. **Customize bloom colors:**
   ```python
   # In game/bloom_colors.rpy
   BLOOM_COLORS = {
       "detective": "#733939",    # Dark red glow
       "my_object": "#00FF00",    # Green glow
       "default": "#FFFFFF"       # White fallback
   }
   ```

### Font Configuration

The framework includes the Quaver pixel font for retro aesthetics:

```python
# In game/font_config.rpy
# Font sizes are optimized for pixel-perfect rendering
# Use multiples of 8: 8, 16, 24, 32, 40, 48
```

## 🧪 Testing Your Installation

### 1. Run the Demo
- Launch the project in Ren'Py
- Navigate the main menu and select "Start"
- You should see a room with a detective and Patreon logo

### 2. Test Mouse Controls
- **Hover** over objects to see floating descriptions
- **Click** the "Exit Room" button in the top-right
- **Click** "Editor Mode" to test the live editor

### 3. Test Gamepad Controls (if available)
- **D-pad/Left stick** - Navigate between objects
- **A button** - Select first object if none selected
- **Back/Select** - Toggle gamepad navigation

### 4. Test Editor Mode
- Press **F1** or click "Editor Mode"
- Use **arrow keys** to move objects
- Use **+/-** to scale objects
- Press **S** to save changes
- Press **F1** again to exit editor mode

## 🐛 Troubleshooting

### Common Issues

**Error: "Could not load font"**
- Ensure `game/fonts/quaver.ttf` exists
- Check that the font file isn't corrupted
- Try re-downloading the framework

**Bloom effects not showing**
- Update your graphics drivers
- Try running on a different device
- Check Ren'Py preferences → Graphics settings

**Gamepad not detected**
- Ensure your controller is connected before launching
- Try different controller types (Xbox, PlayStation, etc.)
- Check controller works in other applications

**Objects not displaying**
- Verify image files exist in `game/images/`
- Check image paths in `room_config.rpy` are correct
- Ensure images are valid PNG files

### Debug Mode

Enable debug information:

```python
# In game/room_config.rpy
default show_editor_help = True  # Shows debug info in editor mode
```

### Log Files

Check Ren'Py log files for detailed error information:
- **Windows**: `%APPDATA%/RenPy/game_name/`
- **Mac**: `~/Library/RenPy/game_name/`
- **Linux**: `~/.renpy/game_name/`

## 📁 Project Structure After Installation

```
your_project/
├── game/
│   ├── room_config.rpy          # Room and object definitions
│   ├── room_main.rpy           # Core exploration system
│   ├── room_functions.rpy      # Room management functions
│   ├── bloom_shader.rpy        # Visual effects system
│   ├── fonts/
│   │   └── quaver.ttf          # Pixel font
│   └── images/
│       ├── room1.png           # Example room background
│       ├── detective.png       # Example object
│       └── patreon.png        # Example object
├── README.md
├── LICENSE
└── .gitignore
```

## 🎯 Next Steps

After successful installation:

1. **Read the [Quick Start Tutorial](Quick-Start-Tutorial)** to create your first custom room
2. **Explore the [Room System](Room-System)** documentation for detailed usage
3. **Check out [Configuration Options](Configuration-Options)** to customize the framework
4. **Join the [GitLab Discussions](../../discussions)** to connect with other developers

## 📞 Getting Help

If you encounter issues:

1. **Check the [Troubleshooting](#-troubleshooting)** section above
2. **Search [existing issues](../../issues)** for solutions
3. **Create a new issue** with detailed information:
   - Operating system and version
   - Ren'Py version  
   - Error messages and log files
   - Steps to reproduce the problem

---

**Installation complete!** 🎉 You're ready to start building amazing point-and-click adventures!

[← Back to Wiki Home](Home) | [Quick Start Tutorial →](Quick-Start-Tutorial)
