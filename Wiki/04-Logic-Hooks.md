# Game Logic Hooks Reference

## Overview

The Snatchernauts Framework uses an event-driven architecture where your game logic responds to player actions and system events through "hooks" - Python functions that are called at specific moments during gameplay. This system provides clean separation between game logic and UI presentation while maintaining flexibility for complex interactions.

## Hook System Architecture

The framework supports two levels of logic handlers:

1. **Global Hooks**: Functions defined in `game/logic/game_logic.rpy` that handle system-wide events
2. **Room-Specific Handlers**: Classes registered for individual rooms that can override global behavior

### Execution Order

When an event occurs, the framework follows this execution order:
1. Check for registered room-specific handler
2. If room handler exists and handles the event (returns `True`), stop processing
3. Otherwise, call the global hook function
4. If global hook handles the event (returns `True`), stop processing
5. Finally, execute framework default behavior (if any)

## Global Hook Functions

All global hooks should be implemented in `game/logic/game_logic.rpy`:

### `on_game_start()`

**When Called**: Once during game initialization, after the startup overlay is displayed

**Purpose**: Perform one-time game setup, initialize global variables, set initial game state

**Parameters**: None

**Return Value**: None

**Example**:
```python
def on_game_start():
    # Initialize global game state
    persistent.game_started = True
    persistent.current_chapter = 1
    
    # Set up character relationships
    store.relationship_detective = 0
    store.evidence_collected = []
    
    # Play intro music
    renpy.music.play("audio/intro_theme.ogg", loop=True)
    
    # Show tutorial if first time
    if not persistent.tutorial_completed:
        renpy.show_screen("tutorial_overlay")
```

### `on_room_enter(room_id)`

**When Called**: Every time a new room is loaded and displayed

**Purpose**: Set up room-specific state, play ambient audio, trigger room-specific events

**Parameters**:
- `room_id` (string): The identifier of the room being entered

**Return Value**: None

**Example**:
```python
def on_room_enter(room_id):
    # Update current location for save system
    persistent.current_room = room_id
    
    # Room-specific setup
    if room_id == "detective_office":
        renpy.music.play("audio/office_ambient.ogg", channel="ambient", loop=True)
        # Check if detective is present
        if store.detective_present:
            renpy.show("detective idle", at_list=[Transform(xpos=400)])
    
    elif room_id == "crime_scene":
        renpy.music.play("audio/crime_ambient.ogg", channel="ambient", loop=True)
        # Darken the scene if first visit
        if not persistent.crime_scene_visited:
            renpy.show("crime_scene", at_list=[Transform(matrixcolor=BrightnessMatrix(0.3))])
            persistent.crime_scene_visited = True
    
    # Log room entry for debugging
    print(f"[GAME] Entered room: {room_id}")
```

### `on_object_hover(room_id, obj)`

**When Called**: When the player hovers over or selects an interactive object

**Purpose**: Update UI feedback, display contextual information, prefetch content

**Parameters**:
- `room_id` (string): The current room identifier
- `obj` (string): The name of the object being hovered over

