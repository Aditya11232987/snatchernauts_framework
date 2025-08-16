# Logic Hooks System

**Part II: Core Development - Chapter 4**

*A comprehensive guide to implementing custom game behavior through the framework's event-driven logic hook system, enabling sophisticated interactive experiences through standardized callback functions.*

---

## Chapter Overview

This chapter provides complete coverage of the framework's logic hook system, the primary mechanism for implementing custom game behavior. The event-driven architecture enables clean separation between game logic and presentation while maintaining the flexibility needed for complex interactive narratives.

The logic hook system represents one of the framework's most powerful features, allowing developers to:
- **Respond to Player Actions**: Handle clicks, hovers, and interactions with sophisticated conditional logic
- **Manage Game State**: Control story progression, character relationships, and environmental changes
- **Create Dynamic Experiences**: Implement adaptive content that responds to player choices and game history
- **Maintain Code Organization**: Separate global logic from room-specific behaviors for better maintainability

**By the end of this chapter, you will master:**
- The complete hierarchy and execution flow of the logic hook system
- Implementation patterns for both global and room-specific event handlers
- Advanced techniques for state management and conditional interactions
- Best practices for performance optimization and error handling
- Common development patterns for inventory, puzzles, and narrative progression
- Debugging and testing strategies for complex interactive logic

## Understanding the Event-Driven Architecture

The framework's event-driven design enables sophisticated game behavior through a clean, predictable system where custom code responds to player actions and system events through standardized callback functions called "hooks."

### Core Design Philosophy

**Separation of Concerns**: The hook system maintains clear boundaries between different aspects of game development:

```python
# Game Logic (hooks) - Pure behavioral implementation
def on_object_interact(room_id, obj, action):
    if obj == "mysterious_box" and action == "examine":
        if game_state.player_has_skill("investigation"):
            return reveal_hidden_compartment()
        else:
            return show_basic_examination()

# UI Implementation - Visual presentation (separate file)
screen room_exploration():
    imagebutton:
        idle "mysterious_box_idle.png"
        hover "mysterious_box_highlight.png"
        action Function(handle_object_interaction, "mysterious_box")
```

**Event Flow Control**: The system provides multiple levels of event handling with clear precedence rules:

1. **Room-Specific Handlers**: Custom logic for individual locations
2. **Global Handlers**: Fallback behavior for system-wide events
3. **Framework Defaults**: Built-in functionality when no custom logic is provided

### Event Processing Pipeline

Understanding the complete event processing pipeline enables effective logic implementation:

#### Phase 1: Event Detection and Routing
```python
# Framework internal event routing (conceptual)
def process_player_interaction(room_id, object_id, action_type):
    # Validate interaction is possible
    if not validate_interaction_context(room_id, object_id, action_type):
        return handle_invalid_interaction()
    
    # Route to appropriate handler
    room_handler = get_registered_room_handler(room_id)
    if room_handler:
        result = room_handler.on_object_interact(room_id, object_id, action_type)
        if result:  # Handler processed the event
            return complete_interaction(result)
    
    # Fall back to global handler
    global_result = call_global_hook("on_object_interact", room_id, object_id, action_type)
    if global_result:
        return complete_interaction(global_result)
    
    # Execute framework default behavior
    return execute_default_interaction(object_id, action_type)
```

#### Phase 2: Logic Execution and State Updates
```python
# State management during hook execution
def execute_hook_with_state_management(hook_function, *args):
    # Capture current state for rollback capability
    previous_state = capture_game_state()
    
    try:
        # Execute custom logic
        result = hook_function(*args)
        
        # Validate state changes
        if validate_state_changes():
            commit_state_changes()
            trigger_state_change_events()
            return result
        else:
            rollback_to_state(previous_state)
            return False
            
    except Exception as e:
        # Handle errors gracefully
        log_hook_error(hook_function.__name__, e)
        rollback_to_state(previous_state)
        return False
```

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

## Comprehensive Global Hook Reference

The framework provides several additional global hooks beyond the basic set, enabling sophisticated game behavior through specialized event handling.

### Advanced Global Hooks

#### `on_room_exit(room_id)`

**When Called**: Just before transitioning away from a room

**Purpose**: Clean up room-specific state, save temporary data, trigger departure events

