# Interactions API Reference

## Overview

The Interactions API (`game/api/interactions_api.rpy`) manages player interactions with objects in the game world. This system handles action menus, input processing, interaction routing, and coordination between the UI layer and game logic. It provides the core functionality that makes the framework's point-and-click exploration possible.

## Core Responsibilities

### Action Management
- Define available actions for each interactive object
- Manage context-sensitive action availability
- Handle action validation and prerequisites
- Coordinate between different interaction types (examine, use, talk, etc.)

### Menu Systems
- Present contextual interaction menus to players
- Handle menu navigation via mouse, keyboard, and gamepad
- Manage menu positioning and visual appearance
- Support dynamic menu content based on game state

### Logic Integration
- Route player actions to appropriate game logic handlers
- Manage the interaction flow between UI and logic layers
- Handle return values and continuation logic
- Provide fallback behaviors for unhandled interactions

### State Management
- Track current interaction state and selected objects
- Manage interaction history and context
- Handle interaction interruption and cancellation
- Coordinate with save/load systems for interaction persistence

## Primary Functions

### Core Interaction Processing

#### `execute_object_action(obj_name, action_id, source="mouse")`

**Purpose**: Execute a player action on a specific object

**Parameters**:
- `obj_name` (string): Name of the target object
- `action_id` (string): Action to perform (e.g., "Examine", "Use", "Talk")
- `source` (string, optional): Input source ("mouse", "keyboard", "gamepad")

**Returns**: Boolean indicating if the action was handled

**Example**:
```python
# Execute action from button click
textbutton "Examine" action Function(execute_object_action, "desk", "Examine")

# Execute action programmatically
if player_has_key:
    execute_object_action("door", "Unlock")

# Handle action result
handled = execute_object_action("computer", "Use")
if not handled:
    renpy.say(None, "You can't use that right now.")
```

**Execution Flow**:
1. Validates object exists and action is available
2. Calls `on_object_interact()` hook with parameters
3. If hook returns `True`, considers action handled
4. If hook returns `False`, executes default behavior
5. Updates interaction state and triggers side effects

#### `execute_selected_action()`

**Purpose**: Execute the currently selected action on the currently selected object

**Example**:
```python
# Keyboard binding for action execution
key "K_RETURN" action Function(execute_selected_action)
key "K_SPACE" action Function(execute_selected_action)

# Gamepad binding
key "joy_0" action Function(execute_selected_action)
```

#### `get_actions_for(obj_name)`

**Purpose**: Get list of available actions for a specific object

**Parameters**:
- `obj_name` (string): Name of the object

**Returns**: List of action strings

**Example**:
```python
# Get actions for menu display
actions = get_actions_for("desk")
for action in actions:
    textbutton action action Function(execute_object_action, "desk", action)

# Check if specific action is available
if "Search" in get_actions_for("filing_cabinet"):
    renpy.say(None, "You could search the filing cabinet.")

# Dynamic action availability
def get_contextual_actions(obj_name):
    base_actions = get_actions_for(obj_name)
    
    # Add inventory-based actions
    if "key" in store.inventory and obj_name == "door":
        base_actions.append("Unlock")
    
    # Add story-based actions
    if store.detective_present and obj_name == "evidence":
        base_actions.append("Discuss")
    
    return base_actions
```

### Menu Management

#### `show_interaction_menu(obj_name, position=None)`

**Purpose**: Display the interaction menu for a specific object

**Parameters**:
- `obj_name` (string): Object to show menu for
- `position` (tuple, optional): Screen position for menu (x, y)

**Example**:
```python
# Show menu at mouse position
show_interaction_menu("desk", position=renpy.get_mouse_pos())

# Show menu at object position
obj_config = get_room_objects()["desk"]
show_interaction_menu("desk", position=obj_config["position"])

# Show menu with automatic positioning
show_interaction_menu("desk")  # Uses smart positioning
```

#### `hide_interaction_menu()`

**Purpose**: Hide the currently displayed interaction menu

