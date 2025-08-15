# Screens and UI System

## Overview

The Screens and UI system provides the visual interface layer for the framework's point-and-click adventure gameplay. This system manages screen composition, user interface elements, overlays, and the coordination between different visual components. It handles everything from room exploration screens to debug overlays, info displays, and interactive elements.

## Core Components

### Room Exploration Screen
The primary gameplay interface that orchestrates:
- Object hover detection and visual feedback
- Description box positioning and content display
- Interactive action menu presentation
- Navigation and selection management
- Input handling for multiple device types

### Overlay Systems
Layered interface elements that provide:
- Information overlays for game status and help
- Debug overlays with variable detail levels
- Visual effect overlays (letterbox, fade, etc.)
- Modal dialog and confirmation systems

### UI Component Architecture
Modular system for:
- Reusable screen components
- Customizable styling and theming
- Responsive layout management
- Accessibility feature integration

## Primary Screen Components

### Room Exploration Screen

**Location**: `game/ui/screens_room.rpy`

**Purpose**: Main gameplay interface that coordinates all room exploration elements

**Key Features**:
- Object interaction detection
- Dynamic description display
- Context-sensitive action menus
- Multi-input method support
- Visual effect integration

**Example Implementation**:
```renpy
screen room_exploration():
    # Background and scene setup
    add get_room_background() at room_background_transform
    
    # Room objects with interaction support
    for obj_name, obj_config in get_room_objects().items():
        if should_display_object(obj_name):
            imagebutton:
                idle obj_config["image"]
                hover Transform(obj_config["image"], brightness=1.2)
                pos obj_config["position"]
                
                # Mouse interactions
                action Function(execute_default_action, obj_name)
                alternate Function(show_interaction_menu, obj_name)
                
                # Hover handling
                hovered Function(handle_object_hover, obj_name)
                unhovered Function(handle_object_unhover)
    
    # Description box
    if store.current_hover_object:
        use description_box(store.current_hover_object)
    
    # Interaction menu
    if store.interaction_menu_active:
        use interaction_menu(store.interaction_target_object)
    
    # Navigation support
    use object_navigation_overlay
    
    # Effect overlays
    if store.bloom_enabled:
        use bloom_overlay
    
    if store.crt_enabled:
        use crt_overlay
    
    # Input handling
    key "K_TAB" action Function(cycle_object_selection)
    key "K_ESCAPE" action Function(handle_escape_key)
    key "K_RETURN" action Function(execute_selected_action)
```

### Description Box Component

**Purpose**: Display contextual information about hovered or selected objects

**Features**:
- Dynamic positioning to avoid screen edges
- Rich text formatting support
- Fade in/out animations
- Responsive sizing based on content

**Example**:
```renpy
screen description_box(obj_name):
    if obj_name and get_object_description(obj_name):
        $ description = get_object_description(obj_name)
        $ box_position = calculate_description_position(obj_name)
        
        frame:
            at description_fade_in
            pos box_position
            maximum (400, 200)
            background "#000000CC"
            padding (10, 8)
            
            text description:
                color "#FFFFFF"
                size 16
                justify True
                
define description_fade_in = Fade(0.2, 0.0, 0.2)

def calculate_description_position(obj_name):
    # Get object position
    obj_config = get_room_objects().get(obj_name, {})
    obj_pos = obj_config.get("position", (0, 0))
    
    # Calculate box position avoiding screen edges
    screen_width, screen_height = renpy.get_physical_size()
    box_width, box_height = 400, 200
    
    x = obj_pos[0] + 50
    y = obj_pos[1] - box_height - 10
    
    # Adjust for screen boundaries
    if x + box_width > screen_width:
        x = screen_width - box_width - 10
    if y < 0:
        y = obj_pos[1] + 50
    
    return (x, y)
```

### Interaction Menu Component

**Purpose**: Present available actions for the selected object

**Features**:
- Dynamic action list generation
- Keyboard/gamepad navigation support
- Visual action categories
- Icon and text combinations

