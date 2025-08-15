# Display and Effects API Reference

## Overview

The Display API (`game/api/display_api.rpy`) manages visual effects and display properties in the Snatchernauts Framework. This API provides centralized control over cinematic effects, object visibility, background management, and visual state coordination across different game systems.

## Core Responsibilities

### Visual Effects Management
- Control CRT shader effects with real-time parameter adjustment
- Manage letterbox overlay for cinematic scenes
- Coordinate bloom and desaturation effects for object highlighting
- Handle color grading and atmospheric lighting transitions

### Display State Control
- Manage object visibility and rendering state
- Handle background image management and transitions
- Coordinate shader effect combinations and layering
- Provide fallback rendering for unsupported platforms

### Integration Coordination
- Bridge between room system and visual effects
- Coordinate with audio system for synchronized audio-visual effects
- Manage effect persistence across room transitions
- Handle save/load state for visual preferences

## Primary Functions

### Background and Scene Management

#### `get_room_background(room_id=None)`

**Purpose**: Get the background image for a specific room

**Parameters**:
- `room_id` (string, optional): Room identifier (defaults to current room)

**Returns**: String path to background image, or `None` if not found

**Example**:
```python
# Get current room background
current_bg = get_room_background()
if current_bg:
    renpy.show("background", what=current_bg)

# Get specific room background
office_bg = get_room_background("detective_office")
```

#### `get_fallback_background()`

**Purpose**: Get the default fallback background for error states

**Returns**: String path to fallback background image

**Example**:
```python
# Use fallback if room background is missing
bg = get_room_background(room_id) or get_fallback_background()
renpy.scene(bg)
```

#### `set_fallback_background_color(color)`

**Purpose**: Set the default background color for scenes without backgrounds

**Parameters**:
- `color` (string): Color value (hex code or named color)

**Example**:
```python
# Set dark background for noir scenes
set_fallback_background_color("#1a1a1a")

# Set blue background for tech scenes
set_fallback_background_color("#001133")
```

#### `set_default_background(image_path)`

**Purpose**: Set the default background image to use when no room-specific background is available

**Parameters**:
- `image_path` (string): Path to default background image

**Example**:
```python
# Set generic detective office as default
set_default_background("images/backgrounds/generic_office.png")
```

### Object Visibility Control

#### `should_display_object(obj_config, obj_name=None)`

**Purpose**: Check if an object should be rendered based on its configuration and game state

**Parameters**:
- `obj_config` (dict): Object configuration dictionary
- `obj_name` (string, optional): Object name for debugging

**Returns**: Boolean indicating if object should be displayed

**Example**:
```python
# Check if object should be shown
obj = get_room_objects()["desk"]
if should_display_object(obj, "desk"):
    renpy.show("desk", at_list=[obj["position"]])

# Conditional display based on story progress
def update_room_objects():
    objects = get_room_objects()
    for obj_name, obj_config in objects.items():
        if should_display_object(obj_config, obj_name):
            show_object(obj_name)
        else:
            hide_object(obj_name)
```

#### `hide_object(obj_name)`

**Purpose**: Hide a specific object from display

**Parameters**:
- `obj_name` (string): Name of object to hide

**Example**:
```python
# Hide object after player takes it
def on_object_interact(room_id, obj, action):
    if obj == "key" and action == "Take":
        store.inventory.append("office_key")
        hide_object("key")
        return True

# Hide objects based on story state
if store.lights_off:
    hide_object("light_switch_on")
    show_object("light_switch_off")
```

#### `show_object(obj_name)`

**Purpose**: Show a previously hidden object

**Parameters**:
- `obj_name` (string): Name of object to show

**Example**:
```python
# Show object when conditions are met
if store.case_progress >= 3:
    show_object("evidence_board")
    renpy.notify("New evidence board available!")

# Show objects dynamically
def reveal_hidden_objects():
    hidden_objects = ["secret_panel", "hidden_safe", "concealed_door"]
    for obj in hidden_objects:
        if obj in store.discovered_secrets:
            show_object(obj)
```

