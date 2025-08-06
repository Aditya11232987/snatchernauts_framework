# Snatchernauts Framework

A comprehensive Ren'Py point-and-click adventure game framework inspired by classic detective games like *Snatcher*. Build immersive room exploration games with stunning visual effects, gamepad support, and pixel-perfect rendering.

## 🌟 Features

### Core Systems
- **🏠 Room Exploration System** - Point-and-click interface with hover descriptions
- **🎮 Gamepad Support** - Full controller navigation with D-pad and analog sticks  
- **✨ Advanced Visual Effects** - Dynamic bloom effects and hover animations
- **📺 CRT Shader Effects** - Authentic retro CRT monitor simulation with scanlines
- **📝 Floating Descriptions** - Smart auto-positioning description boxes
- **🔧 Live Editor Mode** - In-game object positioning and scaling tools
- **🎨 Pixel-Perfect Rendering** - Optimized for pixel art with the Quaver font

### Technical Highlights
- **Modular Architecture** - Organized, reusable code components
- **Persistent State Management** - Save object positions across sessions
- **Dynamic Configuration** - JSON-like object definitions with inheritance
- **Bloom Shader System** - GPU-accelerated glow effects
- **Smart Box Positioning** - Automatic description placement with collision detection
- **Cross-Platform Input** - Seamless mouse and gamepad integration

## 🚀 Quick Start

### Prerequisites
- Ren'Py 8.3.7+ SDK
- Quaver pixel font (included)
- Basic knowledge of Ren'Py scripting

### Installation

1. Clone the repository:
```bash
git clone https://gitlab.com/yourusername/snatchernauts_framework.git
cd snatchernauts_framework
```

2. Open in Ren'Py:
```bash
/path/to/renpy/renpy.sh .
```

3. Run the demo:
- Click "Launch Project" in Ren'Py Launcher
- Navigate with mouse or gamepad
- Press F1 to enable Editor Mode

## 📖 Documentation

### Basic Usage

#### Adding Objects to Rooms

Edit `game/room_config.rpy` to add new interactive objects:

```python
"my_object": merge_configs({
    # Basic properties
    "x": 100, "y": 200,
    "scale_percent": 100,
    "width": 200, "height": 150,
    "image": "images/my_object.png",
    "description": "A mysterious object that catches your eye.",
    "box_position": "top+20",
    "object_type": "item",
}, 
# Custom bloom effects
create_bloom_config({
    "bloom_intensity": 0.8,
    "bloom_radius": 10.0,
}),
# Custom animations
create_animation_config({
    "hover_scale_boost": 1.05,
}))
```

#### Creating New Rooms

Add new rooms to the `ROOM_DEFINITIONS` dictionary:

```python
"room2": {
    "background": "images/room2.png",
    "objects": {
        # Define room objects here
    }
}
```

#### Description Box Positioning

Control where description boxes appear:
- `"auto"` - Smart auto-positioning (default)
- `"top+30"` - Above object with 30px margin
- `"right+50"` - Right of object with 50px margin  
- `"left+25"` - Left of object with 25px margin
- `"bottom+40"` - Below object with 40px margin

### Advanced Features

#### Bloom Effects

Customize glowing effects for objects:

```python
create_bloom_config({
    "bloom_intensity": 0.6,        # Glow strength (0.0-1.0)
    "bloom_radius": 8.0,           # Glow spread radius
    "bloom_threshold": 0.03,       # Brightness threshold
    "bloom_softness": 0.9,         # Edge softness (0.0-1.0)
    "bloom_alpha_min": 0.2,        # Minimum glow opacity
    "bloom_alpha_max": 0.8,        # Maximum glow opacity
    "bloom_pulse_speed": 1.0       # Pulsing animation speed
})
```

#### CRT Shader Effects

Authentic retro CRT monitor simulation with customizable parameters:

**Keyboard Controls:**
- **C** - Toggle CRT effect on/off
- **1** - Fine scanlines (0.5)
- **2** - Normal scanlines (1.0) - Default
- **3** - Thick scanlines (1.5)
- **4** - Very thick scanlines (3.0)

**Features:**
- **Resolution-independent scanlines** - Consistent appearance across window sizes
- **Barrel distortion (warp)** - Authentic CRT curvature effect
- **Chromatic aberration** - Color separation for retro authenticity
- **Adjustable scanline thickness** - Four preset intensity levels
- **Enabled by default** - Starts with optimal scanline settings