**Example**:
```renpy
screen interaction_menu(obj_name):
    if obj_name:
        $ actions = get_actions_for(obj_name)
        $ menu_position = get_menu_base_position(obj_name)
        
        frame:
            at interaction_menu_appear
            pos menu_position
            background "#222222EE"
            padding (8, 6)
            
            vbox:
                spacing 4
                
                for action in actions:
                    textbutton action:
                        text_size 14
                        text_color "#FFFFFF"
                        text_hover_color "#FFFF00"
                        background None
                        hover_background "#444444AA"
                        
                        action Function(execute_object_action, obj_name, action)
                        
                        # Visual feedback for disabled actions
                        if not is_action_available(obj_name, action):
                            text_color "#666666"
                            action NullAction()
                            tooltip f"You can't {action.lower()} this right now."

define interaction_menu_appear = Transform:
    alpha 0.0
    on show:
        easein 0.15 alpha 1.0
    on hide:
        easeout 0.15 alpha 0.0
```

### Object Navigation Overlay

**Purpose**: Provide keyboard/gamepad navigation support for objects

**Features**:
- Visual selection indicators
- Navigation path highlighting
- Selection state persistence
- Input method adaptation

**Example**:
```renpy
screen object_navigation_overlay():
    # Show selection indicator for keyboard/gamepad navigation
    if store.selected_object and store.input_method != "mouse":
        $ obj_config = get_room_objects().get(store.selected_object, {})
        $ obj_pos = obj_config.get("position", (0, 0))
        $ obj_size = obj_config.get("size", (100, 100))
        
        frame:
            pos (obj_pos[0] - 5, obj_pos[1] - 5)
            xysize (obj_size[0] + 10, obj_size[1] + 10)
            background None
            
            # Selection border
            add "selection_border.png"
            
            # Pulsing effect for current selection
            at selection_pulse
    
    # Navigation hints for gamepad users
    if store.input_method == "gamepad" and store.show_navigation_hints:
        vbox:
            pos (20, 20)
            text "Navigate: D-Pad" size 12 color "#CCCCCC"
            text "Select: A Button" size 12 color "#CCCCCC"
            text "Menu: X Button" size 12 color "#CCCCCC"

define selection_pulse = Transform:
    alpha 0.7
    linear 1.0 alpha 1.0
    linear 1.0 alpha 0.7
    repeat
```

## Overlay Systems

### Info Overlay

**Location**: `game/overlays/info_overlay.rpy`

**Purpose**: Display game information, help text, and status indicators

**Features**:
- Startup welcome information
- Toggleable help and control information
- Game status indicators
- Version and build information

**Example**:
```renpy
screen info_overlay():
    if store.show_info_overlay:
        frame:
            at info_overlay_transform
            align (0.5, 0.5)
            background "#000000EE"
            padding (30, 20)
            
            vbox:
                spacing 15
                
                text "Snatchernauts Framework" size 24 color "#FFFFFF" bold True
                text "Version 0.5.3" size 16 color "#CCCCCC"
                
                null height 10
                
                text "Controls:" size 18 color "#FFFFFF" underline True
                text "• Mouse: Click objects to interact" size 14
                text "• Keyboard: TAB to navigate, ENTER to select" size 14
                text "• Right-click or SPACE for action menu" size 14
                text "• ESC to close menus or return to main menu" size 14
                
                null height 10
                
                textbutton "Close (ESC)":
                    action Function(hide_info_overlay)
                    align (0.5, 0.0)
    
    # Toggle shortcut
    key "K_F1" action Function(toggle_info_overlay)
    key "K_h" action Function(toggle_info_overlay)

define info_overlay_transform = Transform:
    alpha 0.0
    on show:
        easein 0.3 alpha 1.0
    on hide:
        easeout 0.3 alpha 0.0
```

### Debug Overlay

**Location**: `game/overlays/debug_overlay.rpy`

**Purpose**: Display development and debugging information

**Features**:
- Three visibility modes: hidden, compact, verbose
- Real-time game state monitoring
- Performance metrics display
- Object and room state information