#### `is_object_hidden(obj_name)`

**Purpose**: Check if an object is currently hidden

**Parameters**:
- `obj_name` (string): Name of object to check

**Returns**: Boolean indicating if object is hidden

**Example**:
```python
# Check visibility before interactions
if not is_object_hidden("secret_panel"):
    renpy.say(None, "You notice something unusual about the wall panel.")

# Conditional descriptions
def get_room_description():
    desc = "You're in the detective's office."
    if not is_object_hidden("evidence_board"):
        desc += " An evidence board covers one wall."
    return desc
```

### Visual Effects Control

#### `show_letterbox(enabled, duration=0.5)`

**Purpose**: Enable or disable cinematic letterbox effect

**Parameters**:
- `enabled` (boolean): Whether to show letterbox bars
- `duration` (float, optional): Animation duration in seconds

**Example**:
```python
# Enable letterbox for dramatic dialogue
def start_dramatic_scene():
    show_letterbox(True, duration=1.0)
    renpy.pause(1.0)
    detective "This changes everything..."

# Disable letterbox after scene
def end_dramatic_scene():
    show_letterbox(False, duration=0.5)
    renpy.pause(0.5)
```

#### `toggle_letterbox()`

**Purpose**: Toggle letterbox effect on/off

**Example**:
```python
# Keyboard shortcut for letterbox
key "l" action Function(toggle_letterbox)

# Toggle during gameplay
def on_object_interact(room_id, obj, action):
    if obj == "tv" and action == "Watch":
        toggle_letterbox()  # Enable cinematic mode
        renpy.call("tv_scene")
        toggle_letterbox()  # Disable after scene
        return True
```

### CRT Shader Effects

#### `toggle_crt_effect()`

**Purpose**: Enable/disable CRT shader effect

**Example**:
```python
# Keyboard shortcut
key "c" action Function(toggle_crt_effect)

# Context-sensitive CRT
def on_room_enter(room_id):
    if room_id in ["computer_room", "security_office"]:
        store.crt_enabled = True
    else:
        store.crt_enabled = False
```

#### `set_crt_parameters(warp=None, scanlines=None, chroma=None, vignette_strength=None, vignette_width=None, animated=None)`

**Purpose**: Configure CRT effect parameters

**Parameters**: All optional, `None` means no change
- `warp` (float): Screen curvature intensity (0.0-0.5)
- `scanlines` (float): Scanline visibility (0.0-1.0)
- `chroma` (float): Chromatic aberration amount (0.0-0.01)
- `vignette_strength` (float): Edge darkening (0.0-1.0)
- `vignette_width` (float): Vignette area (0.5-1.0)
- `animated` (boolean): Enable scanline animation

**Example**:
```python
# Subtle CRT for dialogue scenes
set_crt_parameters(
    warp=0.05,
    scanlines=0.1,
    chroma=0.002,
    animated=False
)

# Strong retro effect for flashbacks
set_crt_parameters(
    warp=0.15,
    scanlines=0.3,
    chroma=0.006,
    vignette_strength=0.6,
    animated=True
)

# Dynamic adjustment based on scene
def adjust_crt_for_scene(scene_type):
    if scene_type == "flashback":
        set_crt_parameters(warp=0.12, scanlines=0.25, animated=True)
    elif scene_type == "computer":
        set_crt_parameters(warp=0.08, scanlines=0.4, chroma=0.004)
    elif scene_type == "normal":
        set_crt_parameters(warp=0.05, scanlines=0.15, animated=False)
```

#### `reset_crt_parameters()`

**Purpose**: Reset CRT parameters to default values

**Example**:
```python
# Reset after special effect
def end_flashback_sequence():
    reset_crt_parameters()
    set_color_grade("normal")

# Keyboard shortcut for reset
key "0" action Function(reset_crt_parameters)
```

### Bloom and Highlighting Effects

