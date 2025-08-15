# UI API Reference

## Overview

The UI API (`game/api/ui_api.rpy`) provides essential user interface functionality for the framework's point-and-click adventure system. This API handles floating description boxes, screen composition for room exploration, tooltips, prompts, confirmations, and various UI helper functions. It serves as the bridge between game logic and the visual presentation layer.

## Core Responsibilities

### Description Management
- Display floating description boxes for hovered objects
- Manage description positioning and appearance
- Handle dynamic description content based on game state
- Coordinate description visibility with other UI elements

### Screen Composition
- Drive the main room exploration screen architecture
- Coordinate between different UI components and overlays
- Manage screen transitions and state changes
- Handle multi-layer UI composition for complex scenes

### Interactive Elements
- Provide tooltip systems for enhanced user experience
- Handle confirmation dialogs and prompts
- Manage modal UI states and user input routing
- Support keyboard, mouse, and gamepad interaction patterns

### Visual Feedback
- Coordinate hover effects and visual states
- Manage UI element highlighting and selection feedback
- Handle loading states and progress indicators
- Provide consistent visual language across different screens

## Primary Functions

### Description Box Management

#### `show_description(obj_name, description, position=None)`

**Purpose**: Display a floating description box for an object

**Parameters**:
- `obj_name` (string): Name of the object being described
- `description` (string): Text content to display
- `position` (tuple, optional): Screen position (x, y) for the description box

**Example**:
```python
# Show description at mouse position
show_description("desk", "A cluttered detective's desk with papers scattered about.")

# Show description at specific position
show_description("door", "A heavy wooden door.", position=(100, 200))

# Show dynamic description based on game state
def show_contextual_description(obj_name):
    if obj_name == "safe":
        if store.safe_opened:
            desc = "The safe is open and empty."
        elif store.has_combination:
            desc = "You know the combination to this safe."
        else:
            desc = "A locked safe with a combination dial."
        show_description(obj_name, desc)
```

#### `hide_description()`

**Purpose**: Hide the currently displayed description box

**Example**:
```python
# Hide description on object unhover
def handle_object_unhover():
    hide_description()
    store.current_hover_object = None

# Auto-hide description after timeout
init python:
    def auto_hide_description():
        renpy.timeout(2.0)
        hide_description()
```

#### `update_description(new_description)`

**Purpose**: Update the content of the currently displayed description box

**Parameters**:
- `new_description` (string): New description text

**Example**:
```python
# Update description based on examination progress
def examine_desk():
    if store.desk_examination_count == 0:
        update_description("A cluttered desk. You should look more carefully.")
    elif store.desk_examination_count == 1:
        update_description("Looking closer, you notice a hidden drawer.")
    else:
        update_description("You've thoroughly examined this desk.")
    
    store.desk_examination_count += 1
```

### Screen Composition Helpers

#### `compose_exploration_screen(room_id, **kwargs)`

**Purpose**: Set up the main room exploration screen with all necessary components

**Parameters**:
- `room_id` (string): Identifier of the current room
- `**kwargs`: Additional configuration parameters

**Example**:
```python
# Basic room exploration setup
compose_exploration_screen("office")

# Room exploration with custom settings
compose_exploration_screen(
    "office",
    enable_descriptions=True,
    show_debug_overlay=store.dev_mode,
    interaction_menu_style="contextual",
    enable_gamepad_nav=True
)

# Compose screen with room-specific UI elements
def setup_crime_scene_ui():
    compose_exploration_screen(
        "crime_scene",
        evidence_collection_mode=True,
        show_evidence_counter=True,
        restrict_interactions=store.case_progress < 5
    )
```

#### `register_ui_component(component_name, component_screen)`

**Purpose**: Register a custom UI component for use in screen composition

**Parameters**:
- `component_name` (string): Unique identifier for the component
- `component_screen` (string): Name of the Ren'Py screen to use

**Example**:
```python
# Register custom inventory display
register_ui_component("inventory_bar", "inventory_horizontal_bar")

# Register mini-map component
register_ui_component("mini_map", "room_mini_map")

# Use registered components
def compose_enhanced_exploration():
    base_components = get_default_ui_components()
    base_components.extend(["inventory_bar", "mini_map"])
    
    compose_exploration_screen(
        get_current_room(),
        components=base_components
    )
```

### Interactive UI Elements

#### `show_confirmation(message, on_yes=None, on_no=None, **kwargs)`

**Purpose**: Display a confirmation dialog with customizable actions

**Parameters**:
- `message` (string): Confirmation message text
- `on_yes` (callable, optional): Function to call if user confirms
- `on_no` (callable, optional): Function to call if user cancels
- `**kwargs`: Additional styling and behavior options