**Example**:
```renpy
screen debug_overlay():
    if store.debug_overlay_mode != "hidden":
        frame:
            align (1.0, 0.0)
            background "#000000AA"
            padding (10, 8)
            
            vbox:
                spacing 2
                
                # Always show basic info in compact mode
                text f"Room: {get_current_room()}" size 12 color "#00FF00"
                text f"Objects: {len(get_room_objects())}" size 12 color "#00FF00"
                
                if store.current_hover_object:
                    text f"Hover: {store.current_hover_object}" size 12 color "#FFFF00"
                
                if store.debug_overlay_mode == "verbose":
                    null height 5
                    
                    text "Game State:" size 12 color "#FFFFFF" underline True
                    text f"Game time: {renpy.get_game_runtime():.1f}s" size 10
                    text f"Save slots: {len(renpy.list_saved_games())}" size 10
                    
                    if hasattr(store, "inventory"):
                        text f"Inventory: {len(store.inventory)} items" size 10
                    
                    null height 5
                    
                    text "Performance:" size 12 color "#FFFFFF" underline True
                    text f"FPS: {renpy.get_fps():.1f}" size 10
                    text f"Frame time: {1000/max(renpy.get_fps(), 1):.1f}ms" size 10
                    
                    null height 5
                    
                    text "Effects:" size 12 color "#FFFFFF" underline True
                    text f"CRT: {'ON' if store.crt_enabled else 'OFF'}" size 10
                    text f"Bloom: {'ON' if store.bloom_enabled else 'OFF'}" size 10
                    text f"Letterbox: {'ON' if store.letterbox_enabled else 'OFF'}" size 10
    
    # Cycle through debug modes
    key "cmd_shift_K_F12" action Function(cycle_debug_overlay)
    key "ctrl_shift_K_F12" action Function(cycle_debug_overlay)

def cycle_debug_overlay():
    if store.debug_overlay_mode == "hidden":
        store.debug_overlay_mode = "compact"
    elif store.debug_overlay_mode == "compact":
        store.debug_overlay_mode = "verbose"
    else:
        store.debug_overlay_mode = "hidden"
```

### Modal Dialog System

**Purpose**: Handle confirmations, prompts, and modal interactions

**Features**:
- Configurable dialog types
- Custom button layouts
- Input validation
- Keyboard navigation support

**Example**:
```renpy
screen modal_dialog(dialog_type, message, buttons=None, **kwargs):
    modal True
    
    # Dim background
    add "#000000AA"
    
    frame:
        align (0.5, 0.5)
        maximum (500, 300)
        background get_dialog_background(dialog_type)
        padding (20, 15)
        
        vbox:
            spacing 20
            
            # Icon based on dialog type
            if dialog_type in ["warning", "error", "info", "question"]:
                add f"ui/icons/{dialog_type}.png" align (0.5, 0.0) size (32, 32)
            
            # Message text
            text message:
                align (0.5, 0.0)
                text_align 0.5
                size 16
                color get_dialog_text_color(dialog_type)
            
            # Button area
            hbox:
                align (0.5, 0.0)
                spacing 20
                
                if buttons:
                    for button_text, button_action in buttons:
                        textbutton button_text:
                            action button_action
                            style get_dialog_button_style(dialog_type)
                else:
                    textbutton "OK":
                        action Hide("modal_dialog")
                        style "dialog_button"
    
    # Keyboard shortcuts
    if dialog_type == "confirmation":
        key "K_RETURN" action buttons[0][1] if buttons else Hide("modal_dialog")
        key "K_ESCAPE" action buttons[1][1] if len(buttons) > 1 else Hide("modal_dialog")
    else:
        key "K_ESCAPE" action Hide("modal_dialog")

def get_dialog_background(dialog_type):
    backgrounds = {
        "info": "#E3F2FDEE",
        "warning": "#FFF3E0EE",
        "error": "#FFEBEEEE",
        "question": "#F3E5F5EE",
        "confirmation": "#E8F5E8EE"
    }
    return backgrounds.get(dialog_type, "#F5F5F5EE")
```

## UI Customization System

### Style Configuration

**Location**: `game/ui/` directory

**Purpose**: Centralized styling and theming for all UI components

**Key Files**:
- `styles.rpy`: Base style definitions
- `themes.rpy`: Color schemes and theme variations
- `transforms.rpy`: Animation and transition effects
- `fonts.rpy`: Typography configuration