**Return Value**: None (this hook doesn't prevent default behavior)

**Example**:
```python
def on_object_hover(room_id, obj):
    # Update status text or cursor
    if obj == "evidence_box":
        renpy.show_screen("hover_tooltip", text="Evidence Box - Contains case files")
    elif obj == "detective":
        if store.detective_talked_to:
            renpy.show_screen("hover_tooltip", text="Detective Martinez - Ask about the case")
        else:
            renpy.show_screen("hover_tooltip", text="Detective Martinez - Introduce yourself")
    elif obj == "door_locked":
        renpy.show_screen("hover_tooltip", text="Locked Door - Need a key")
    
    # Prefetch audio for interactions
    if obj == "radio" and not renpy.music.get_playing("radio"):
        renpy.music.queue("audio/radio_static.ogg", channel="radio")
    
    # Debug logging
    print(f"[HOVER] {room_id}.{obj}")
```

### `on_object_interact(room_id, obj, action) -> bool`

**When Called**: When the player performs an action on an interactive object

**Purpose**: Handle specific interactions, trigger story events, modify game state

**Parameters**:
- `room_id` (string): The current room identifier
- `obj` (string): The name of the object being interacted with
- `action` (string): The action being performed (e.g., "Examine", "Take", "Talk")

**Return Value**: Boolean indicating whether the interaction was fully handled
- `True`: Interaction was handled, skip framework defaults
- `False`: Allow framework to process default behavior

**Example**:
```python
def on_object_interact(room_id, obj, action):
    # Handle evidence collection
    if obj == "evidence_photo" and action == "Take":
        if "photo" not in store.evidence_collected:
            store.evidence_collected.append("photo")
            renpy.say(None, "You carefully pick up the photograph.")
            renpy.hide("evidence_photo")
            renpy.notify("Evidence collected: Mysterious photograph")
            return True
        else:
            renpy.say(None, "You've already taken this photograph.")
            return True
    
    # Handle character conversations
    if obj == "detective" and action == "Talk":
        if not store.detective_talked_to:
            renpy.call("detective_first_conversation")
            store.detective_talked_to = True
        else:
            renpy.call("detective_followup_conversation")
        return True
    
    # Handle locked doors
    if obj == "door_locked" and action == "Open":
        if "office_key" in store.inventory:
            renpy.say(None, "You unlock the door with the key.")
            renpy.call("load_room", "secret_office")
        else:
            renpy.say(None, "The door is locked. You need a key.")
        return True
    
    # Let framework handle unspecified interactions
    return False
```

## Room-Specific Logic Handlers

For complex games, you can create dedicated logic classes for individual rooms to keep code organized and maintainable.

### Creating Room Handlers

1. Create a new file: `game/logic/rooms/{room_name}_logic.rpy`
2. Define a Python class with methods matching the global hooks
3. Register the handler using `register_room_logic()`

### Room Handler Template

```python
# File: game/logic/rooms/detective_office_logic.rpy

init python:
    class DetectiveOfficeLogic:
        def __init__(self):
            # Initialize room-specific state
            self.first_visit = True
            self.evidence_examined = set()
        
        def on_room_enter(self, room_id):
            """Handle entering the detective office"""
            if self.first_visit:
                renpy.say(None, "You step into the cluttered detective office.")
                self.first_visit = False
            
            # Update ambient lighting based on time of day
            if store.time_of_day == "night":
                renpy.show("office_night", zorder=0)
            else:
                renpy.show("office_day", zorder=0)
        
        def on_object_hover(self, room_id, obj):
            """Provide contextual hover information"""
            if obj == "case_files":
                count = len(store.evidence_collected)
                renpy.show_screen("hover_tooltip", 
                    text=f"Case Files - {count} pieces of evidence collected")
        
        def on_object_interact(self, room_id, obj, action):
            """Handle office-specific interactions"""
            if obj == "desk_drawer" and action == "Search":
                if "desk_key" not in store.inventory:
                    renpy.say(None, "The drawer is locked tight.")
                else:
                    renpy.say(None, "You find a hidden compartment with documents.")
                    # Add evidence or trigger story event
                    store.evidence_collected.append("hidden_documents")
                return True
            
            if obj == "detective_photo" and action == "Examine":
                if "photo" not in self.evidence_examined:
                    renpy.call("examine_detective_photo_scene")
                    self.evidence_examined.add("photo")
                else:
                    renpy.say(None, "You've already studied this photograph closely.")
                return True
            
            # Let global handler or framework handle other interactions
            return False
    
    # Register the handler for the detective office room
    register_room_logic("detective_office", DetectiveOfficeLogic())
```

### Advanced Room Handler Features

#### State Persistence
```python
class RoomLogic:
    def __init__(self):
        # Use persistent data for state that should survive saves/loads
        if not hasattr(persistent, 'office_state'):
            persistent.office_state = {
                "lights_on": False,
                "safe_combination_known": False,
                "items_discovered": []
            }
    
    def on_object_interact(self, room_id, obj, action):
        if obj == "light_switch" and action == "Use":
            persistent.office_state["lights_on"] = not persistent.office_state["lights_on"]
            self._update_lighting()
            return True
    
    def _update_lighting(self):
        if persistent.office_state["lights_on"]:
            renpy.show("office_bright")
        else:
            renpy.show("office_dark")
```

#### Dynamic Object Creation
```python
def on_room_enter(self, room_id):
    # Add objects based on story progression
    if store.chapter >= 3 and "evidence_board" not in room_objects:
        room_api.add_room_object(room_id, "evidence_board", {
            "image": "evidence_board.png",
            "position": (600, 200),
            "actions": ["Examine", "Update"]
        })
```

## Best Practices

### Code Organization
1. **Keep hooks focused**: Each hook should handle one specific aspect of gameplay
2. **Use descriptive names**: Object and action names should be self-explanatory
3. **Separate concerns**: Keep UI logic in screens, game logic in hooks
4. **Handle edge cases**: Always check for required conditions before executing actions

### Performance Considerations
1. **Minimize hover logic**: `on_object_hover` is called frequently, keep it lightweight
2. **Cache expensive operations**: Store computed values rather than recalculating
3. **Use lazy loading**: Only load resources when actually needed
4. **Avoid blocking operations**: Don't perform long-running tasks in hooks

### Error Handling
```python
def on_object_interact(self, room_id, obj, action):
    try:
        if obj == "computer" and action == "Use":
            if not hasattr(store, 'computer_password'):
                renpy.say(None, "You need to find the password first.")
                return True
            
            # Perform computer interaction
            return self._handle_computer_use()
    except Exception as e:
        # Log error and provide user feedback
        print(f"[ERROR] Computer interaction failed: {e}")
        renpy.say(None, "The computer seems to be malfunctioning.")
        return True
```

### Testing and Debugging
1. **Use debug prints**: Add logging to track hook execution
2. **Test return values**: Ensure `True`/`False` returns work as expected
3. **Verify state changes**: Check that persistent data is updated correctly
4. **Test edge cases**: What happens with invalid objects or actions?

## Common Patterns

### Inventory Management
```python
def on_object_interact(self, room_id, obj, action):
    if action == "Take":
        if obj not in store.inventory:
            store.inventory.append(obj)
            renpy.hide(obj)  # Remove from room
            renpy.notify(f"Picked up: {obj.replace('_', ' ').title()}")
        else:
            renpy.say(None, "You already have this item.")
        return True
```

### Conditional Interactions
```python
def on_object_interact(self, room_id, obj, action):
    if obj == "safe" and action == "Open":
        if store.player_knows_combination:
            renpy.call("open_safe_scene")
        elif "safe_manual" in store.evidence_collected:
            renpy.call("try_safe_combination_scene")
        else:
            renpy.say(None, "You need to find the combination first.")
        return True
```

### Progressive Revelation
```python
def on_object_interact(self, room_id, obj, action):
    if obj == "painting" and action == "Examine":
        examination_count = persistent.painting_examinations
        
        if examination_count == 0:
            renpy.say(None, "A beautiful landscape painting.")
        elif examination_count == 1:
            renpy.say(None, "Wait, there's something odd about the frame.")
        elif examination_count >= 2:
            renpy.say(None, "You notice a hidden switch behind the frame!")
            room_api.add_room_object(room_id, "hidden_switch", {...})
        
        persistent.painting_examinations += 1
        return True
```