**Example**:
```python
# Simple confirmation
show_confirmation("Are you sure you want to quit?", 
                 on_yes=Function(renpy.quit),
                 on_no=Function(hide_confirmation))

# Confirmation with game logic
def try_destroy_evidence():
    show_confirmation(
        "Destroying evidence is irreversible. Continue?",
        on_yes=Function(destroy_evidence_and_update_plot),
        on_no=Function(hide_confirmation),
        style="danger",
        require_double_confirm=True
    )

# Confirmation with parameters
def confirm_room_transition(target_room):
    show_confirmation(
        f"Leave this area and go to {target_room}?",
        on_yes=Function(navigate_to_room, target_room),
        on_no=Function(hide_confirmation)
    )
```

#### `show_tooltip(element, tooltip_text, **kwargs)`

**Purpose**: Display a tooltip for a UI element

**Parameters**:
- `element` (string): Identifier of the UI element
- `tooltip_text` (string): Tooltip content
- `**kwargs`: Positioning and styling options

**Example**:
```python
# Show tooltip on hover
screen inventory_item(item_name):
    imagebutton:
        idle f"inventory/{item_name}.png"
        action Function(use_inventory_item, item_name)
        hovered Function(show_tooltip, item_name, get_item_description(item_name))
        unhovered Function(hide_tooltip)

# Show contextual tooltip
def show_action_tooltip(action_name):
    tooltips = {
        "Examine": "Look closely at this object",
        "Use": "Interact with this object",
        "Talk": "Start a conversation",
        "Take": "Add to your inventory"
    }
    
    show_tooltip(action_name, tooltips.get(action_name, "Perform action"))
```

#### `show_prompt(message, input_type="text", on_submit=None, **kwargs)`

**Purpose**: Display an input prompt dialog

**Parameters**:
- `message` (string): Prompt message
- `input_type` (string): Type of input ("text", "number", "choice")
- `on_submit` (callable): Function to call with the input value
- `**kwargs`: Additional configuration options

**Example**:
```python
# Text input prompt
def ask_for_safe_combination():
    show_prompt(
        "Enter the safe combination:",
        input_type="number",
        on_submit=Function(try_safe_combination),
        max_length=4,
        placeholder="0000"
    )

# Choice prompt
def ask_dialogue_choice():
    choices = ["Ask about the case", "Ask about the victim", "Leave"]
    show_prompt(
        "What would you like to discuss?",
        input_type="choice",
        choices=choices,
        on_submit=Function(handle_dialogue_choice)
    )
```

### UI State Management

#### `get_ui_state()`

**Purpose**: Get the current UI state information

**Returns**: Dictionary containing current UI state

**Example**:
```python
# Check current UI state
ui_state = get_ui_state()

if ui_state["modal_active"]:
    print("Modal dialog is open")

if ui_state["description_visible"]:
    print(f"Showing description for: {ui_state['description_target']}")

# Save UI state for restoration
store.saved_ui_state = get_ui_state()
```

#### `set_ui_state(state_dict)`

**Purpose**: Set UI state from a state dictionary

**Parameters**:
- `state_dict` (dict): State information to restore

**Example**:
```python
# Restore saved UI state
def restore_ui_state():
    if hasattr(store, "saved_ui_state"):
        set_ui_state(store.saved_ui_state)
        del store.saved_ui_state

# Set specific UI state
set_ui_state({
    "modal_active": False,
    "description_visible": False,
    "interaction_menu_active": False,
    "current_focus": None
})
```

#### `save_ui_preferences()`

**Purpose**: Save user UI preferences to persistent storage

**Example**:
```python
# Save UI preferences
def save_ui_preferences():
    persistent.ui_preferences = {
        "description_position": store.description_position_preference,
        "tooltip_delay": store.tooltip_delay,
        "confirmation_style": store.confirmation_style,
        "menu_animation_speed": store.menu_animation_speed,
        "accessibility_mode": store.accessibility_mode
    }

# Load UI preferences
def load_ui_preferences():
    if hasattr(persistent, "ui_preferences"):
        prefs = persistent.ui_preferences
        store.description_position_preference = prefs.get("description_position", "auto")
        store.tooltip_delay = prefs.get("tooltip_delay", 0.5)
        store.confirmation_style = prefs.get("confirmation_style", "standard")
        store.menu_animation_speed = prefs.get("menu_animation_speed", 1.0)
        store.accessibility_mode = prefs.get("accessibility_mode", False)
```

### Advanced UI Features

#### `create_dynamic_menu(menu_items, position=None, **kwargs)`

**Purpose**: Create a dynamic menu with customizable items and behavior

**Parameters**:
- `menu_items` (list): List of menu item dictionaries
- `position` (tuple, optional): Menu position (x, y)
- `**kwargs`: Additional menu configuration