**Example**:
```python
# Hide menu on escape key
key "K_ESCAPE" action Function(hide_interaction_menu)

# Hide menu after action execution
def execute_and_hide(obj, action):
    execute_object_action(obj, action)
    hide_interaction_menu()

# Auto-hide menu after timeout
init python:
    def auto_hide_menu():
        renpy.timeout(3.0)
        hide_interaction_menu()
```

#### `navigate_interaction_menu(direction)`

**Purpose**: Navigate through interaction menu options using keyboard/gamepad

**Parameters**:
- `direction` (string): Navigation direction ("up", "down", "left", "right")

**Example**:
```python
# Navigation key bindings
key "K_UP" action Function(navigate_interaction_menu, "up")
key "K_DOWN" action Function(navigate_interaction_menu, "down")
key "K_LEFT" action Function(navigate_interaction_menu, "left")
key "K_RIGHT" action Function(navigate_interaction_menu, "right")

# Gamepad navigation
key "joy_hat_y" action Function(navigate_interaction_menu, "up")
key "joy_hat_-y" action Function(navigate_interaction_menu, "down")
```

### Specialized Action Handlers

The framework provides built-in handlers for common action types:

#### `handle_talk_action(obj_name, character=None)`

**Purpose**: Handle conversation initiation with characters

**Parameters**:
- `obj_name` (string): Object representing the character
- `character` (string, optional): Character identifier for dialogue system

**Example**:
```python
# Simple talk action
def on_object_interact(room_id, obj, action):
    if obj == "detective" and action == "Talk":
        handle_talk_action("detective", character="det_martinez")
        return True

# Complex conversation handling
def handle_talk_action(obj_name, character=None):
    if character == "det_martinez":
        if store.case_progress < 3:
            renpy.call("detective_intro_scene")
        elif store.evidence_collected:
            renpy.call("detective_evidence_scene")
        else:
            renpy.call("detective_default_scene")
```

#### `handle_examine_action(obj_name, description=None)`

**Purpose**: Handle object examination with contextual descriptions

**Parameters**:
- `obj_name` (string): Object to examine
- `description` (string, optional): Override description

**Example**:
```python
# Basic examination
def on_object_interact(room_id, obj, action):
    if action == "Examine":
        descriptions = {
            "desk": "A cluttered detective's desk with papers scattered about.",
            "window": "Rain streaks down the dirty glass.",
            "filing_cabinet": "A locked metal filing cabinet."
        }
        handle_examine_action(obj, descriptions.get(obj))
        return True

# Dynamic descriptions
def get_dynamic_description(obj_name):
    if obj_name == "desk":
        if store.desk_searched:
            return "The desk drawers are open and empty."
        else:
            return "A cluttered detective's desk. Something might be hidden here."
    return None
```

#### `handle_take_action(obj_name, item_id=None)`

**Purpose**: Handle item collection and inventory management

**Parameters**:
- `obj_name` (string): Object to take
- `item_id` (string, optional): Inventory item identifier

**Example**:
```python
def on_object_interact(room_id, obj, action):
    if action == "Take":
        if obj == "key":
            if handle_take_action("key", "office_key"):
                hide_object("key")  # Remove from room
                renpy.notify("Taken: Office Key")
            return True
        elif obj == "evidence":
            if len(store.inventory) < MAX_INVENTORY:
                handle_take_action("evidence", f"evidence_{len(store.evidence_collected)}")
                store.evidence_collected.append(obj)
                return True
            else:
                renpy.say(None, "Your inventory is full.")
                return True
    return False
```

#### `handle_use_action(obj_name, tool_item=None)`

**Purpose**: Handle using items on objects or using objects directly

**Parameters**:
- `obj_name` (string): Target object
- `tool_item` (string, optional): Item being used on the object

**Example**:
```python
def on_object_interact(room_id, obj, action):
    if action.startswith("Use "):
        tool = action[4:]  # Remove "Use " prefix
        return handle_use_action(obj, tool)
    elif action == "Use":
        return handle_use_action(obj)
    return False

def handle_use_action(obj_name, tool_item=None):
    if tool_item:
        # Using an item on an object
        if tool_item == "key" and obj_name == "door":
            renpy.say(None, "You unlock the door.")
            store.door_unlocked = True
            return True
        elif tool_item == "crowbar" and obj_name == "crate":
            renpy.say(None, "You pry open the crate.")
            show_object("crate_contents")
            return True
    else:
        # Using the object directly
        if obj_name == "computer":
            renpy.call_screen("computer_interface")
            return True
        elif obj_name == "phone":
            renpy.call("phone_menu")
            return True
    
    return False
```