**Parameters**:
- `room_id` (string): The identifier of the room being exited

**Return Value**: None

**Example**:
```python
def on_room_exit(room_id):
    # Save room-specific temporary state
    if room_id == "laboratory":
        persistent.lab_state = {
            "experiment_progress": store.current_experiment_step,
            "equipment_used": list(store.lab_equipment_activated),
            "last_visit_time": renpy.get_game_runtime()
        }
    
    # Stop room-specific audio
    renpy.music.stop(channel="ambient", fadeout=1.0)
    
    # Clear temporary visual effects
    renpy.hide_screen("room_specific_overlay")
    
    # Log room exit for analytics
    log_room_transition(room_id, "exit", renpy.get_game_runtime())
```

#### `on_game_save(save_data) -> dict`

**When Called**: Before the game saves player progress

**Purpose**: Add custom data to save files, perform pre-save validation

**Parameters**:
- `save_data` (dict): Current save data being prepared

**Return Value**: Dictionary of additional data to include in save file

**Example**:
```python
def on_game_save(save_data):
    # Add custom analytics and state tracking
    custom_data = {
        "game_statistics": {
            "total_playtime": renpy.get_game_runtime(),
            "rooms_visited": len(persistent.visited_rooms),
            "evidence_collected": len(store.evidence_collected),
            "conversations_completed": store.conversation_count
        },
        "player_choices": {
            "moral_alignment": calculate_moral_alignment(),
            "relationship_scores": dict(store.character_relationships),
            "major_decisions": list(persistent.story_decisions)
        },
        "technical_data": {
            "framework_version": get_framework_version(),
            "save_timestamp": time.time(),
            "debug_mode": config.developer
        }
    }
    
    # Validate save data integrity
    if not validate_save_integrity(custom_data):
        raise SaveDataValidationError("Save data validation failed")
    
    return custom_data
```

#### `on_game_load(save_data)`

**When Called**: After loading a saved game

**Purpose**: Restore custom state, perform post-load setup, handle save compatibility

**Parameters**:
- `save_data` (dict): Complete save data including custom additions

**Return Value**: None

**Example**:
```python
def on_game_load(save_data):
    # Restore custom game statistics
    if "game_statistics" in save_data:
        stats = save_data["game_statistics"]
        store.total_playtime = stats.get("total_playtime", 0)
        store.completion_percentage = calculate_completion_percentage(stats)
    
    # Handle save compatibility
    save_version = save_data.get("framework_version", "1.0.0")
    if save_version != get_framework_version():
        migrate_save_data(save_data, save_version)
    
    # Restore room-specific state
    current_room = persistent.current_room
    if current_room and current_room in save_data.get("room_states", {}):
        restore_room_state(current_room, save_data["room_states"][current_room])
    
    # Update UI based on loaded state
    refresh_character_relationship_display()
    update_evidence_board()
    
    # Log successful load for debugging
    print(f"[LOAD] Game loaded successfully. Playtime: {store.total_playtime}s")
```

#### `on_game_state_change(key, old_value, new_value)`

**When Called**: Whenever a monitored game state variable changes

**Purpose**: React to state changes, trigger dependent updates, validate state transitions

**Parameters**:
- `key` (string): The name of the changed variable
- `old_value` (any): Previous value
- `new_value` (any): New value

**Return Value**: None

**Example**:
```python
def on_game_state_change(key, old_value, new_value):
    # React to evidence collection
    if key == "evidence_collected" and len(new_value) > len(old_value):
        new_evidence = set(new_value) - set(old_value)
        for evidence in new_evidence:
            trigger_evidence_analysis(evidence)
            update_case_progress()
    
    # Handle relationship changes
    if key.startswith("relationship_"):
        character = key.replace("relationship_", "")
        relationship_change = new_value - old_value
        
        if relationship_change > 0:
            show_relationship_improvement(character, relationship_change)
        elif relationship_change < 0:
            show_relationship_decline(character, abs(relationship_change))
    
    # Validate critical state changes
    if key == "player_health" and new_value <= 0:
        trigger_game_over_sequence()
    elif key == "current_chapter" and new_value > old_value:
        initialize_new_chapter(new_value)
```

### Advanced State Management Patterns

Effective state management is crucial for creating coherent, persistent interactive experiences.

