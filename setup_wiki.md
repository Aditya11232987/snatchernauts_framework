# GitLab Wiki Setup Instructions

GitLab Wiki is a separate system from your repository files. You need to manually create the wiki pages. Here's how:

## 🔧 Enable and Set Up GitLab Wiki

### Step 1: Enable Wiki Feature
1. Go to your GitLab project: https://gitlab.com/grahfmusic/snatchernauts_framework
2. Click **Settings** → **General**
3. Expand **Visibility, features, permissions**
4. Enable **Wiki** checkbox
5. Click **Save changes**

### Step 2: Create Home Page
1. Go to **Wiki** in your project's left sidebar
2. Click **Create your first page** or **New page**
3. Title: `Home`
4. Copy the content below:

---

# Snatchernauts Framework Wiki

Welcome to the comprehensive documentation for the Snatchernauts Framework! This wiki contains detailed guides, tutorials, and API documentation to help you build amazing point-and-click adventure games with Ren'Py.

## 📚 Table of Contents

### Getting Started
- [Installation Guide](Installation-Guide) - Set up the framework in your project
- [Quick Start Tutorial](Quick-Start-Tutorial) - Build your first room in 10 minutes
- [Project Structure](Project-Structure) - Understanding the codebase organization

### Core Systems
- [Room System](Room-System) - Creating and managing explorable rooms  
- [Object System](Object-System) - Interactive objects and descriptions
- [Gamepad Support](Gamepad-Support) - Controller navigation implementation
- [Visual Effects](Visual-Effects) - Bloom effects and animations

### Advanced Features  
- [Editor Mode](Editor-Mode) - Live object positioning and scaling
- [Font System](Font-System) - Pixel-perfect text rendering
- [State Management](State-Management) - Saving and loading object positions
- [Configuration System](Configuration-System) - Object definitions and inheritance

### Customization Guides
- [Adding New Rooms](Adding-New-Rooms) - Step-by-step room creation
- [Custom Bloom Effects](Custom-Bloom-Effects) - Advanced visual customization
- [Animation System](Animation-System) - Creating hover animations
- [Description Boxes](Description-Boxes) - Smart positioning and styling

### API Reference
- [Function Reference](Function-Reference) - Complete function documentation
- [Configuration Options](Configuration-Options) - All available settings
- [Variable Reference](Variable-Reference) - Global variables and their usage
- [Event System](Event-System) - Hook into framework events

### Tutorials & Examples
- [Detective Game Tutorial](Detective-Game-Tutorial) - Build a complete detective scene
- [Art Gallery Example](Art-Gallery-Example) - Educational showcase implementation  
- [Mystery Room Tutorial](Mystery-Room-Tutorial) - Puzzle-solving gameplay
- [Performance Optimization](Performance-Optimization) - Best practices for smooth gameplay

### Development
- [Contributing Guide](https://gitlab.com/grahfmusic/snatchernauts_framework/-/blob/main/CONTRIBUTING.md) - How to contribute to the framework
- [Development Setup](Development-Setup) - Setting up a development environment
- [Testing Guide](Testing-Guide) - Manual and automated testing procedures
- [Release Process](Release-Process) - How framework releases are created

## 🚀 Quick Links

- **New to Ren'Py?** Start with the [Ren'Py Tutorial](https://renpy.org/doc/html/quickstart.html) first
- **Want to see examples?** Check out the included demo room
- **Need help?** Visit the [GitLab Discussions](../../-/issues) 
- **Found a bug?** Report it in [GitLab Issues](../../-/issues)

## 🎯 Framework Overview

The Snatchernauts Framework provides:

### 🏠 **Room Exploration**
Point-and-click interface with intelligent hover descriptions and smart positioning

### 🎮 **Input Systems** 
Seamless mouse and gamepad controls with D-pad navigation

### ✨ **Visual Effects**
GPU-accelerated bloom effects with customizable parameters and animations

### 🔧 **Development Tools**
Live editor mode for rapid prototyping and object positioning

### 📱 **Cross-Platform**
Works on Windows, Mac, Linux, and Android with consistent behavior

## 🎨 Use Cases

Perfect for creating:
- Detective/mystery games with investigation mechanics
- Point-and-click adventures with rich environments  
- Educational games with interactive elements
- Art gallery experiences with detailed descriptions
- Visual novels with exploration segments

## 🌟 Key Features

| Feature | Description |
|---------|-------------|
| **Modular Architecture** | Clean, organized code structure |
| **Smart Positioning** | Automatic description box placement |
| **Persistent State** | Object positions saved across sessions |
| **Pixel-Perfect Fonts** | Crisp text rendering with Quaver font |
| **Gamepad Navigation** | Full controller support |
| **Visual Effects** | Dynamic bloom and animation systems |
| **Live Editing** | Real-time object manipulation |
| **Cross-Platform** | Consistent behavior across devices |

## 🏁 Next Steps

1. **Read the [Installation Guide](Installation-Guide)** to set up the framework
2. **Try the [Quick Start Tutorial](Quick-Start-Tutorial)** to create your first room
3. **Explore the [API Reference](Function-Reference)** for detailed documentation
4. **Join the community** in [GitLab Discussions](../../-/issues)

---

**Happy game development!** 🎮✨

*The Snatchernauts Framework team*

---

### Step 3: Create Installation Guide Page
1. Click **New page** in wiki
2. Title: `Installation-Guide`
3. Copy the content below:

---

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
   git clone https://gitlab.com/grahfmusic/snatchernauts_framework.git
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
   - Visit the [GitLab Releases page](../../-/releases)
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
4. **Join the [GitLab Discussions](../../-/issues)** to connect with other developers

## 📞 Getting Help

If you encounter issues:

1. **Check the [Troubleshooting](#-troubleshooting)** section above
2. **Search [existing issues](../../-/issues)** for solutions
3. **Create a new issue** with detailed information:
   - Operating system and version
   - Ren'Py version  
   - Error messages and log files
   - Steps to reproduce the problem

---

**Installation complete!** 🎉 You're ready to start building amazing point-and-click adventures!

[← Back to Wiki Home](Home) | [Quick Start Tutorial →](Quick-Start-Tutorial)

---

### Step 4: Add More Wiki Pages
Create additional pages as needed using the same process. Some suggested pages to start with:

- **Quick-Start-Tutorial** - Step-by-step first room creation
- **Room-System** - Detailed room management documentation
- **Object-System** - Interactive objects and configuration
- **Visual-Effects** - Bloom effects and animation system
- **API-Reference** - Function and variable documentation

## 🔄 Alternative: Wiki Git Repository

If you prefer to manage the wiki with Git (advanced):

1. Clone the wiki repository:
   ```bash
   git clone https://gitlab.com/grahfmusic/snatchernauts_framework.wiki.git
   ```

2. Add your wiki files and push:
   ```bash
   cd snatchernauts_framework.wiki
   # Copy your wiki/*.md files here
   git add .
   git commit -m "Add comprehensive wiki documentation"
   git push origin main
   ```

This allows you to manage the wiki content with version control, but the manual method above is easier for most users.