### Advanced Interaction Features

#### `get_menu_base_position(obj_name)`

**Purpose**: Calculate optimal menu position for an object

**Parameters**:
- `obj_name` (string): Object to position menu for

**Returns**: Tuple (x, y) for menu positioning

**Example**:
```python
# Smart menu positioning
def show_smart_menu(obj_name):
    pos = get_menu_base_position(obj_name)
    
    # Adjust for screen boundaries
    screen_width, screen_height = renpy.get_physical_size()
    menu_width, menu_height = 200, 150
    
    x, y = pos
    if x + menu_width > screen_width:
        x = screen_width - menu_width
    if y + menu_height > screen_height:
        y = screen_height - menu_height
    
    show_interaction_menu(obj_name, position=(x, y))
```

#### `trigger_dialogue_scene(scene_label, character=None, **kwargs)`

**Purpose**: Start a dialogue scene with proper state management

**Parameters**:
- `scene_label` (string): Ren'Py label to call
- `character` (string, optional): Character identifier
- `**kwargs`: Additional parameters to pass to the scene

**Example**:
```python
# Trigger dialogue with context
def on_object_interact(room_id, obj, action):
    if obj == "witness" and action == "Talk":
        trigger_dialogue_scene(
            "witness_conversation",
            character="witness_mary",
            case_progress=store.case_progress,
            evidence_count=len(store.evidence_collected)
        )
        return True

# Scene with prerequisites
def try_start_confession_scene():
    if store.case_progress >= 8 and "smoking_gun" in store.evidence_collected:
        trigger_dialogue_scene("suspect_confession", character="main_suspect")
        return True
    else:
        renpy.say(None, "You need more evidence before confronting the suspect.")
        return False
```

### Input Method Support

#### Mouse Interaction

```python
# Mouse-based object interaction
screen room_objects():
    for obj_name, obj_config in get_room_objects().items():
        imagebutton:
            idle obj_config["image"]
            hover Transform(obj_config["image"], brightness=1.2)
            pos obj_config["position"]
            
            # Right-click for menu
            action Function(show_interaction_menu, obj_name)
            
            # Left-click for default action
            alternate Function(execute_default_action, obj_name)
            
            # Hover handling
            hovered Function(handle_object_hover, obj_name)
            unhovered Function(handle_object_unhover)
```

#### Keyboard Navigation

```python
# Keyboard interaction system
init python:
    def setup_keyboard_bindings():
        # Object navigation
        renpy.register_keymap("object_nav", {
            "K_TAB": "next_object",
            "K_TAB shift": "prev_object",
            "K_UP": "nav_up",
            "K_DOWN": "nav_down",
            "K_LEFT": "nav_left",
            "K_RIGHT": "nav_right"
        })
        
        # Action execution
        renpy.register_keymap("interaction", {
            "K_RETURN": "execute_action",
            "K_SPACE": "show_menu",
            "K_ESCAPE": "cancel_interaction"
        })
```

#### Gamepad Support

```python
# Gamepad interaction handling
def handle_gamepad_input(event_name):
    if event_name == "gamepad_activate":
        if store.gamepad_selected_object:
            show_interaction_menu(store.gamepad_selected_object)
    elif event_name == "gamepad_select":
        execute_selected_action()
    elif event_name == "gamepad_cancel":
        hide_interaction_menu()

# Gamepad navigation
def gamepad_navigate_objects(direction):
    current = store.gamepad_selected_object
    objects = get_object_list_for_navigation()
    
    if current in objects:
        current_index = objects.index(current)
        if direction == "next":
            new_index = (current_index + 1) % len(objects)
        else:
            new_index = (current_index - 1) % len(objects)
        
        store.gamepad_selected_object = objects[new_index]
        handle_object_hover(objects[new_index])
```

### Interaction State Management