#### Hierarchical State Organization

```python
# game/logic/game_logic.rpy
init python:
    class GameStateManager:
        def __init__(self):
            # Initialize hierarchical state structure
            if not hasattr(persistent, 'game_state'):
                persistent.game_state = {
                    "story": {
                        "chapter": 1,
                        "scene": "opening",
                        "major_decisions": [],
                        "unlocked_locations": ["home"]
                    },
                    "player": {
                        "inventory": [],
                        "skills": {"investigation": 1, "social": 1, "technical": 1},
                        "experience_points": 0,
                        "moral_alignment": 0
                    },
                    "world": {
                        "time_of_day": "morning",
                        "weather": "clear",
                        "day_number": 1,
                        "location_states": {}
                    },
                    "characters": {
                        "relationships": {},
                        "conversation_flags": {},
                        "character_locations": {}
                    }
                }
        
        def get_state(self, path):
            """Retrieve state value using dot notation path"""
            keys = path.split('.')
            current = persistent.game_state
            
            for key in keys:
                if key in current:
                    current = current[key]
                else:
                    return None
            return current
        
        def set_state(self, path, value):
            """Set state value using dot notation path"""
            keys = path.split('.')
            current = persistent.game_state
            
            # Navigate to parent of target key
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the final value
            old_value = current.get(keys[-1])
            current[keys[-1]] = value
            
            # Trigger state change event
            on_game_state_change(path, old_value, value)
        
        def has_state(self, path):
            """Check if state path exists"""
            return self.get_state(path) is not None
    
    # Global state manager instance
    game_state = GameStateManager()
```

#### Conditional State Validation

```python
# Advanced state validation system
init python:
    class StateValidator:
        def __init__(self):
            self.validation_rules = {
                "player.skills.*": self.validate_skill_level,
                "story.chapter": self.validate_chapter_progression,
                "world.time_of_day": self.validate_time_progression,
                "player.inventory": self.validate_inventory_constraints
            }
        
        def validate_skill_level(self, skill_name, new_value):
            """Ensure skill levels stay within valid bounds"""
            if not isinstance(new_value, int) or new_value < 1 or new_value > 10:
                raise ValueError(f"Invalid skill level: {new_value}")
            return True
        
        def validate_chapter_progression(self, new_chapter):
            """Ensure chapters progress logically"""
            current_chapter = game_state.get_state("story.chapter")
            if new_chapter > current_chapter + 1:
                raise ValueError(f"Cannot skip chapters: {current_chapter} -> {new_chapter}")
            return True
        
        def validate_inventory_constraints(self, new_inventory):
            """Check inventory size and item compatibility"""
            max_inventory_size = 20
            if len(new_inventory) > max_inventory_size:
                raise ValueError(f"Inventory full: {len(new_inventory)}/{max_inventory_size}")
            
            # Check for conflicting items
            conflicting_pairs = [("holy_water", "cursed_artifact")]
            for item1, item2 in conflicting_pairs:
                if item1 in new_inventory and item2 in new_inventory:
                    raise ValueError(f"Conflicting items: {item1} and {item2}")
            
            return True
    
    state_validator = StateValidator()
```

## Advanced Room Logic Patterns

Sophisticated room logic enables complex, adaptive gameplay experiences that respond to player actions and game state.

### Multi-State Room Logic