#### `get_object_display_properties(obj_config, obj_name=None)`

**Purpose**: Get computed display properties for an object including effects

**Parameters**:
- `obj_config` (dict): Object configuration
- `obj_name` (string, optional): Object name for debugging

**Returns**: Dictionary of display properties

**Example**:
```python
# Get object display properties
obj = get_room_objects()["evidence"]
props = get_object_display_properties(obj, "evidence")

# Apply properties to display
renpy.show("evidence", at_list=[
    Transform(
        pos=props["position"],
        zoom=props["scale"],
        alpha=props["alpha"]
    )
])
```

#### `bloom_fade_in(room_id=None, duration=1.0)`

**Purpose**: Perform a bloom fade-in effect for room transition

**Parameters**:
- `room_id` (string, optional): Target room (defaults to current)
- `duration` (float): Fade duration in seconds

**Example**:
```python
# Smooth transition between rooms
def transition_to_room(new_room):
    bloom_fade_out(duration=0.5)
    renpy.pause(0.5)
    load_room(new_room)
    bloom_fade_in(duration=0.5)
```

#### `bloom_fade_out(duration=1.0)`

**Purpose**: Perform a bloom fade-out effect

**Parameters**:
- `duration` (float): Fade duration in seconds

**Example**:
```python
# Fade out before major scene change
def start_revelation_scene():
    bloom_fade_out(duration=2.0)
    renpy.pause(2.0)
    renpy.scene("black")
    renpy.say(None, "Everything went white...")
```

### Color Grading and Atmosphere

#### `set_color_grade(preset_name)`

**Purpose**: Apply a color grading preset to the entire scene

**Parameters**:
- `preset_name` (string): Name of color grading preset

**Available Presets**:
- `"normal"` - Default color balance
- `"noir"` - High contrast black and white
- `"sepia"` - Warm vintage tones
- `"cool"` - Blue-tinted cool atmosphere
- `"warm"` - Orange-tinted warm atmosphere
- `"desaturated"` - Muted colors
- `"crime_scene"` - High contrast with red emphasis
- `"detective_office"` - Vintage investigation feel

**Example**:
```python
# Set mood based on room
def on_room_enter(room_id):
    if room_id == "crime_scene":
        set_color_grade("noir")
    elif room_id == "flashback_room":
        set_color_grade("sepia")
    else:
        set_color_grade("normal")

# Dynamic grading based on story events
def update_atmosphere():
    if store.case_solved:
        set_color_grade("warm")
    elif store.danger_level > 7:
        set_color_grade("crime_scene")
    else:
        set_color_grade("detective_office")
```

#### `get_current_color_grade()`

**Purpose**: Get the currently active color grading preset

**Returns**: String name of current preset

**Example**:
```python
# Save current state before temporary change
current_grade = get_current_color_grade()
set_color_grade("noir")
# ... dramatic scene ...
set_color_grade(current_grade)  # Restore
```

### Advanced Display Control

#### `get_object_main_color(obj_config)`

**Purpose**: Extract the dominant color from an object for effect coordination

**Parameters**:
- `obj_config` (dict): Object configuration

**Returns**: Color tuple (r, g, b) normalized to 0.0-1.0

**Example**:
```python
# Coordinate bloom color with object
obj = get_room_objects()["ruby"]
main_color = get_object_main_color(obj)

# Apply matching bloom effect
apply_colored_bloom(obj_name="ruby", color=main_color)
```

#### `create_gradient_background(color1, color2, direction="vertical")`

**Purpose**: Create a gradient background for special scenes

**Parameters**:
- `color1` (string): Starting color
- `color2` (string): Ending color
- `direction` (string): Gradient direction ("vertical", "horizontal")

**Returns**: Displayable object for use as background

**Example**:
```python
# Create atmospheric background for dream sequence
dream_bg = create_gradient_background("#000033", "#330066", "vertical")
renpy.scene(dream_bg)

# Sunset effect
sunset_bg = create_gradient_background("#ff6600", "#ffcc00", "horizontal")
renpy.show("sunset_overlay", what=sunset_bg, alpha=0.3)
```