#### Animation System

Configure hover animations:

```python
create_animation_config({
    "hover_animation_type": "breathe",  # "breathe", "breath", or "pulse"
    "hover_scale_boost": 1.02,          # Scale multiplier on hover
    "hover_brightness_boost": 0.1       # Brightness increase on hover
})
```

#### Editor Mode

Enable live editing with F1 or the "Editor Mode" button:
- **Arrow Keys** - Move selected object
- **+/-** - Scale object up/down
- **R** - Reset object to 100% scale
- **S** - Save changes to persistent storage
- **U** - Update room_config.rpy file
- **Tab** - Cycle through objects

### Keyboard Controls

**General Navigation:**
- **C** - Toggle CRT effect on/off
- **F** - Fade out room audio
- **R** - Refresh/restart interaction
- **F1** - Toggle Editor Mode

**CRT Scanline Controls:**
- **1** - Fine scanlines (0.5)
- **2** - Normal scanlines (1.0) - Default
- **3** - Thick scanlines (1.5)
- **4** - Very thick scanlines (3.0)

**Editor Mode (when enabled):**
- **Arrow Keys** - Move selected object
- **+/-** - Scale object up/down
- **R** - Reset object to 100% scale
- **S** - Save changes to persistent storage
- **U** - Update room_config.rpy file
- **Tab** - Cycle through objects

### Gamepad Controls

- **D-Pad/Left Stick** - Navigate between objects
- **A Button** - Select first object (if none selected)
- **Back/Select** - Toggle gamepad navigation on/off

## 🎨 Asset Guidelines

### Images
- **Room Backgrounds**: 1280x720 PNG files
- **Objects**: PNG with transparency, any size
- **Pixel Art**: Use multiples of 8 pixels for crisp rendering

### Fonts  
- Primary font: Quaver (pixel font, included)
- UI sizes: 8, 16, 24, 32, 40, 48 pixels
- Renders pixel-perfect at intended sizes

## 🗂️ Project Structure

```
game/
├── room_config.rpy          # Main room and object definitions
├── room_main.rpy           # Core room exploration screen
├── room_functions.rpy      # Room management functions
├── room_ui.rpy            # UI buttons and controls  
├── room_descriptions.rpy   # Description box system
├── room_display.rpy        # Object rendering system
├── room_editor.rpy         # Live editing tools
├── bloom_shader.rpy        # Visual effects shaders
├── font_config.rpy         # Font configuration
├── common_utils.rpy        # Shared utility functions
└── images/
    ├── room1.png          # Room background
    ├── detective.png      # Example object
    └── patreon.png       # Example object
```

## 🔧 Configuration

### Global Settings

Modify `game/room_config.rpy` for global behavior:

```python
# Gamepad navigation (default: enabled)
default gamepad_navigation_enabled = True

# Editor mode settings
default move_speed = 5  # Pixels per keypress
default show_editor_help = True

# Room interaction
default current_room_id = "room1"
```

### Bloom Color System

Customize per-object bloom colors in `game/bloom_colors.rpy`:

```python
BLOOM_COLORS = {
    "detective": "#733939",    # Dark red glow
    "patreon": "#FF6B35",      # Orange glow  
    "default": "#FFFFFF"       # White glow fallback
}
```

## 🎯 Use Cases

Perfect for creating:
- **Detective/Mystery Games** - Investigate crime scenes and gather clues
- **Point-and-Click Adventures** - Explore environments and solve puzzles
- **Visual Novels with Exploration** - Add interactive exploration to story scenes
- **Educational Games** - Create interactive learning environments
- **Art Gallery Experiences** - Showcase artwork with detailed descriptions

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable  
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a merge request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ren'Py Team** - For the excellent visual novel engine
- **Snatcher** - Inspiration for the detective game aesthetic  
- **Quaver Font** - Perfect pixel font for retro games
- **Community Contributors** - Thanks to everyone who helps improve the framework

## 🆘 Support

- **Documentation**: Check the [Wiki](../../wiki) for detailed guides
- **Issues**: Report bugs via [GitLab Issues](../../issues)
- **Discussions**: Ask questions in [GitLab Discussions](../../discussions)

---

**Made with ❤️ for the Ren'Py community**

*Build your dream point-and-click adventure with Snatchernauts Framework!*