**Example**:
```python
# Create context menu
def show_context_menu(obj_name):
    menu_items = []
    
    # Add basic actions
    menu_items.append({
        "text": "Examine",
        "action": Function(execute_object_action, obj_name, "Examine"),
        "enabled": True
    })
    
    # Add conditional actions
    if obj_name in store.usable_objects:
        menu_items.append({
            "text": "Use",
            "action": Function(execute_object_action, obj_name, "Use"),
            "enabled": True
        })
    
    # Add inventory-based actions
    for item in store.inventory:
        if can_use_item_on_object(item, obj_name):
            menu_items.append({
                "text": f"Use {item}",
                "action": Function(use_item_on_object, item, obj_name),
                "enabled": True,
                "icon": f"inventory/{item}.png"
            })
    
    create_dynamic_menu(menu_items, style="contextual")
```

#### `handle_ui_input(input_event, context=None)`

**Purpose**: Handle UI input events with proper routing and context awareness

**Parameters**:
- `input_event` (dict): Input event information
- `context` (string, optional): Current input context

**Example**:
```python
# Handle keyboard shortcuts
def handle_ui_input(input_event, context=None):
    event_type = input_event.get("type")
    key = input_event.get("key")
    
    if event_type == "keydown":
        if key == "K_ESCAPE":
            if get_ui_state()["modal_active"]:
                close_current_modal()
            elif get_ui_state()["interaction_menu_active"]:
                hide_interaction_menu()
            else:
                show_main_menu()
            return True
        
        elif key == "K_TAB":
            if context == "room_exploration":
                cycle_object_selection()
            return True
        
        elif key == "K_RETURN":
            if context == "room_exploration":
                execute_selected_action()
            return True
    
    return False
```

### UI Animation and Transitions

#### `animate_ui_element(element_id, animation_type, **kwargs)`

**Purpose**: Animate UI elements with various transition effects

**Parameters**:
- `element_id` (string): Identifier of the UI element to animate
- `animation_type` (string): Type of animation ("fade", "slide", "scale", "bounce")
- `**kwargs`: Animation parameters (duration, easing, etc.)

**Example**:
```python
# Fade in description box
animate_ui_element("description_box", "fade", 
                  direction="in", duration=0.3, easing="ease_out")

# Slide menu from right
animate_ui_element("interaction_menu", "slide",
                  direction="right_to_center", duration=0.5)

# Bounce notification
animate_ui_element("notification", "bounce",
                  intensity=0.2, duration=0.8)

# Scale hover effect
def animate_hover_effect(obj_name, hover_state):
    if hover_state:
        animate_ui_element(f"object_{obj_name}", "scale",
                          target_scale=1.1, duration=0.2)
    else:
        animate_ui_element(f"object_{obj_name}", "scale",
                          target_scale=1.0, duration=0.2)
```

## Integration with Other Systems

### Room System Integration

```python
# Update UI when room changes
def on_room_enter(room_id):
    # Clear existing UI state
    hide_all_modals()
    hide_description()
    
    # Set up room-specific UI
    setup_room_ui(room_id)
    
    # Configure room-specific interactions
    configure_interaction_ui(room_id)

def setup_room_ui(room_id):
    """Configure UI for specific room"""
    room_config = get_room_config(room_id)
    
    # Set room-specific UI elements
    if room_config.get("show_inventory", True):
        show_ui_component("inventory")
    
    if room_config.get("show_map", False):
        show_ui_component("mini_map")
    
    # Configure description positioning
    if room_id == "narrow_hallway":
        set_description_position("bottom")
    else:
        set_description_position("auto")
```

### Save System Integration

```python
# Save UI state with game data
def save_ui_state_with_game():
    game_save_data = get_current_save_data()
    game_save_data["ui_state"] = {
        "preferences": get_ui_preferences(),
        "window_positions": get_window_positions(),
        "accessibility_settings": get_accessibility_settings()
    }
    save_game_data(game_save_data)

# Load UI state from save data
def load_ui_state_from_save(save_data):
    if "ui_state" in save_data:
        ui_state = save_data["ui_state"]
        
        if "preferences" in ui_state:
            set_ui_preferences(ui_state["preferences"])
        
        if "accessibility_settings" in ui_state:
            set_accessibility_settings(ui_state["accessibility_settings"])
```

## Accessibility Features

```python
# High contrast mode
def enable_high_contrast_mode():
    set_ui_theme("high_contrast")
    store.accessibility_mode = True
    
# Screen reader support
def announce_to_screen_reader(text):
    if store.accessibility_mode:
        renpy.notify(text)
        # Additional screen reader integration would go here

# Keyboard navigation enhancement
def enhance_keyboard_navigation():
    if store.accessibility_mode:
        # Make all interactive elements keyboard accessible
        register_keyboard_shortcuts({
            "K_h": show_help_dialog,
            "K_d": toggle_description_verbosity,
            "K_s": announce_current_state
        })
```

The UI API provides a comprehensive foundation for creating rich, accessible, and user-friendly interfaces within the framework, with extensive customization options and seamless integration with other framework systems.