```python
# game/logic/rooms/laboratory_logic.rpy
init python:
    class LaboratoryLogic:
        def __init__(self):
            # Define possible room states
            self.room_states = {
                "pristine": {
                    "description": "A clean, well-organized laboratory",
                    "available_objects": ["microscope", "chemical_cabinet", "research_notes"]
                },
                "ransacked": {
                    "description": "The laboratory has been thoroughly searched",
                    "available_objects": ["broken_microscope", "spilled_chemicals", "scattered_papers"]
                },
                "crime_scene": {
                    "description": "Police tape blocks access to most equipment",
                    "available_objects": ["police_tape", "evidence_markers", "detective_badge"]
                }
            }
            
            # Initialize room state based on story progress
            self.current_state = self.determine_initial_state()
        
        def determine_initial_state(self):
            """Determine room state based on game progress"""
            if game_state.get_state("story.chapter") >= 3:
                return "crime_scene"
            elif "laboratory_break_in" in game_state.get_state("story.major_decisions"):
                return "ransacked"
            else:
                return "pristine"
        
        def transition_room_state(self, new_state, reason=None):
            """Change room state with proper cleanup and setup"""
            if new_state not in self.room_states:
                raise ValueError(f"Invalid room state: {new_state}")
            
            old_state = self.current_state
            self.current_state = new_state
            
            # Remove objects from old state
            old_objects = self.room_states[old_state]["available_objects"]
            for obj in old_objects:
                room_api.remove_room_object(obj)
            
            # Add objects for new state
            new_objects = self.room_states[new_state]["available_objects"]
            for obj in new_objects:
                room_api.add_room_object(obj, self.get_object_definition(obj))
            
            # Update room description
            room_api.set_room_description(self.room_states[new_state]["description"])
            
            # Log state transition
            print(f"[LABORATORY] State changed: {old_state} -> {new_state} ({reason})")
        
        def on_object_interact(self, room_id, obj, action):
            """State-aware object interactions"""
            if self.current_state == "pristine":
                return self.handle_pristine_interactions(obj, action)
            elif self.current_state == "ransacked":
                return self.handle_ransacked_interactions(obj, action)
            elif self.current_state == "crime_scene":
                return self.handle_crime_scene_interactions(obj, action)
            
            return False
        
        def handle_pristine_interactions(self, obj, action):
            """Interactions available in pristine state"""
            if obj == "chemical_cabinet" and action == "examine":
                if game_state.get_state("player.skills.technical") >= 3:
                    renpy.say(None, "You identify several dangerous compounds.")
                    game_state.set_state("player.knowledge.chemistry", True)
                else:
                    renpy.say(None, "The chemical labels are too technical to understand.")
                return True
            
            if obj == "research_notes" and action == "read":
                renpy.call("laboratory_research_notes_scene")
                if "research_breakthrough" in persistent.unlocked_knowledge:
                    self.transition_room_state("ransacked", "research_discovery_triggered")
                return True
            
            return False
```

### Dynamic Object Behavior

```python
# Advanced dynamic object system
init python:
    class DynamicObjectManager:
        def __init__(self):
            self.object_behaviors = {}
            self.conditional_objects = {}
        
        def register_conditional_object(self, object_id, conditions, object_definition):
            """Register an object that appears based on conditions"""
            self.conditional_objects[object_id] = {
                "conditions": conditions,
                "definition": object_definition,
                "active": False
            }
        
        def register_dynamic_behavior(self, object_id, behavior_function):
            """Register dynamic behavior for an object"""
            self.object_behaviors[object_id] = behavior_function
        
        def update_conditional_objects(self, room_id):
            """Check and update conditional objects for current room"""
            for object_id, config in self.conditional_objects.items():
                should_be_active = self.evaluate_conditions(config["conditions"])
                
                if should_be_active and not config["active"]:
                    # Object should appear
                    room_api.add_room_object(room_id, object_id, config["definition"])
                    config["active"] = True
                    print(f"[DYNAMIC] Object {object_id} appeared in {room_id}")
                
                elif not should_be_active and config["active"]:
                    # Object should disappear
                    room_api.remove_room_object(object_id)
                    config["active"] = False
                    print(f"[DYNAMIC] Object {object_id} disappeared from {room_id}")
        
        def evaluate_conditions(self, conditions):
            """Evaluate complex conditional logic"""
            for condition in conditions:
                if condition["type"] == "state_equals":
                    if game_state.get_state(condition["path"]) != condition["value"]:
                        return False
                elif condition["type"] == "state_greater_than":
                    if game_state.get_state(condition["path"]) <= condition["value"]:
                        return False
                elif condition["type"] == "has_item":
                    if condition["item"] not in game_state.get_state("player.inventory"):
                        return False
                elif condition["type"] == "custom_function":
                    if not condition["function"]():
                        return False
            return True
        
        def execute_object_behavior(self, object_id, room_id, action):
            """Execute dynamic behavior for an object"""
            if object_id in self.object_behaviors:
                return self.object_behaviors[object_id](room_id, action)
            return False
    
    dynamic_objects = DynamicObjectManager()
```

## Comprehensive Best Practices and Optimization

