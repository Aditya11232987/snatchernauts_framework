# Room API Reference

## Overview

The Room API (`game/api/room_api.rpy`) is the central system for managing room-based gameplay in the Snatchernauts Framework. It handles room loading, object registration, navigation, and state management. This API provides the foundation for creating interactive environments where players can explore, interact with objects, and progress through your story.

## Core Responsibilities

### Room Lifecycle Management
- Load and unload rooms with proper state cleanup
- Maintain current room identification and context
- Handle room transitions and audio management
- Manage persistent room state across save/load cycles

### Object System
- Register interactive objects with their properties and behaviors
- Handle object positioning, scaling, and visual properties
- Manage object visibility and interaction state
- Support dynamic object creation and removal

### Navigation Support
- Provide keyboard and gamepad navigation between objects
- Handle focus management and selection state
- Support accessibility features and alternative input methods
- Calculate optimal navigation paths and object ordering

## Primary Functions

### Room Loading and Management

#### `load_room(room_id, music=None, fade_in=True)`

**Purpose**: Load a new room and set it as the current active room

**Parameters**:
- `room_id` (string): Identifier for the room to load
- `music` (string, optional): Background music file to play
- `fade_in` (boolean): Whether to use fade-in transition

**Example**:
```python
# Basic room loading
load_room("detective_office")

# Load room with specific music
load_room("crime_scene", music="audio/tension_theme.ogg")

# Load room without fade transition
load_room("flashback_room", fade_in=False)
```

**Side Effects**:
- Sets `store.current_room_id` to the new room
- Loads room configuration from `ROOM_DEFINITIONS`
- Triggers `on_room_enter()` hook after loading
- Starts background music if specified
- Clears previous room state and objects

#### `get_current_room()`

**Purpose**: Get the identifier of the currently active room

**Returns**: String identifier of current room, or `None` if no room loaded

**Example**:
```python
current = get_current_room()
if current == "detective_office":
    # Room-specific logic
    show_evidence_board()
```

#### `play_room_audio(room_id, audio_type="ambient")`

**Purpose**: Start audio associated with a specific room

**Parameters**:
- `room_id` (string): Room identifier
- `audio_type` (string): Type of audio ("ambient", "music", "tension")

**Example**:
```python
# Play ambient sound for current room
play_room_audio("detective_office", "ambient")

# Switch to tension music during investigation
play_room_audio("detective_office", "tension")
```

### Object Registration and Management

#### `add_room_object(room_id, object_name, config)`

**Purpose**: Add a new interactive object to a room

**Parameters**:
- `room_id` (string): Target room identifier
- `object_name` (string): Unique object identifier within the room
- `config` (dict): Object configuration dictionary

**Configuration Properties**:
```python
config = {
    "image": "path/to/image.png",      # Required: object image file
    "position": (x, y),               # Required: screen position
    "actions": ["Examine", "Take"],   # Available player actions
    "scale_percent": 100,             # Size scaling (100 = original)
    "visible": True,                  # Initial visibility state
    "description": "A wooden desk",   # Hover description text
    "z_order": 10,                    # Display layering priority
    
    # Desaturation highlighting settings
    "desaturation_intensity": 0.5,
    "desaturation_preset": "moderate",
    
    # Advanced properties
    "interactive": True,              # Can be clicked/selected
    "hover_enabled": True,            # Shows hover effects
    "focus_mask": "path/to/mask.png"  # Custom interaction area
}
```

**Example**:
```python
# Add a simple interactive object
add_room_object("office", "desk", {
    "image": "furniture/desk.png",
    "position": (400, 300),
    "actions": ["Examine", "Search"],
    "description": "A cluttered detective's desk"
})

# Add object with special highlighting
add_room_object("office", "evidence", {
    "image": "items/evidence_box.png",
    "position": (600, 250),
    "actions": ["Examine", "Take"],
    "description": "Box of case evidence",
    "desaturation_preset": "explosive_intense",
    "z_order": 15
})
```

#### `remove_room_object(room_id, object_name)`

**Purpose**: Remove an object from a room

**Parameters**:
- `room_id` (string): Room containing the object
- `object_name` (string): Object to remove

**Example**:
```python
# Remove object after player takes it
def on_object_interact(room_id, obj, action):
    if obj == "key" and action == "Take":
        store.inventory.append("office_key")
        remove_room_object(room_id, "key")
        renpy.say(None, "You pick up the key.")
        return True
```

#### `get_room_objects(room_id=None)`

**Purpose**: Get list of all objects in a room

**Parameters**:
- `room_id` (string, optional): Room to query (defaults to current room)

**Returns**: Dictionary of object configurations

**Example**:
```python
# Check all objects in current room
objects = get_room_objects()
for obj_name, obj_config in objects.items():
    print(f"Object {obj_name} at {obj_config['position']}")

# Count interactive objects
interactive_count = sum(1 for obj in objects.values() 
                       if obj.get('interactive', True))
```

### Object Manipulation

#### `move_object(object_name, dx, dy)`

**Purpose**: Move an object by a relative offset