```python
# Interaction state variables
default interaction_menu_active = False
default interaction_target_object = None
default interaction_selected_action = None
default interaction_history = []

# State management functions
def save_interaction_state():
    """Save current interaction state"""
    persistent.interaction_state = {
        "menu_active": store.interaction_menu_active,
        "target_object": store.interaction_target_object,
        "selected_action": store.interaction_selected_action,
        "history": store.interaction_history[-10:]  # Last 10 interactions
    }

def restore_interaction_state():
    """Restore saved interaction state"""
    if hasattr(persistent, "interaction_state") and persistent.interaction_state:
        state = persistent.interaction_state
        store.interaction_history = state.get("history", [])
        
        # Restore active menu if it was open
        if state.get("menu_active") and state.get("target_object"):
            show_interaction_menu(state["target_object"])

def log_interaction(obj_name, action, result):
    """Log interaction for history and debugging"""
    interaction_record = {
        "object": obj_name,
        "action": action,
        "result": result,
        "timestamp": renpy.get_game_runtime(),
        "room": get_current_room()
    }
    store.interaction_history.append(interaction_record)
    
    # Keep only recent history
    if len(store.interaction_history) > 50:
        store.interaction_history = store.interaction_history[-50:]
```

### Error Handling and Validation

```python
def validate_interaction(obj_name, action):
    """Validate interaction before execution"""
    # Check if object exists
    objects = get_room_objects()
    if obj_name not in objects:
        print(f"[ERROR] Object '{obj_name}' not found in current room")
        return False
    
    # Check if action is available
    available_actions = get_actions_for(obj_name)
    if action not in available_actions:
        print(f"[ERROR] Action '{action}' not available for object '{obj_name}'")
        return False
    
    # Check prerequisites
    obj_config = objects[obj_name]
    if obj_config.get("requires_item") and obj_config["requires_item"] not in store.inventory:
        renpy.say(None, f"You need {obj_config['requires_item']} to {action.lower()} this.")
        return False
    
    return True

def safe_execute_action(obj_name, action):
    """Execute action with error handling"""
    try:
        if not validate_interaction(obj_name, action):
            return False
        
        result = execute_object_action(obj_name, action)
        log_interaction(obj_name, action, result)
        return result
        
    except Exception as e:
        print(f"[ERROR] Interaction failed: {obj_name}.{action} - {e}")
        renpy.say(None, "Something went wrong with that interaction.")
        return False
```

## Integration with Other Systems

### Room System Integration

```python
# Update interactions when room changes
def on_room_enter(room_id):
    # Clear interaction state
    hide_interaction_menu()
    store.interaction_target_object = None
    
    # Set up room-specific interactions
    setup_room_interactions(room_id)

def setup_room_interactions(room_id):
    """Configure interactions for a specific room"""
    room_config = get_room_config(room_id)
    
    # Set up special interaction rules
    if room_id == "crime_scene":
        # Everything requires gloves
        for obj_name in get_room_objects():
            add_interaction_requirement(obj_name, "Use", "gloves")
    elif room_id == "dark_room":
        # Can't examine things without light
        if not store.flashlight_on:
            disable_action_for_room("Examine")
```

### Save System Integration

```python
# Save interaction preferences and history
def save_interaction_preferences():
    persistent.interaction_prefs = {
        "menu_style": store.interaction_menu_style,
        "auto_hide_delay": store.menu_auto_hide_delay,
        "default_action": store.preferred_default_action,
        "show_tooltips": store.interaction_tooltips_enabled
    }

# Load interaction preferences
def load_interaction_preferences():
    if hasattr(persistent, "interaction_prefs"):
        prefs = persistent.interaction_prefs
        store.interaction_menu_style = prefs.get("menu_style", "popup")
        store.menu_auto_hide_delay = prefs.get("auto_hide_delay", 3.0)
        store.preferred_default_action = prefs.get("default_action", "Examine")
        store.interaction_tooltips_enabled = prefs.get("show_tooltips", True)
```

The Interactions API provides a comprehensive system for handling player input and object interaction, with support for multiple input methods, complex action logic, and seamless integration with the rest of the framework.