### Code Organization and Architecture

#### Modular Hook Organization

```python
# game/logic/game_logic.rpy - Main logic coordination
init python:
    # Import specialized logic modules
    from game.logic.modules.inventory_logic import InventoryManager
    from game.logic.modules.dialogue_logic import DialogueManager
    from game.logic.modules.puzzle_logic import PuzzleManager
    
    # Initialize specialized managers
    inventory_manager = InventoryManager()
    dialogue_manager = DialogueManager()
    puzzle_manager = PuzzleManager()

def on_object_interact(room_id, obj, action):
    """Coordinate between specialized logic modules"""
    # Try inventory actions first
    if action in ["take", "use", "combine"]:
        result = inventory_manager.handle_interaction(room_id, obj, action)
        if result:
            return True
    
    # Try dialogue actions
    if action in ["talk", "question", "persuade"]:
        result = dialogue_manager.handle_interaction(room_id, obj, action)
        if result:
            return True
    
    # Try puzzle interactions
    if obj.startswith("puzzle_") or action in ["solve", "manipulate"]:
        result = puzzle_manager.handle_interaction(room_id, obj, action)
        if result:
            return True
    
    # Default to room-specific or framework handling
    return False
```

#### Performance Optimization Strategies

```python
# Performance-optimized hover handling
init python:
    class OptimizedHoverManager:
        def __init__(self):
            self.hover_cache = {}
            self.last_hover_object = None
            self.hover_debounce_timer = 0.0
        
        def handle_hover(self, room_id, obj):
            """Optimized hover handling with caching and debouncing"""
            current_time = renpy.get_game_runtime()
            
            # Debounce rapid hover events
            if current_time - self.hover_debounce_timer < 0.1:
                return
            
            self.hover_debounce_timer = current_time
            
            # Skip if same object as last hover
            if obj == self.last_hover_object:
                return
            
            self.last_hover_object = obj
            
            # Use cached tooltip if available
            cache_key = f"{room_id}_{obj}"
            if cache_key in self.hover_cache:
                tooltip_data = self.hover_cache[cache_key]
                ui_api.show_tooltip(tooltip_data)
                return
            
            # Generate tooltip and cache it
            tooltip_data = self.generate_tooltip(room_id, obj)
            self.hover_cache[cache_key] = tooltip_data
            ui_api.show_tooltip(tooltip_data)
        
        def generate_tooltip(self, room_id, obj):
            """Generate tooltip data for caching"""
            # Implement tooltip generation logic
            return {
                "text": f"Interactive object: {obj}",
                "style": "default_tooltip"
            }
    
    hover_manager = OptimizedHoverManager()
```

#### Comprehensive Error Handling and Recovery

```python
# Robust error handling system
init python:
    class LogicErrorHandler:
        def __init__(self):
            self.error_log = []
            self.fallback_behaviors = {
                "interaction_failed": self.fallback_interaction,
                "state_invalid": self.fallback_state_recovery,
                "object_missing": self.fallback_object_creation
            }
        
        def safe_execute_hook(self, hook_function, *args, **kwargs):
            """Execute hook with comprehensive error handling"""
            try:
                return hook_function(*args, **kwargs)
            
            except AttributeError as e:
                self.log_error("AttributeError", str(e), hook_function.__name__)
                return self.fallback_behaviors["state_invalid"]()
            
            except KeyError as e:
                self.log_error("KeyError", str(e), hook_function.__name__)
                return self.fallback_behaviors["object_missing"]()
            
            except Exception as e:
                self.log_error("GeneralError", str(e), hook_function.__name__)
                return self.fallback_behaviors["interaction_failed"]()
        
        def log_error(self, error_type, message, function_name):
            """Log error with context information"""
            error_entry = {
                "timestamp": renpy.get_game_runtime(),
                "type": error_type,
                "message": message,
                "function": function_name,
                "game_state": self.capture_error_context()
            }
            
            self.error_log.append(error_entry)
            
            # Log to console in developer mode
            if config.developer:
                print(f"[ERROR] {error_type} in {function_name}: {message}")
        
        def capture_error_context(self):
            """Capture relevant game state for error debugging"""
            return {
                "current_room": persistent.current_room,
                "chapter": game_state.get_state("story.chapter"),
                "inventory_size": len(game_state.get_state("player.inventory")),
                "playtime": renpy.get_game_runtime()
            }
    
    error_handler = LogicErrorHandler()
```