**Parameters**:
- `object_name` (string): Object to move
- `dx` (int): Horizontal movement in pixels
- `dy` (int): Vertical movement in pixels

**Example**:
```python
# Animate object falling
move_object("vase", 0, 100)  # Move down 100 pixels

# Shake effect
for i in range(3):
    move_object("desk", 5, 0)
    renpy.pause(0.1)
    move_object("desk", -5, 0)
    renpy.pause(0.1)
```

#### `scale_object(object_name, scale_change)`

**Purpose**: Change an object's size

**Parameters**:
- `object_name` (string): Object to scale
- `scale_change` (float): Scale multiplier (1.0 = no change)

**Example**:
```python
# Make object larger to show importance
scale_object("evidence", 1.2)  # 20% larger

# Shrink object as it's taken
scale_object("coin", 0.5)  # 50% of original size
```

### Navigation and Selection

#### `get_object_list_for_navigation()`

**Purpose**: Get ordered list of objects for keyboard/gamepad navigation

**Returns**: List of object names in navigation order

**Example**:
```python
# Get navigation order
nav_objects = get_object_list_for_navigation()
print(f"Navigation order: {nav_objects}")

# Check if specific object is navigable
if "secret_panel" in nav_objects:
    renpy.notify("Hidden object discovered!")
```

#### `find_nearest_object(current_obj, direction)`

**Purpose**: Find the nearest object in a given direction for navigation

**Parameters**:
- `current_obj` (string): Currently selected object
- `direction` (string): Direction to search ("up", "down", "left", "right")

**Returns**: Name of nearest object, or `None` if no object found

**Example**:
```python
# Implement custom navigation logic
def custom_navigate(direction):
    current = store.gamepad_selected_object
    next_obj = find_nearest_object(current, direction)
    if next_obj:
        store.gamepad_selected_object = next_obj
        handle_object_hover(next_obj)
```

#### `gamepad_navigate(direction)`

**Purpose**: Handle gamepad/keyboard navigation between objects

**Parameters**:
- `direction` (string): Navigation direction

**Example**:
```python
# Navigation key bindings
key "K_UP" action Function(gamepad_navigate, "up")
key "K_DOWN" action Function(gamepad_navigate, "down")
key "K_LEFT" action Function(gamepad_navigate, "left")
key "K_RIGHT" action Function(gamepad_navigate, "right")
```

#### `gamepad_select_first_object()`

**Purpose**: Select the first navigable object in the room

**Example**:
```python
# Auto-select first object when entering room
def on_room_enter(room_id):
    gamepad_select_first_object()
    renpy.notify("Use arrow keys to navigate")
```

### State Management

#### `save_room_changes(room_id=None)`

**Purpose**: Persist current room state for save/load functionality

**Parameters**:
- `room_id` (string, optional): Room to save (defaults to current)

**Example**:
```python
# Save room state after significant changes
def on_object_interact(room_id, obj, action):
    if obj == "switch" and action == "Use":
        # Toggle lights
        store.office_lights_on = not store.office_lights_on
        update_room_lighting()
        save_room_changes()
        return True
```

#### `reset_room_changes(room_id=None)`

**Purpose**: Reset room to its initial state

**Parameters**:
- `room_id` (string, optional): Room to reset (defaults to current)

**Example**:
```python
# Reset room for new game+
def reset_chapter():
    for room in ["office", "crime_scene", "lab"]:
        reset_room_changes(room)
```

### Visual Effects Integration

#### `toggle_crt_effect()`

**Purpose**: Enable/disable CRT shader effect

**Example**:
```python
# Toggle CRT for retro feel
key "c" action Function(toggle_crt_effect)

# Enable CRT for specific scenes
def on_room_enter(room_id):
    if room_id == "computer_room":
        store.crt_enabled = True
    else:
        store.crt_enabled = False
```

#### `set_crt_parameters(warp=None, scan=None, chroma=None, vignette_strength=None, vignette_width=None)`

**Purpose**: Configure CRT effect parameters

**Parameters**: All optional, `None` means no change
- `warp` (float): Screen curvature (0.0-0.5)
- `scan` (float): Scanline intensity (0.0-1.0)
- `chroma` (float): Color separation (0.0-0.01)
- `vignette_strength` (float): Edge darkening (0.0-1.0)
- `vignette_width` (float): Vignette size (0.5-1.0)

**Example**:
```python
# Subtle CRT effect for dialogue
set_crt_parameters(warp=0.05, scan=0.1, chroma=0.001)

# Strong retro effect for flashback
set_crt_parameters(warp=0.15, scan=0.25, chroma=0.005)
```

## Room Configuration System

### Room Definition Structure

Rooms are defined in `ROOM_DEFINITIONS` dictionaries:

```python
ROOM_DEFINITIONS = {
    "detective_office": {
        "background": "images/backgrounds/office.png",
        "objects": {
            "desk": {
                "image": "images/furniture/desk.png",
                "position": (400, 300),
                "actions": ["Examine", "Search"]
            },
            "filing_cabinet": {
                "image": "images/furniture/cabinet.png",
                "position": (700, 280),
                "actions": ["Examine", "Open"],
                "description": "A locked filing cabinet"
            }
        },
        "audio": {
            "ambient": "audio/office_ambient.ogg",
            "tension": "audio/tension_music.ogg"
        },
        "effects": {
            "crt_enabled": False,
            "letterbox_enabled": False,
            "color_grade": "detective_office"
        }
    }
}
```

### Dynamic Room Creation

```python
# Create room at runtime
def create_new_room(room_id, background_image, objects=None):
    room_config = {
        "background": background_image,
        "objects": objects or {},
        "audio": {},
        "effects": {}
    }
    
    # Add to global definitions
    store.ROOM_DEFINITIONS[room_id] = room_config
    
    # Load immediately if needed
    if should_load_now:
        load_room(room_id)
```

## Error Handling and Validation

### Common Error Scenarios

```python
# Robust object interaction
def on_object_interact(room_id, obj, action):
    try:
        # Check if object exists
        objects = get_room_objects(room_id)
        if obj not in objects:
            print(f"[ERROR] Object {obj} not found in {room_id}")
            return False
        
        # Check if action is valid
        valid_actions = objects[obj].get('actions', [])
        if action not in valid_actions:
            print(f"[ERROR] Action {action} not valid for {obj}")
            return False
        
        # Perform action
        return handle_specific_interaction(room_id, obj, action)
        
    except Exception as e:
        print(f"[ERROR] Interaction failed: {e}")
        return False
```

### Validation Helpers

```python
def validate_room_config(room_id, config):
    """Validate room configuration before loading"""
    required_keys = ["background"]
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Room {room_id} missing required key: {key}")
    
    # Validate object configurations
    objects = config.get("objects", {})
    for obj_name, obj_config in objects.items():
        if "image" not in obj_config:
            raise ValueError(f"Object {obj_name} missing image")
        if "position" not in obj_config:
            raise ValueError(f"Object {obj_name} missing position")
```

## Performance Considerations

### Memory Management
- Large rooms with many objects can consume significant memory
- Consider lazy loading of object images
- Unload unused rooms during long gameplay sessions

```python
# Memory-conscious room loading
def smart_load_room(room_id):
    # Unload previous room if memory usage is high
    if get_memory_usage() > MEMORY_THRESHOLD:
        unload_previous_rooms()
    
    # Load new room
    load_room(room_id)
```

### Navigation Performance
- Navigation calculations are cached for performance
- Large numbers of objects (>50) may impact navigation speed
- Consider grouping objects or using navigation hints

## Best Practices

### Room Naming Conventions
- Use descriptive, consistent names: `detective_office`, `crime_scene`, `lab`
- Avoid spaces and special characters
- Use underscores for multi-word names
- Keep names short but meaningful

### Object Organization
- Group related objects logically
- Use consistent action names across objects
- Provide meaningful descriptions for all interactive objects
- Consider navigation flow when positioning objects

### State Management
- Save room state after significant changes
- Use persistent storage for progress that should survive save/load
- Reset temporary states when appropriate
- Handle edge cases gracefully

## Integration Examples

### Complete Room Setup

```python
# Complete example of setting up a new room
def setup_investigation_room():
    # Define room configuration
    room_config = {
        "background": "images/investigation_room.png",
        "objects": {
            "evidence_board": {
                "image": "images/evidence_board.png",
                "position": (200, 100),
                "actions": ["Examine", "Update"],
                "description": "Board with case evidence",
                "desaturation_preset": "explosive_normal"
            },
            "suspect_photos": {
                "image": "images/photos.png",
                "position": (500, 150),
                "actions": ["Examine", "Analyze"],
                "description": "Photographs of suspects",
                "visible": False  # Hidden until discovered
            },
            "computer": {
                "image": "images/computer.png",
                "position": (600, 300),
                "actions": ["Use", "Search"],
                "description": "Police database terminal"
            }
        },
        "audio": {
            "ambient": "audio/investigation_ambient.ogg",
            "tension": "audio/discovery_theme.ogg"
        },
        "effects": {
            "color_grade": "detective_office",
            "lighting": "desk_lamp"
        }
    }
    
    # Register room
    store.ROOM_DEFINITIONS["investigation_room"] = room_config
    
    # Set up room-specific logic
    class InvestigationLogic:
        def on_room_enter(self, room_id):
            renpy.music.play("audio/investigation_ambient.ogg", channel="ambient")
            if store.case_progress >= 3:
                # Reveal hidden photos
                show_object("suspect_photos")
        
        def on_object_interact(self, room_id, obj, action):
            if obj == "evidence_board" and action == "Update":
                if len(store.evidence_collected) >= 5:
                    renpy.call("evidence_breakthrough_scene")
                else:
                    renpy.say(None, "You need more evidence first.")
                return True
            return False
    
    # Register logic handler
    register_room_logic("investigation_room", InvestigationLogic())
```

This comprehensive Room API provides all the tools needed to create rich, interactive environments in your visual novel while maintaining clean separation between presentation and logic.