**Example Style Configuration**:
```renpy
# Base button style
style default_button:
    background "#4A4A4A"
    hover_background "#6A6A6A"
    selected_background "#8A8A8A"
    padding (12, 8)
    text_size 14
    text_color "#FFFFFF"
    text_hover_color "#FFFF00"

# Interaction menu button style
style interaction_button is default_button:
    background None
    hover_background "#444444AA"
    padding (8, 4)
    text_size 12
    minimum (120, 28)

# Description box style
style description_frame:
    background "#000000CC"
    padding (10, 8)
    maximum (400, 200)
    
style description_text:
    color "#FFFFFF"
    size 16
    justify True
    line_spacing 2

# Debug overlay styles
style debug_text:
    color "#00FF00"
    size 12
    font "fonts/mono.ttf"

# Theme variations
init python:
    def apply_dark_theme():
        style.default_button.background = "#2A2A2A"
        style.default_button.hover_background = "#4A4A4A"
        store.ui_theme = "dark"
    
    def apply_high_contrast_theme():
        style.default_button.background = "#000000"
        style.default_button.hover_background = "#FFFFFF"
        style.default_button.text_color = "#FFFFFF"
        style.default_button.text_hover_color = "#000000"
        store.ui_theme = "high_contrast"
```

### Custom Transforms and Animations

**Purpose**: Provide smooth transitions and visual effects for UI elements

**Example Transforms**:
```renpy
# Fade transitions
define ui_fade_in = Fade(0.2, 0.0, 0.2)
define ui_fade_out = Fade(0.0, 0.2, 0.0)

# Slide transitions
define slide_in_from_right = Transform:
    xoffset 300
    alpha 0.0
    on show:
        parallel:
            easein 0.3 xoffset 0
        parallel:
            easein 0.3 alpha 1.0

define slide_out_to_right = Transform:
    on hide:
        parallel:
            easeout 0.3 xoffset 300
        parallel:
            easeout 0.3 alpha 0.0

# Scale effects
define hover_scale = Transform:
    on hover:
        easein 0.1 zoom 1.05
    on idle:
        easein 0.1 zoom 1.0

# Bounce effect for notifications
define notification_bounce = Transform:
    yoffset -20
    alpha 0.0
    on show:
        parallel:
            easein 0.2 yoffset 0
            easeout 0.1 yoffset -5
            easein 0.1 yoffset 0
        parallel:
            easein 0.2 alpha 1.0
    on hide:
        parallel:
            easeout 0.2 yoffset -20
        parallel:
            easeout 0.2 alpha 0.0

# Pulsing effect for important elements
define pulse_important = Transform:
    linear 1.0 alpha 0.7
    linear 1.0 alpha 1.0
    repeat
```

## Best Practices

### Performance Optimization

```python
# Cache frequently used images
init python:
    def preload_ui_images():
        """Preload common UI images for better performance"""
        ui_images = [
            "ui/button_bg.png",
            "ui/frame_bg.png",
            "ui/selection_border.png",
            "ui/icons/info.png",
            "ui/icons/warning.png"
        ]
        
        for image_path in ui_images:
            renpy.cache_pin(image_path)

# Efficient object rendering
screen optimized_room_objects():
    # Only render visible objects
    for obj_name, obj_config in get_visible_room_objects().items():
        # Use cached transforms when possible
        if obj_name in store.cached_object_transforms:
            add obj_config["image"] at store.cached_object_transforms[obj_name]
        else:
            add obj_config["image"] at obj_config.get("transform", identity)
```

### Accessibility Considerations

```python
# Screen reader support
init python:
    def announce_screen_change(screen_name, description):
        """Announce screen changes for accessibility"""
        if store.accessibility_mode:
            renpy.notify(f"Screen changed to {screen_name}: {description}")
    
    def set_focus_order(elements):
        """Define keyboard navigation order"""
        store.focus_order = elements
        store.current_focus_index = 0

# High contrast support
screen accessible_button(text, action, **kwargs):
    textbutton text:
        action action
        
        # Use high contrast colors if enabled
        if store.accessibility_mode:
            text_color "#000000"
            text_hover_color "#FFFFFF"
            background "#FFFFFF"
            hover_background "#000000"
        
        # Ensure minimum size for touch accessibility
        minimum (44, 44)
        
        # Add keyboard focus indicator
        if kwargs.get("has_focus", False):
            background Transform(kwargs.get("background", "#4A4A4A"), brightness=1.5)
```

The Screens and UI system provides a comprehensive, flexible foundation for creating engaging and accessible user interfaces in the framework, with extensive customization options and robust component architecture.