## Effect Coordination and Presets

### Scene Preset System

```python
# Define scene presets for quick setup
SCENE_PRESETS = {
    "normal": {
        "color_grade": "normal",
        "crt_enabled": False,
        "letterbox_enabled": False,
        "bloom_intensity": 0.3
    },
    "noir_investigation": {
        "color_grade": "noir",
        "crt_enabled": True,
        "crt_scanlines": 0.2,
        "letterbox_enabled": True,
        "bloom_intensity": 0.5
    },
    "flashback": {
        "color_grade": "sepia",
        "crt_enabled": True,
        "crt_warp": 0.1,
        "crt_animated": True,
        "bloom_intensity": 0.4
    },
    "computer_terminal": {
        "color_grade": "cool",
        "crt_enabled": True,
        "crt_scanlines": 0.4,
        "crt_chroma": 0.005
    }
}

def apply_scene_preset(preset_name):
    """Apply a complete scene preset"""
    if preset_name not in SCENE_PRESETS:
        return False
    
    preset = SCENE_PRESETS[preset_name]
    
    # Apply color grading
    if "color_grade" in preset:
        set_color_grade(preset["color_grade"])
    
    # Configure CRT
    if preset.get("crt_enabled", False):
        store.crt_enabled = True
        set_crt_parameters(
            warp=preset.get("crt_warp"),
            scanlines=preset.get("crt_scanlines"),
            chroma=preset.get("crt_chroma"),
            animated=preset.get("crt_animated")
        )
    else:
        store.crt_enabled = False
    
    # Configure letterbox
    if preset.get("letterbox_enabled", False):
        show_letterbox(True)
    else:
        show_letterbox(False)
    
    return True
```

### Performance Optimization

#### `optimize_display_for_performance()`

**Purpose**: Reduce visual effects for better performance

**Example**:
```python
# Detect performance issues and optimize
def check_and_optimize_performance():
    if renpy.get_fps() < 30:  # Low framerate detected
        optimize_display_for_performance()
        renpy.notify("Performance mode enabled")

def optimize_display_for_performance():
    """Reduce effects for better performance"""
    store.crt_enabled = False
    store.bloom_quality = "low"
    store.film_grain_enabled = False
    
    # Use simpler color grading
    if get_current_color_grade() in ["noir", "crime_scene"]:
        set_color_grade("desaturated")
```

### Integration with Save/Load System

```python
# Save display preferences
def save_display_preferences():
    persistent.display_prefs = {
        "crt_enabled": store.crt_enabled,
        "crt_warp": getattr(store, "crt_warp", 0.12),
        "crt_scanlines": getattr(store, "crt_scanlines", 0.18),
        "letterbox_preferred": getattr(store, "letterbox_preferred", False),
        "color_grade_preference": get_current_color_grade()
    }

# Load display preferences
def load_display_preferences():
    if hasattr(persistent, "display_prefs") and persistent.display_prefs:
        prefs = persistent.display_prefs
        store.crt_enabled = prefs.get("crt_enabled", False)
        set_crt_parameters(
            warp=prefs.get("crt_warp"),
            scanlines=prefs.get("crt_scanlines")
        )
        if prefs.get("letterbox_preferred"):
            show_letterbox(True)
```

## Best Practices

### Effect Timing
- Use gradual transitions (0.5-2.0 seconds) for major visual changes
- Keep effect parameters consistent within scenes
- Reset effects between major story transitions

### Performance Considerations
- Monitor framerate when combining multiple effects
- Provide options to disable intensive effects
- Use simpler alternatives on mobile platforms

### Narrative Integration
- Match visual effects to story mood and themes
- Use effects to enhance rather than distract from narrative
- Maintain consistency within story arcs

The Display API provides comprehensive control over the visual presentation of your game while maintaining performance and narrative coherence.