### Advanced Testing and Debugging

#### Automated Hook Testing Framework

```python
# game/logic/testing/hook_tests.rpy
init python:
    class HookTestFramework:
        def __init__(self):
            self.test_results = []
            self.mock_state = {}
        
        def run_all_tests(self):
            """Execute comprehensive hook testing suite"""
            self.test_results = []
            
            # Test global hooks
            self.test_on_game_start()
            self.test_on_room_enter()
            self.test_on_object_interact()
            self.test_on_object_hover()
            
            # Test room-specific logic
            self.test_room_logic_handlers()
            
            # Test state management
            self.test_state_persistence()
            
            # Generate test report
            self.generate_test_report()
        
        def test_on_object_interact(self):
            """Test object interaction logic"""
            test_cases = [
                {
                    "room_id": "test_room",
                    "obj": "test_object",
                    "action": "examine",
                    "expected": True
                },
                {
                    "room_id": "test_room",
                    "obj": "invalid_object",
                    "action": "examine",
                    "expected": False
                }
            ]
            
            for case in test_cases:
                try:
                    result = on_object_interact(
                        case["room_id"], 
                        case["obj"], 
                        case["action"]
                    )
                    
                    self.assert_equal(result, case["expected"], 
                                    f"Interaction test: {case}")
                except Exception as e:
                    self.record_test_failure("on_object_interact", str(e), case)
        
        def assert_equal(self, actual, expected, test_name):
            """Assert that values are equal"""
            if actual == expected:
                self.record_test_success(test_name)
            else:
                self.record_test_failure(test_name, 
                                       f"Expected {expected}, got {actual}")
        
        def record_test_success(self, test_name):
            self.test_results.append({
                "test": test_name,
                "status": "PASS",
                "message": None
            })
        
        def record_test_failure(self, test_name, error_message, context=None):
            self.test_results.append({
                "test": test_name,
                "status": "FAIL",
                "message": error_message,
                "context": context
            })
    
    # Only create test framework in developer mode
    if config.developer:
        hook_test_framework = HookTestFramework()
```

### Navigation and Next Steps

With mastery of the logic hook system, you're equipped to implement sophisticated game behavior that responds dynamically to player actions and game state.

### Recommended Learning Path

**Immediate Application**:

1. **[Screen and UI System](05-Screens-and-UI.md)** - Learn how logic hooks integrate with user interface components to create seamless interactive experiences.

2. **[Room API Deep Dive](10-API-Room.md)** - Explore the room management system that works closely with logic hooks to control game environments.

3. **[Interaction API Integration](11-API-Interactions.md)** - Master the interaction system that provides the framework infrastructure supporting your custom hook logic.

**Advanced Development**:

4. **[Effects and Visual Integration](06-Effects-and-Shaders.md)** - Learn to trigger sophisticated visual effects from logic hooks for enhanced player feedback.

5. **[Audio System Coordination](12-API-Audio.md)** - Implement dynamic audio that responds to logic hook events for immersive soundscapes.

6. **[Save/Load Integration](13-API-Save.md)** - Design robust save systems that properly preserve your custom game state across sessions.

### Development Best Practices Summary

**Logic Hook Design Principles**:

- **Single Responsibility**: Each hook should handle one specific aspect of game behavior
- **Predictable Returns**: Always return consistent boolean values from interaction hooks
- **State Validation**: Validate game state before making changes to prevent corruption
- **Error Resilience**: Implement graceful error handling to maintain game stability
- **Performance Awareness**: Keep frequently-called hooks (especially hover) lightweight
- **Testing Integration**: Build testable logic with clear inputs and expected outputs

---

**Navigation**:

← [**Previous: Framework Architecture**](03-Architecture.md) | [**Next: Screens and UI System**](05-Screens-and-UI.md) →

---

*This completes Chapter 4 of the Snatchernauts Framework Manual. You now have comprehensive understanding of the logic hook system, enabling you to implement sophisticated game behavior through event-driven architecture. Continue to the Screens and UI chapter to learn how your logic integrates with visual presentation systems.*

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

