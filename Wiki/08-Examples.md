# Examples and Case Studies

**Part II: Core Development - Chapter 8**

*Comprehensive practical examples and real-world case studies demonstrating advanced implementation patterns, optimization techniques, and production-ready solutions using the Snatchernauts Framework.*

---

## Chapter Overview

This chapter provides an extensive collection of practical examples, implementation patterns, and case studies that demonstrate the full power and flexibility of the Snatchernauts Framework. Rather than simple code snippets, these are complete, production-ready implementations that you can adapt and extend for your own projects.

Each example is carefully crafted to demonstrate not just how to implement specific features, but also best practices, performance considerations, error handling, and maintainable code architecture. The examples progress from fundamental concepts to sophisticated systems that showcase the framework's advanced capabilities.

**What makes these examples comprehensive:**
- **Production-Ready Code**: Complete implementations with error handling and optimization
- **Progressive Complexity**: From basic concepts to advanced architectural patterns
- **Real-World Context**: Examples based on actual game development scenarios
- **Performance Conscious**: Efficient implementations with performance metrics and optimization
- **Extensible Patterns**: Modular designs that can be easily adapted and extended

**By studying these examples, you will master:**
- Advanced room system architectures with dynamic object management
- Sophisticated logic hook patterns for complex game mechanics
- Custom UI system integration and responsive design patterns
- Visual effects orchestration and atmospheric design systems
- Performance optimization techniques and debugging methodologies
- Save/load system integration with complex state management
- Testing frameworks and quality assurance patterns
- Production deployment and maintenance strategies

## Basic Room Setup

### Simple Room Configuration

```python
# File: game/rooms/office/scripts/office_config.rpy

# Basic room definition
define OFFICE_OBJECTS = {
    "desk": {
        "image": "office/desk.png",
        "position": (400, 300),
        "actions": ["Examine", "Search"],
        "description": "A cluttered detective's desk"
    },
    "filing_cabinet": {
        "image": "office/filing_cabinet.png",
        "position": (700, 250),
        "actions": ["Examine", "Open"],
        "description": "A locked filing cabinet"
    },
    "window": {
        "image": "office/window.png",
        "position": (100, 100),
        "actions": ["Look"],
        "description": "Rain streaks down the glass"
    }
}

define ROOM_DEFINITIONS_OFFICE = {
    "detective_office": {
        "background": "office/background.png",
        "objects": OFFICE_OBJECTS,
        "audio": {
            "ambient": "audio/office_ambient.ogg",
            "tension": "audio/investigation_theme.ogg"
        }
    }
}

# Merge with global room definitions
init python:
    ROOM_DEFINITIONS.update(ROOM_DEFINITIONS_OFFICE)
```

### Loading and Entering Rooms

```python
# File: game/script.rpy

label start:
    # Show intro
    scene black
    "Welcome to the Snatchernauts Framework demonstration."
    
    # Load the first room
    $ load_room("detective_office")
    
    # Start exploration
    call screen room_exploration
    
    return

label play_room(room_id="detective_office", music=None):
    # Load room with optional music
    $ load_room(room_id, music)
    
    # Start interactive exploration
    call screen room_exploration
    
    return
```

## Logic Hook Examples

### Basic Per-Room Logic Handler

```python
# File: game/logic/rooms/office_logic.rpy

init python:
    class OfficeLogic:
        def __init__(self):
            self.desk_searched = False
            self.cabinet_opened = False
            self.window_examined = False
        
        def on_room_enter(self, room_id):
            """Called when player enters the office"""
            if not persistent.office_visited:
                renpy.say(None, "You step into the dimly lit detective office.")
                persistent.office_visited = True
            
            # Set appropriate mood music
            if store.case_urgency > 5:
                play_room_audio(room_id, "tension")
            else:
                play_room_audio(room_id, "ambient")
        
        def on_object_hover(self, room_id, obj):
            """Called when player hovers over objects"""
            # Provide contextual information
            if obj == "filing_cabinet" and not self.cabinet_opened:
                renpy.show_screen("hover_tooltip", text="Locked - need a key")
            elif obj == "desk" and not self.desk_searched:
                renpy.show_screen("hover_tooltip", text="Something might be hidden here")
        
        def on_object_interact(self, room_id, obj, action):
            """Handle specific object interactions"""
            
            # Desk interactions
            if obj == "desk":
                if action == "Examine":
                    renpy.say(None, "The desk is covered with case files and coffee stains.")
                    return True
                elif action == "Search":
                    return self._search_desk()
            
            # Filing cabinet interactions
            elif obj == "filing_cabinet":
                if action == "Examine":
                    renpy.say(None, "A sturdy metal filing cabinet with a combination lock.")
                    return True
                elif action == "Open":
                    return self._open_cabinet()
            
            # Window interactions
            elif obj == "window":
                if action == "Look":
                    return self._look_out_window()
            
            return False  # Let framework handle unrecognized interactions
        
        def _search_desk(self):
            """Handle desk searching"""
            if self.desk_searched:
                renpy.say(None, "You've already searched the desk thoroughly.")
                return True
            
            renpy.say(None, "You carefully search through the desk drawers...")
            
            # Add suspense
            renpy.pause(1.0)
            
            if "office_key" not in store.inventory:
                renpy.say(None, "You find a small brass key hidden under some papers!")
                store.inventory.append("office_key")
                renpy.notify("Found: Office Key")
            else:
                renpy.say(None, "Nothing else of interest in the desk.")
            
            self.desk_searched = True
            return True
        
        def _open_cabinet(self):
            """Handle filing cabinet opening"""
            if "office_key" not in store.inventory:
                renpy.say(None, "The filing cabinet is locked. You need a key.")
                return True
            
            if self.cabinet_opened:
                renpy.say(None, "The filing cabinet is already open.")
                return True
            
            renpy.say(None, "You unlock the filing cabinet with the brass key.")
            renpy.play("audio/unlock.ogg")
            
            # Add important evidence
            renpy.say(None, "Inside, you discover classified case files!")
            store.evidence_collected.append("classified_files")
            renpy.notify("Evidence found: Classified Files")
            
            self.cabinet_opened = True
            
            # Progress the story
            $ store.case_progress += 1
            
            return True
        
        def _look_out_window(self):
            """Handle window examination"""
            if not self.window_examined:
                renpy.say(None, "Rain streaks down the dirty glass. The city looks gray and lifeless.")
                self.window_examined = True
            else:
                # Different description on repeat examination
                if store.time_of_day == "night":
                    renpy.say(None, "The city lights blur through the rain-streaked glass.")
                else:
                    renpy.say(None, "The rain continues to fall steadily outside.")
            
            return True
    
    # Register the logic handler
    register_room_logic("detective_office", OfficeLogic())
```

### Global Logic Handler

```python
# File: game/logic/game_logic.rpy

init python:
    # Global game state
    default inventory = []
    default evidence_collected = []
    default case_progress = 0
    default case_urgency = 3
    default time_of_day = "day"

def on_game_start():
    """Called once at game startup"""
    # Initialize global state
    store.inventory = []
    store.evidence_collected = []
    store.case_progress = 0
    
    # Set up initial conditions
    persistent.tutorial_completed = persistent.tutorial_completed or False
    
    # Show tutorial for new players
    if not persistent.tutorial_completed:
        renpy.call("tutorial_sequence")
    
    print("[GAME] Game started successfully")

def on_room_enter(room_id):
    """Called when entering any room (global handler)"""
    # Update save data
    persistent.current_room = room_id
    
    # Room-specific global setup
    if room_id == "crime_scene":
        # Always tense music at crime scene
        store.case_urgency = max(store.case_urgency, 7)
    elif room_id.startswith("flashback_"):
        # Special effects for flashbacks
        store.crt_enabled = True
        set_color_grade("vintage")
    
    print(f"[GAME] Entered room: {room_id}")

def on_object_hover(room_id, obj):
    """Called when hovering over any object (global handler)"""
    # Global hover behaviors
    pass  # Most hover logic is handled by room-specific handlers

def on_object_interact(room_id, obj, action):
    """Called for any object interaction (global handler)"""
    # Handle global interactions that work everywhere
    
    # Generic examine behavior for undefined objects
    if action == "Examine" and obj not in get_room_objects(room_id):
        renpy.say(None, "Nothing particularly interesting.")
        return True
    
    # Inventory item usage
    if action.startswith("Use "):
        item = action[4:]  # Remove "Use " prefix
        return handle_inventory_usage(item, obj)
    
    return False  # Let room handlers or defaults handle it

def handle_inventory_usage(item, target_obj):
    """Handle using inventory items on objects"""
    if item not in store.inventory:
        renpy.say(None, f"You don't have {item.replace('_', ' ')}.")
        return True
    
    # Specific item combinations
    if item == "office_key" and target_obj == "filing_cabinet":
        renpy.say(None, "You unlock the filing cabinet.")
        # This would be handled by room-specific logic
        return False
    
    # Generic "doesn't work" message
    renpy.say(None, f"Using {item.replace('_', ' ')} on {target_obj.replace('_', ' ')} doesn't work.")
    return True
```

## Advanced Examples

### Dynamic Object Creation

```python
# File: game/logic/rooms/investigation_room_logic.rpy

init python:
    class InvestigationRoomLogic:
        def __init__(self):
            self.evidence_board_updated = False
            self.computer_accessed = False
        
        def on_room_enter(self, room_id):
            """Set up room based on investigation progress"""
            # Add evidence board if player has collected enough evidence
            if len(store.evidence_collected) >= 3 and not self.evidence_board_updated:
                add_room_object(room_id, "evidence_board", {
                    "image": "investigation/evidence_board.png",
                    "position": (200, 150),
                    "actions": ["Examine", "Update"],
                    "description": "Board showing case connections",
                    "desaturation_preset": "explosive_normal"
                })
                renpy.notify("Evidence board now available!")
                self.evidence_board_updated = True
            
            # Add computer terminal if case progress is sufficient
            if store.case_progress >= 5 and not self.computer_accessed:
                add_room_object(room_id, "computer", {
                    "image": "investigation/computer.png",
                    "position": (600, 300),
                    "actions": ["Use", "Search Database"],
                    "description": "Police database terminal"
                })
        
        def on_object_interact(self, room_id, obj, action):
            if obj == "evidence_board":
                if action == "Examine":
                    self._examine_evidence_board()
                    return True
                elif action == "Update":
                    self._update_evidence_board()
                    return True
            
            elif obj == "computer":
                if action == "Use":
                    self._use_computer()
                    return True
                elif action == "Search Database":
                    self._search_database()
                    return True
            
            return False
        
        def _examine_evidence_board(self):
            """Show current evidence connections"""
            evidence_count = len(store.evidence_collected)
            
            if evidence_count < 3:
                renpy.say(None, "The evidence board is mostly empty.")
            elif evidence_count < 6:
                renpy.say(None, "Several pieces of evidence are connected with red string.")
            else:
                renpy.say(None, "The evidence board shows a complex web of connections.")
                if evidence_count >= 8:
                    renpy.say(None, "Wait... there's a pattern emerging here!")
                    $ store.case_breakthrough = True
        
        def _update_evidence_board(self):
            """Add new evidence to the board"""
            new_evidence = [e for e in store.evidence_collected if e not in store.evidence_on_board]
            
            if not new_evidence:
                renpy.say(None, "All your evidence is already on the board.")
                return
            
            for evidence in new_evidence:
                store.evidence_on_board.append(evidence)
                renpy.say(None, f"You pin {evidence.replace('_', ' ')} to the board.")
            
            # Check for breakthrough
            if len(store.evidence_on_board) >= 6:
                renpy.call("evidence_breakthrough_scene")
        
        def _use_computer(self):
            """Basic computer interaction"""
            if not self.computer_accessed:
                renpy.say(None, "You log into the police database.")
                self.computer_accessed = True
            else:
                renpy.say(None, "The computer screen shows the main database menu.")
            
            # Show computer interface screen
            renpy.call_screen("computer_interface")
        
        def _search_database(self):
            """Search for case-related information"""
            if not store.suspects_identified:
                renpy.say(None, "You search for information about the case suspects...")
                renpy.pause(1.5)
                renpy.say(None, "Several matching records found!")
                $ store.suspects_identified = True
                $ store.case_progress += 2
            else:
                renpy.say(None, "You've already found all relevant information.")
    
    # Initialize default variables
    default evidence_on_board = []
    default case_breakthrough = False
    default suspects_identified = False
    
    register_room_logic("investigation_room", InvestigationRoomLogic())
```

### Custom UI and Interaction Screens

```python
# File: game/ui/custom_screens.rpy

# Custom computer interface screen
screen computer_interface():
    modal True
    
    # Background
    add "#001122" alpha 0.9
    
    frame:
        xalign 0.5
        yalign 0.5
        background "#003366"
        padding (40, 40)
        
        vbox:
            spacing 20
            
            text "POLICE DATABASE" size 32 color "#00FF00" xalign 0.5
            
            null height 10
            
            # Search options
            vbox:
                spacing 15
                
                textbutton "Search Suspects" action Return("search_suspects")
                textbutton "Case Files" action Return("case_files")
                textbutton "Evidence Database" action Return("evidence_db")
                
                if store.case_progress >= 7:
                    textbutton "Classified Records" action Return("classified")
            
            null height 20
            
            textbutton "Log Out" action Return("logout") xalign 0.5

# Enhanced interaction menu
screen enhanced_interaction_menu(obj):
    modal True
    
    # Get object info
    $ obj_config = get_room_objects().get(obj, {})
    $ actions = obj_config.get('actions', [])
    $ description = obj_config.get('description', obj.replace('_', ' ').title())
    
    # Background overlay
    add "#000000" alpha 0.5
    
    frame:
        xpos mouse_pos[0]
        ypos mouse_pos[1]
        background Frame("ui/menu_bg.png", 10, 10)
        
        vbox:
            spacing 8
            
            # Object name
            text description size 18 color "#FFFFFF" xalign 0.5
            
            null height 5
            
            # Action buttons
            for action in actions:
                textbutton action:
                    action [Function(execute_object_action, obj, action), Return()]
                    text_size 16
            
            # Inventory item usage (if inventory exists)
            if store.inventory:
                null height 10
                text "Use item:" size 14 color "#CCCCCC"
                
                for item in store.inventory:
                    textbutton f"Use {item.replace('_', ' ')}":
                        action [Function(execute_object_action, obj, f"Use {item}"), Return()]
                        text_size 14
            
            null height 10
            textbutton "Cancel" action Return() text_size 14 xalign 0.5

# Evidence collection notification
screen evidence_notification(evidence_name):
    zorder 100
    
    frame:
        xalign 0.5
        yalign 0.1
        background "#004400"
        padding (20, 15)
        
        hbox:
            spacing 10
            text "🔍" size 24
            text f"Evidence Found: {evidence_name.replace('_', ' ').title()}" size 18 color "#FFFFFF"
    
    # Auto-hide after 3 seconds
    timer 3.0 action Hide("evidence_notification")
```

### Advanced Visual Effects

```python
# File: game/logic/effects_examples.rpy

init python:
    def setup_crime_scene_atmosphere():
        """Set up dramatic atmosphere for crime scene"""
        # Enable letterbox for cinematic feel
        show_letterbox(True)
        
        # Use noir color grading
        set_color_grade("crime_scene")
        
        # Add police lights effect
        set_lighting("police_lights")
        
        # Subtle film grain
        store.film_grain_enabled = True
        store.film_grain_intensity = 0.3
    
    def setup_flashback_sequence():
        """Visual effects for flashback scenes"""
        # Enable CRT for retro feel
        store.crt_enabled = True
        set_crt_parameters(warp=0.08, scan=0.2, chroma=0.004)
        
        # Vintage color grading
        set_color_grade("vintage")
        
        # Desaturate slightly
        renpy.show("flashback_overlay", at_list=[Transform(matrixcolor=SaturationMatrix(0.7))])
    
    def create_investigation_montage():
        """Dynamic visual sequence for investigation progress"""
        # Quick room transitions with effects
        rooms = ["office", "crime_scene", "lab", "suspects_room"]
        
        for i, room in enumerate(rooms):
            # Flash effect
            renpy.show("white", at_list=[Transform(alpha=0.8)])
            renpy.pause(0.1)
            renpy.hide("white")
            
            # Load room
            load_room(room, fade_in=False)
            
            # Show key evidence
            evidence_item = store.evidence_collected[i] if i < len(store.evidence_collected) else None
            if evidence_item:
                renpy.show(f"evidence_{evidence_item}", at_list=[
                    Transform(xalign=0.5, yalign=0.5, zoom=1.5, alpha=0.0),
                    ease(0.5, alpha=1.0, zoom=1.0)
                ])
                renpy.pause(1.0)
                renpy.hide(f"evidence_{evidence_item}")
            
            renpy.pause(0.5)
```

### Save/Load Integration

```python
# File: game/logic/save_system.rpy

init python:
    def save_investigation_state():
        """Save current investigation progress"""
        persistent.investigation_data = {
            "evidence_collected": store.evidence_collected[:],
            "evidence_on_board": store.evidence_on_board[:],
            "case_progress": store.case_progress,
            "suspects_identified": store.suspects_identified,
            "rooms_visited": getattr(store, "rooms_visited", []),
            "current_room": get_current_room()
        }
        
        # Save room-specific states
        for room_id in ["office", "crime_scene", "investigation_room"]:
            save_room_changes(room_id)
    
    def load_investigation_state():
        """Restore investigation progress"""
        if hasattr(persistent, "investigation_data") and persistent.investigation_data:
            data = persistent.investigation_data
            
            store.evidence_collected = data.get("evidence_collected", [])
            store.evidence_on_board = data.get("evidence_on_board", [])
            store.case_progress = data.get("case_progress", 0)
            store.suspects_identified = data.get("suspects_identified", False)
            store.rooms_visited = data.get("rooms_visited", [])
            
            # Load last room
            last_room = data.get("current_room")
            if last_room:
                load_room(last_room)
    
    # Auto-save on significant progress
    def auto_save_progress():
        """Automatic save when case progresses"""
        if store.case_progress % 2 == 0:  # Save every 2 progress points
            save_investigation_state()
            renpy.notify("Progress saved")

# Hook into the case progress system
init python:
    def increment_case_progress(amount=1):
        """Safely increment case progress with auto-save"""
        store.case_progress += amount
        auto_save_progress()
        
        # Check for major milestones
        if store.case_progress == 10:
            renpy.call("case_solved_scene")
        elif store.case_progress == 5:
            renpy.call("breakthrough_scene")
```

## Testing and Debugging Examples

### Debug Commands

```python
# File: game/debug_commands.rpy

init python:
    def debug_add_evidence(evidence_name):
        """Debug command to add evidence"""
        if evidence_name not in store.evidence_collected:
            store.evidence_collected.append(evidence_name)
            renpy.notify(f"Debug: Added {evidence_name}")
    
    def debug_set_progress(progress_level):
        """Debug command to set case progress"""
        store.case_progress = progress_level
        renpy.notify(f"Debug: Progress set to {progress_level}")
    
    def debug_unlock_all_rooms():
        """Debug command to make all rooms accessible"""
        store.rooms_unlocked = ["office", "crime_scene", "lab", "investigation_room"]
        renpy.notify("Debug: All rooms unlocked")
    
    # Console commands (accessible via Shift+O)
    config.console_commands = {
        "evidence": debug_add_evidence,
        "progress": debug_set_progress,
        "unlock": debug_unlock_all_rooms
    }
```

### Performance Testing

```python
# File: game/performance_test.rpy

init python:
    import time
    
    def benchmark_room_loading():
        """Test room loading performance"""
        rooms = ["office", "crime_scene", "lab"]
        times = []
        
        for room in rooms:
            start = time.time()
            load_room(room)
            end = time.time()
            times.append(end - start)
            print(f"Room {room} loaded in {end - start:.3f}s")
        
        avg_time = sum(times) / len(times)
        print(f"Average room load time: {avg_time:.3f}s")
    
    def stress_test_interactions():
        """Test rapid object interactions"""
        objects = get_room_objects()
        
        for obj_name in objects:
            for action in objects[obj_name].get('actions', []):
                start = time.time()
                execute_object_action(obj_name, action)
                end = time.time()
                print(f"Interaction {obj_name}.{action}: {end - start:.3f}s")
```

## Advanced Case Studies

### Case Study 1: Multi-Room Investigation System

This comprehensive example demonstrates a complete investigation system spanning multiple interconnected rooms with persistent state management.

#### Investigation State Manager

```python
# File: game/systems/investigation_manager.rpy

init python:
    class InvestigationManager:
        """Central manager for investigation progress across all rooms"""
        
        def __init__(self):
            self.case_files = {}
            self.evidence_connections = {}
            self.room_states = {}
            self.timeline = []
            self.breakthrough_thresholds = [3, 6, 9, 12]
            self.current_breakthroughs = 0
        
        def initialize_case(self, case_id):
            """Initialize a new case investigation"""
            self.case_files[case_id] = {
                "evidence": [],
                "suspects": [],
                "locations": [],
                "connections": {},
                "solved": False,
                "start_time": renpy.get_game_runtime()
            }
            
            # Initialize room access based on case
            if case_id == "missing_files":
                self.unlock_rooms(["detective_office", "evidence_room"])
            elif case_id == "murder_mystery":
                self.unlock_rooms(["crime_scene", "victim_apartment"])
        
        def add_evidence(self, case_id, evidence_id, room_id, method="found"):
            """Add evidence with full context tracking"""
            if case_id not in self.case_files:
                raise ValueError(f"Case {case_id} not initialized")
            
            case = self.case_files[case_id]
            evidence_entry = {
                "id": evidence_id,
                "room": room_id,
                "method": method,
                "timestamp": renpy.get_game_runtime(),
                "game_time": store.current_game_time if hasattr(store, 'current_game_time') else "unknown"
            }
            
            case["evidence"].append(evidence_entry)
            self.timeline.append(f"Evidence {evidence_id} found in {room_id}")
            
            # Check for breakthroughs
            self.check_breakthrough(case_id)
            
            # Auto-save progress
            self.save_investigation_state()
        
        def connect_evidence(self, case_id, evidence1, evidence2, connection_type="related"):
            """Create connections between pieces of evidence"""
            case = self.case_files.get(case_id)
            if not case:
                return
            
            connections = case.setdefault("connections", {})
            key = f"{evidence1}_{evidence2}"
            connections[key] = {
                "type": connection_type,
                "timestamp": renpy.get_game_runtime()
            }
            
            # Visual notification
            renpy.notify(f"Connection discovered: {evidence1} ↔ {evidence2}")
        
        def check_breakthrough(self, case_id):
            """Check if investigation has reached breakthrough thresholds"""
            case = self.case_files.get(case_id)
            if not case:
                return
            
            evidence_count = len(case["evidence"])
            
            for threshold in self.breakthrough_thresholds:
                if evidence_count >= threshold and self.current_breakthroughs < self.breakthrough_thresholds.index(threshold) + 1:
                    self.current_breakthroughs = self.breakthrough_thresholds.index(threshold) + 1
                    self.trigger_breakthrough(case_id, threshold)
                    break
        
        def trigger_breakthrough(self, case_id, threshold):
            """Handle investigation breakthroughs"""
            breakthrough_effects = {
                3: self.first_breakthrough,
                6: self.major_breakthrough,
                9: self.final_breakthrough,
                12: self.case_solution
            }
            
            effect_func = breakthrough_effects.get(threshold)
            if effect_func:
                effect_func(case_id)
        
        def first_breakthrough(self, case_id):
            """Handle first breakthrough - unlock new areas"""
            renpy.call("breakthrough_scene_1")
            
            if case_id == "missing_files":
                self.unlock_rooms(["interrogation_room", "archive_basement"])
            
            # Visual effects
            store.investigation_tension_level = 2
            self.update_atmospheric_effects()
        
        def major_breakthrough(self, case_id):
            """Handle major breakthrough - identify key suspects"""
            renpy.call("breakthrough_scene_2")
            
            # Enable confrontation options
            store.confrontation_available = True
            
            # Unlock final locations
            if case_id == "missing_files":
                self.unlock_rooms(["chief_office", "security_office"])
            
            store.investigation_tension_level = 3
            self.update_atmospheric_effects()
        
        def final_breakthrough(self, case_id):
            """Handle final breakthrough - case near resolution"""
            renpy.call("breakthrough_scene_3")
            
            # Dramatic visual effects
            store.investigation_tension_level = 4
            self.update_atmospheric_effects()
            
            # Enable final confrontation
            store.final_confrontation_ready = True
        
        def case_solution(self, case_id):
            """Handle case solution"""
            case = self.case_files[case_id]
            case["solved"] = True
            case["solution_time"] = renpy.get_game_runtime()
            
            renpy.call("case_solved_sequence")
        
        def unlock_rooms(self, room_ids):
            """Unlock new rooms for investigation"""
            newly_unlocked = []
            
            for room_id in room_ids:
                if room_id not in store.unlocked_rooms:
                    store.unlocked_rooms.append(room_id)
                    newly_unlocked.append(room_id)
            
            if newly_unlocked:
                rooms_str = ", ".join([r.replace("_", " ").title() for r in newly_unlocked])
                renpy.notify(f"New locations available: {rooms_str}")
        
        def update_atmospheric_effects(self):
            """Update visual atmosphere based on investigation tension"""
            tension = getattr(store, 'investigation_tension_level', 1)
            
            # Adjust global visual parameters
            effects_map = {
                1: {"film_grain": 0.1, "contrast": 1.0, "desaturation": 0.0},
                2: {"film_grain": 0.2, "contrast": 1.1, "desaturation": 0.1},
                3: {"film_grain": 0.3, "contrast": 1.2, "desaturation": 0.2},
                4: {"film_grain": 0.4, "contrast": 1.3, "desaturation": 0.3}
            }
            
            effects = effects_map.get(tension, effects_map[1])
            
            for param, value in effects.items():
                setattr(store, f"global_{param}_level", value)
            
            # Apply to current room if loaded
            if hasattr(store, 'current_room_id') and store.current_room_id:
                self.apply_room_atmosphere(store.current_room_id)
        
        def apply_room_atmosphere(self, room_id):
            """Apply tension-based atmosphere to specific room"""
            tension = getattr(store, 'investigation_tension_level', 1)
            
            # Room-specific atmosphere adjustments
            room_atmospheres = {
                "detective_office": {
                    1: "contemplative",
                    2: "focused",
                    3: "intense",
                    4: "climactic"
                },
                "evidence_room": {
                    1: "clinical",
                    2: "methodical",
                    3: "urgent",
                    4: "critical"
                },
                "crime_scene": {
                    1: "somber",
                    2: "investigative",
                    3: "revelatory",
                    4: "confrontational"
                }
            }
            
            atmosphere = room_atmospheres.get(room_id, {}).get(tension, "default")
            set_room_atmosphere(room_id, atmosphere)
        
        def save_investigation_state(self):
            """Save complete investigation state to persistent data"""
            persistent.investigation_manager_data = {
                "case_files": self.case_files,
                "evidence_connections": self.evidence_connections,
                "timeline": self.timeline,
                "current_breakthroughs": self.current_breakthroughs,
                "room_states": self.room_states
            }
        
        def load_investigation_state(self):
            """Load investigation state from persistent data"""
            if hasattr(persistent, 'investigation_manager_data') and persistent.investigation_manager_data:
                data = persistent.investigation_manager_data
                
                self.case_files = data.get("case_files", {})
                self.evidence_connections = data.get("evidence_connections", {})
                self.timeline = data.get("timeline", [])
                self.current_breakthroughs = data.get("current_breakthroughs", 0)
                self.room_states = data.get("room_states", {})
                
                return True
            return False
    
    # Global investigation manager instance
    investigation_manager = InvestigationManager()
    
    # Initialize default variables
    default unlocked_rooms = ["detective_office"]
    default investigation_tension_level = 1
    default confrontation_available = False
    default final_confrontation_ready = False
```

#### Cross-Room Evidence System

```python
# File: game/systems/evidence_system.rpy

init python:
    class EvidenceSystem:
        """Advanced evidence management with cross-room connections"""
        
        def __init__(self):
            self.evidence_types = {
                "document": {"icon": "📄", "color": "#FFFF88"},
                "physical": {"icon": "🔍", "color": "#88FFFF"},
                "testimony": {"icon": "🗣️", "color": "#FF88FF"},
                "digital": {"icon": "💾", "color": "#88FF88"}
            }
            
            self.evidence_database = {}
            self.connection_patterns = {}
        
        def register_evidence(self, evidence_id, evidence_data):
            """Register evidence with full metadata"""
            required_fields = ["name", "description", "type", "room_found"]
            
            for field in required_fields:
                if field not in evidence_data:
                    raise ValueError(f"Evidence {evidence_id} missing required field: {field}")
            
            self.evidence_database[evidence_id] = {
                **evidence_data,
                "id": evidence_id,
                "found_timestamp": renpy.get_game_runtime(),
                "connections": [],
                "analysis_level": 0,  # 0 = unexamined, 1 = basic, 2 = detailed, 3 = expert
                "relevance_score": self.calculate_relevance_score(evidence_data)
            }
        
        def calculate_relevance_score(self, evidence_data):
            """Calculate evidence relevance based on type and context"""
            base_score = 1.0
            
            # Type-based scoring
            type_scores = {
                "document": 1.2,
                "physical": 1.5,
                "testimony": 0.8,
                "digital": 1.3
            }
            
            score = base_score * type_scores.get(evidence_data.get("type"), 1.0)
            
            # Context-based adjustments
            if evidence_data.get("room_found") == "crime_scene":
                score *= 1.3
            elif evidence_data.get("room_found") == "suspects_room":
                score *= 1.1
            
            # Rarity adjustment
            if evidence_data.get("rarity", "common") == "rare":
                score *= 1.5
            elif evidence_data.get("rarity", "common") == "unique":
                score *= 2.0
            
            return round(score, 2)
        
        def analyze_evidence(self, evidence_id, analysis_method="basic"):
            """Perform evidence analysis with different methods"""
            evidence = self.evidence_database.get(evidence_id)
            if not evidence:
                return False
            
            analysis_methods = {
                "basic": self.basic_analysis,
                "detailed": self.detailed_analysis,
                "forensic": self.forensic_analysis,
                "digital": self.digital_analysis
            }
            
            method_func = analysis_methods.get(analysis_method)
            if method_func:
                return method_func(evidence_id)
            
            return False
        
        def basic_analysis(self, evidence_id):
            """Basic evidence examination"""
            evidence = self.evidence_database[evidence_id]
            
            if evidence["analysis_level"] >= 1:
                return {"result": "already_analyzed", "level": evidence["analysis_level"]}
            
            evidence["analysis_level"] = 1
            
            # Generate basic insights
            insights = []
            if evidence["type"] == "document":
                insights.append("Document appears authentic")
                insights.append("Contains handwritten notes")
            elif evidence["type"] == "physical":
                insights.append("Shows signs of recent handling")
                insights.append("No obvious damage")
            
            evidence["basic_insights"] = insights
            
            return {"result": "success", "insights": insights, "level": 1}
        
        def detailed_analysis(self, evidence_id):
            """Detailed evidence examination"""
            evidence = self.evidence_database[evidence_id]
            
            if evidence["analysis_level"] < 1:
                self.basic_analysis(evidence_id)
            
            if evidence["analysis_level"] >= 2:
                return {"result": "already_analyzed", "level": evidence["analysis_level"]}
            
            evidence["analysis_level"] = 2
            
            # Advanced insights based on evidence type and context
            advanced_insights = self.generate_advanced_insights(evidence)
            evidence["detailed_insights"] = advanced_insights
            
            # Check for connections to other evidence
            potential_connections = self.find_evidence_connections(evidence_id)
            
            return {
                "result": "success",
                "insights": advanced_insights,
                "connections": potential_connections,
                "level": 2
            }
        
        def generate_advanced_insights(self, evidence):
            """Generate context-specific advanced insights"""
            insights = []
            
            evidence_type = evidence["type"]
            room_found = evidence["room_found"]
            
            # Type and location specific insights
            insight_patterns = {
                ("document", "detective_office"): [
                    "Paper watermark matches department stationery",
                    "Ink analysis suggests recent creation"
                ],
                ("physical", "crime_scene"): [
                    "Fingerprint residue detected",
                    "Microscopic fibers present"
                ],
                ("digital", "suspects_room"): [
                    "File metadata shows recent modification",
                    "Digital signature validates authenticity"
                ]
            }
            
            pattern_key = (evidence_type, room_found)
            insights = insight_patterns.get(pattern_key, ["Further analysis required"])
            
            return insights
        
        def find_evidence_connections(self, evidence_id):
            """Find potential connections to other evidence"""
            evidence = self.evidence_database[evidence_id]
            connections = []
            
            for other_id, other_evidence in self.evidence_database.items():
                if other_id == evidence_id:
                    continue
                
                connection_score = self.calculate_connection_score(evidence, other_evidence)
                
                if connection_score > 0.5:
                    connections.append({
                        "evidence_id": other_id,
                        "score": connection_score,
                        "reason": self.determine_connection_reason(evidence, other_evidence)
                    })
            
            return sorted(connections, key=lambda x: x["score"], reverse=True)
        
        def calculate_connection_score(self, evidence1, evidence2):
            """Calculate likelihood of connection between two pieces of evidence"""
            score = 0.0
            
            # Same room bonus
            if evidence1["room_found"] == evidence2["room_found"]:
                score += 0.3
            
            # Same type bonus
            if evidence1["type"] == evidence2["type"]:
                score += 0.2
            
            # Temporal proximity (found within similar timeframe)
            time_diff = abs(evidence1["found_timestamp"] - evidence2["found_timestamp"])
            if time_diff < 300:  # 5 minutes
                score += 0.4
            elif time_diff < 900:  # 15 minutes
                score += 0.2
            
            # Content-based connections (if applicable)
            if self.check_content_similarity(evidence1, evidence2):
                score += 0.5
            
            return min(score, 1.0)
        
        def check_content_similarity(self, evidence1, evidence2):
            """Check for content-based similarities between evidence"""
            # Keywords that suggest connection
            connection_keywords = {
                "names": ["watson", "martinez", "johnson"],
                "locations": ["evidence_room", "archive", "basement"],
                "times": ["tuesday", "night", "2:47"]
            }
            
            desc1 = evidence1.get("description", "").lower()
            desc2 = evidence2.get("description", "").lower()
            
            for category, keywords in connection_keywords.items():
                for keyword in keywords:
                    if keyword in desc1 and keyword in desc2:
                        return True
            
            return False
        
        def determine_connection_reason(self, evidence1, evidence2):
            """Determine the reason for evidence connection"""
            reasons = []
            
            if evidence1["room_found"] == evidence2["room_found"]:
                reasons.append("Found in same location")
            
            if evidence1["type"] == evidence2["type"]:
                reasons.append("Similar evidence type")
            
            if self.check_content_similarity(evidence1, evidence2):
                reasons.append("Content references match")
            
            time_diff = abs(evidence1["found_timestamp"] - evidence2["found_timestamp"])
            if time_diff < 300:
                reasons.append("Found within minutes of each other")
            
            return "; ".join(reasons) if reasons else "General correlation"
        
        def create_evidence_network(self):
            """Create visual network of evidence connections"""
            network_data = {
                "nodes": [],
                "edges": []
            }
            
            # Add nodes for each piece of evidence
            for evidence_id, evidence in self.evidence_database.items():
                evidence_type = evidence["type"]
                type_info = self.evidence_types.get(evidence_type, {})
                
                network_data["nodes"].append({
                    "id": evidence_id,
                    "label": evidence["name"],
                    "type": evidence_type,
                    "icon": type_info.get("icon", "?"),
                    "color": type_info.get("color", "#FFFFFF"),
                    "relevance": evidence["relevance_score"]
                })
            
            # Add edges for connections
            for evidence_id, evidence in self.evidence_database.items():
                connections = self.find_evidence_connections(evidence_id)
                
                for connection in connections:
                    if connection["score"] > 0.6:  # Only strong connections
                        network_data["edges"].append({
                            "from": evidence_id,
                            "to": connection["evidence_id"],
                            "strength": connection["score"],
                            "reason": connection["reason"]
                        })
            
            return network_data
    
    # Global evidence system instance
    evidence_system = EvidenceSystem()
```

### Case Study 2: Dynamic Dialogue System with Relationship Tracking

This example shows a sophisticated dialogue system that adapts based on character relationships and investigation progress.

#### Advanced Character System

```python
# File: game/systems/character_system.rpy

init python:
    class CharacterRelationshipSystem:
        """Advanced character relationship and dialogue management"""
        
        def __init__(self):
            self.characters = {}
            self.relationship_modifiers = {
                "trust_gained": 0.1,
                "suspicion_raised": -0.15,
                "evidence_shown": 0.05,
                "lie_detected": -0.2,
                "help_provided": 0.2
            }
            self.dialogue_history = {}
            self.conversation_contexts = {}
        
        def register_character(self, char_id, character_data):
            """Register a character with full relationship tracking"""
            default_data = {
                "name": char_id.title(),
                "trust": 50,
                "suspicion": 0,
                "knowledge_level": 0,  # How much they know about the case
                "cooperation_level": 50,
                "personality_type": "neutral",  # cooperative, defensive, aggressive, secretive
                "secrets": [],
                "motivations": [],
                "dialogue_state": "initial",
                "topics_available": [],
                "evidence_reactions": {},
                "conversation_count": 0
            }
            
            self.characters[char_id] = {**default_data, **character_data}
            self.dialogue_history[char_id] = []
        
        def modify_relationship(self, char_id, modifier_type, amount=None):
            """Modify character relationship based on player actions"""
            if char_id not in self.characters:
                return False
            
            character = self.characters[char_id]
            
            if amount is None:
                amount = self.relationship_modifiers.get(modifier_type, 0)
            
            if modifier_type in ["trust_gained", "help_provided", "evidence_shown"]:
                character["trust"] = min(100, character["trust"] + (amount * 100))
            elif modifier_type in ["suspicion_raised", "lie_detected"]:
                character["suspicion"] = min(100, character["suspicion"] + (abs(amount) * 100))
                character["trust"] = max(0, character["trust"] - (abs(amount) * 50))
            
            # Update cooperation based on trust/suspicion balance
            trust_suspicion_balance = character["trust"] - character["suspicion"]
            character["cooperation_level"] = max(0, min(100, 50 + (trust_suspicion_balance * 0.5)))
            
            # Update personality response based on relationship changes
            self.update_personality_state(char_id)
            
            return True
        
        def update_personality_state(self, char_id):
            """Update character's personality state based on relationships"""
            character = self.characters[char_id]
            base_personality = character.get("base_personality", character["personality_type"])
            
            # Personality can shift based on trust/suspicion
            if character["suspicion"] > 70:
                character["personality_type"] = "hostile"
            elif character["trust"] > 80:
                character["personality_type"] = "cooperative"
            elif character["cooperation_level"] < 30:
                character["personality_type"] = "defensive"
            else:
                character["personality_type"] = base_personality
        
        def get_available_topics(self, char_id):
            """Get topics available for discussion based on character state and investigation progress"""
            character = self.characters.get(char_id)
            if not character:
                return []
            
            base_topics = character["topics_available"][:]
            dynamic_topics = []
            
            # Add topics based on evidence collected
            for evidence_id in store.evidence_collected:
                if self.character_knows_about_evidence(char_id, evidence_id):
                    topic_id = f"evidence_{evidence_id}"
                    if topic_id not in base_topics:
                        dynamic_topics.append(topic_id)
            
            # Add topics based on investigation progress
            if store.case_progress >= 5 and "case_theory" not in base_topics:
                dynamic_topics.append("case_theory")
            
            if character["suspicion"] > 50 and "confrontation" not in base_topics:
                dynamic_topics.append("confrontation")
            
            # Add topics based on other character interactions
            for other_char_id, other_char in self.characters.items():
                if other_char_id != char_id and other_char.get("conversation_count", 0) > 0:
                    topic_id = f"about_{other_char_id}"
                    if topic_id not in base_topics and self.should_discuss_character(char_id, other_char_id):
                        dynamic_topics.append(topic_id)
            
            return base_topics + dynamic_topics
        
        def character_knows_about_evidence(self, char_id, evidence_id):
            """Determine if character would know about specific evidence"""
            character = self.characters.get(char_id)
            if not character:
                return False
            
            # Check evidence database for character connections
            evidence = evidence_system.evidence_database.get(evidence_id)
            if not evidence:
                return False
            
            # Characters know about evidence from their own rooms
            character_rooms = character.get("associated_rooms", [])
            if evidence.get("room_found") in character_rooms:
                return True
            
            # Characters with high knowledge levels know more
            if character["knowledge_level"] >= 3:
                return True
            
            # Specific character-evidence relationships
            evidence_knowledge = character.get("evidence_knowledge", {})
            return evidence_knowledge.get(evidence_id, False)
        
        def should_discuss_character(self, asking_char_id, target_char_id):
            """Determine if one character would discuss another"""
            asking_char = self.characters.get(asking_char_id)
            target_char = self.characters.get(target_char_id)
            
            if not asking_char or not target_char:
                return False
            
            # Characters are more likely to discuss others they don't trust
            if target_char["suspicion"] > 40:
                return True
            
            # Characters with high cooperation discuss colleagues
            if asking_char["cooperation_level"] > 70:
                return True
            
            return False
        
        def generate_dialogue_response(self, char_id, topic, context=None):
            """Generate contextual dialogue response based on character state"""
            character = self.characters.get(char_id)
            if not character:
                return "I don't have anything to say."
            
            personality = character["personality_type"]
            cooperation = character["cooperation_level"]
            trust = character["trust"]
            suspicion = character["suspicion"]
            
            # Base response templates by personality and topic
            response_templates = self.get_response_templates()
            
            # Get base template
            template_key = f"{personality}_{topic}"
            if template_key not in response_templates:
                template_key = f"neutral_{topic}"
            
            template = response_templates.get(template_key, "I'm not sure about that.")
            
            # Modify based on relationship levels
            if cooperation < 30:
                template = self.make_response_uncooperative(template)
            elif trust > 80:
                template = self.make_response_helpful(template)
            
            # Track conversation
            self.record_dialogue(char_id, topic, template)
            
            return template
        
        def get_response_templates(self):
            """Get dialogue response templates organized by personality and topic"""
            return {
                # Cooperative responses
                "cooperative_case_progress": "I'm glad to see you're making progress on this case. Let me know if I can help further.",
                "cooperative_evidence_document": "Yes, I remember that document. It seemed important when I saw it.",
                "cooperative_about_martinez": "Martinez is a good officer. I've worked with him for years.",
                
                # Defensive responses
                "defensive_case_progress": "I've told you everything I know. I don't see how I can help more.",
                "defensive_evidence_document": "I don't know anything about that document. Should I?",
                "defensive_confrontation": "I don't like your tone. I'm trying to cooperate here.",
                
                # Hostile responses
                "hostile_case_progress": "Why are you still bothering me with this? I have work to do.",
                "hostile_evidence_document": "I don't have to answer questions about every piece of paper you find.",
                "hostile_confrontation": "Are you accusing me of something? Because if you are...",
                
                # Secretive responses
                "secretive_case_progress": "The case is... complicated. Some things are better left alone.",
                "secretive_evidence_document": "That document... where did you find it?",
                "secretive_about_watson": "The Chief has his reasons for things. It's not my place to question them."
            }
        
        def make_response_uncooperative(self, template):
            """Modify response to be less cooperative"""
            uncooperative_modifiers = [
                "I suppose... ",
                "Maybe... ",
                "I'm not sure I should say, but... ",
                "Against my better judgment... "
            ]
            
            import random
            modifier = random.choice(uncooperative_modifiers)
            return modifier + template.lower()
        
        def make_response_helpful(self, template):
            """Modify response to be more helpful"""
            helpful_additions = [
                " And I'll tell you something else - ",
                " You should also know that ",
                " Between you and me, ",
                " I probably shouldn't say this, but "
            ]
            
            import random
            addition = random.choice(helpful_additions)
            additional_info = self.get_additional_info(template)
            
            return template + addition + additional_info
        
        def get_additional_info(self, base_response):
            """Generate additional helpful information"""
            additional_info_pool = [
                "I saw some unusual activity that night.",
                "there were some discrepancies in the logs.",
                "Martinez seemed nervous about something.",
                "the Chief has been acting strange lately.",
                "I heard voices in the evidence room after hours."
            ]
            
            import random
            return random.choice(additional_info_pool)
        
        def record_dialogue(self, char_id, topic, response):
            """Record dialogue for history tracking"""
            if char_id not in self.dialogue_history:
                self.dialogue_history[char_id] = []
            
            self.dialogue_history[char_id].append({
                "topic": topic,
                "response": response,
                "timestamp": renpy.get_game_runtime(),
                "character_state": {
                    "trust": self.characters[char_id]["trust"],
                    "suspicion": self.characters[char_id]["suspicion"],
                    "cooperation": self.characters[char_id]["cooperation_level"]
                }
            })
            
            # Update conversation count
            self.characters[char_id]["conversation_count"] += 1
        
        def show_character_evidence(self, char_id, evidence_id):
            """Handle showing evidence to character with dynamic reactions"""
            character = self.characters.get(char_id)
            evidence = evidence_system.evidence_database.get(evidence_id)
            
            if not character or not evidence:
                return "No reaction."
            
            # Check if character has seen this evidence before
            evidence_shown = character.get("evidence_shown", [])
            
            if evidence_id in evidence_shown:
                return "You've already shown me that."
            
            # Add to shown evidence list
            evidence_shown.append(evidence_id)
            character["evidence_shown"] = evidence_shown
            
            # Generate reaction based on character's relationship to evidence
            reaction = self.generate_evidence_reaction(char_id, evidence_id)
            
            # Modify relationship based on evidence
            self.modify_relationship(char_id, "evidence_shown")
            
            # Special reactions for incriminating evidence
            if self.is_evidence_incriminating(char_id, evidence_id):
                self.modify_relationship(char_id, "suspicion_raised", 0.3)
                reaction += "\n\n*Their expression changes noticeably.*"
            
            return reaction
        
        def generate_evidence_reaction(self, char_id, evidence_id):
            """Generate character-specific evidence reactions"""
            character = self.characters[char_id]
            evidence = evidence_system.evidence_database[evidence_id]
            personality = character["personality_type"]
            
            # Base reactions by personality type
            personality_reactions = {
                "cooperative": "Interesting. Let me take a closer look at this.",
                "defensive": "I'm not sure what you want me to say about this.",
                "hostile": "So what? What does this prove?",
                "secretive": "Where... where did you get this?"
            }
            
            base_reaction = personality_reactions.get(personality, "I see.")
            
            # Add evidence-specific reactions
            evidence_reactions = character.get("evidence_reactions", {})
            specific_reaction = evidence_reactions.get(evidence_id)
            
            if specific_reaction:
                return specific_reaction
            
            return base_reaction
        
        def is_evidence_incriminating(self, char_id, evidence_id):
            """Check if evidence is incriminating for specific character"""
            character = self.characters.get(char_id)
            if not character:
                return False
            
            # Check character's secrets against evidence
            character_secrets = character.get("secrets", [])
            evidence = evidence_system.evidence_database.get(evidence_id, {})
            evidence_implications = evidence.get("implications", [])
            
            # Evidence is incriminating if it relates to character's secrets
            for secret in character_secrets:
                if secret in evidence_implications:
                    return True
            
            return False
    
    # Global character relationship system
    character_system = CharacterRelationshipSystem()
```

### Case Study 3: Performance-Optimized Visual Effects System

This example demonstrates advanced visual effects management with performance monitoring and adaptive quality settings.

#### Adaptive Visual Effects Manager

```python
# File: game/systems/effects_manager.rpy

init python:
    class AdaptiveEffectsManager:
        """Performance-aware visual effects management system"""
        
        def __init__(self):
            self.performance_metrics = {
                "frame_times": [],
                "effect_costs": {},
                "quality_level": "high",  # high, medium, low, minimal
                "target_fps": 60,
                "min_acceptable_fps": 30
            }
            
            self.effect_presets = {
                "high": {
                    "crt_enabled": True,
                    "film_grain_intensity": 0.4,
                    "letterbox_enabled": True,
                    "particle_count": 100,
                    "shader_quality": "full",
                    "anti_aliasing": True
                },
                "medium": {
                    "crt_enabled": True,
                    "film_grain_intensity": 0.2,
                    "letterbox_enabled": True,
                    "particle_count": 50,
                    "shader_quality": "reduced",
                    "anti_aliasing": False
                },
                "low": {
                    "crt_enabled": False,
                    "film_grain_intensity": 0.1,
                    "letterbox_enabled": False,
                    "particle_count": 20,
                    "shader_quality": "minimal",
                    "anti_aliasing": False
                },
                "minimal": {
                    "crt_enabled": False,
                    "film_grain_intensity": 0.0,
                    "letterbox_enabled": False,
                    "particle_count": 0,
                    "shader_quality": "none",
                    "anti_aliasing": False
                }
            }
            
            self.active_effects = []
            self.effect_queue = []
            self.performance_monitor_enabled = True
        
        def initialize_performance_monitoring(self):
            """Initialize performance monitoring system"""
            # Detect system capabilities
            self.detect_system_capabilities()
            
            # Set initial quality based on system
            self.set_initial_quality_level()
            
            # Start performance monitoring
            if self.performance_monitor_enabled:
                self.start_performance_monitoring()
        
        def detect_system_capabilities(self):
            """Detect system graphics capabilities"""
            # Basic capability detection based on renderer info
            renderer_info = renpy.get_renderer_info()
            
            capabilities = {
                "gpu_vendor": renderer_info.get("renderer", "unknown"),
                "opengl_version": renderer_info.get("version", "unknown"),
                "shader_support": "gl" in renderer_info.get("renderer", "").lower(),
                "mobile_device": renpy.mobile
            }
            
            self.performance_metrics["capabilities"] = capabilities
        
        def set_initial_quality_level(self):
            """Set initial quality level based on system capabilities"""
            capabilities = self.performance_metrics.get("capabilities", {})
            
            if capabilities.get("mobile_device"):
                self.performance_metrics["quality_level"] = "low"
            elif not capabilities.get("shader_support"):
                self.performance_metrics["quality_level"] = "minimal"
            else:
                # Start with high quality, will adjust based on performance
                self.performance_metrics["quality_level"] = "high"
        
        def start_performance_monitoring(self):
            """Start continuous performance monitoring"""
            renpy.call_in_new_context("performance_monitoring_loop")
        
        def monitor_frame_performance(self):
            """Monitor and record frame performance"""
            import time
            
            # Measure frame time
            current_time = time.time()
            if hasattr(self, '_last_frame_time'):
                frame_time = current_time - self._last_frame_time
                self.performance_metrics["frame_times"].append(frame_time)
                
                # Keep only recent measurements
                if len(self.performance_metrics["frame_times"]) > 60:
                    self.performance_metrics["frame_times"].pop(0)
                
                # Calculate average FPS
                avg_frame_time = sum(self.performance_metrics["frame_times"]) / len(self.performance_metrics["frame_times"])
                current_fps = 1.0 / max(avg_frame_time, 0.001)
                
                # Check if performance adjustment needed
                if current_fps < self.performance_metrics["min_acceptable_fps"]:
                    self.adjust_quality_for_performance()
            
            self._last_frame_time = current_time
        
        def adjust_quality_for_performance(self):
            """Automatically adjust quality settings based on performance"""
            current_quality = self.performance_metrics["quality_level"]
            quality_levels = ["high", "medium", "low", "minimal"]
            
            try:
                current_index = quality_levels.index(current_quality)
                if current_index < len(quality_levels) - 1:
                    new_quality = quality_levels[current_index + 1]
                    self.set_quality_level(new_quality)
                    renpy.notify(f"Graphics quality adjusted to {new_quality} for better performance")
            except ValueError:
                pass
        
        def set_quality_level(self, quality_level):
            """Set overall quality level and apply settings"""
            if quality_level not in self.effect_presets:
                return False
            
            self.performance_metrics["quality_level"] = quality_level
            settings = self.effect_presets[quality_level]
            
            # Apply all settings
            for setting, value in settings.items():
                self.apply_quality_setting(setting, value)
            
            # Save quality preference
            persistent.graphics_quality = quality_level
            
            return True
        
        def apply_quality_setting(self, setting, value):
            """Apply specific quality setting"""
            if setting == "crt_enabled":
                store.crt_enabled = value
            elif setting == "film_grain_intensity":
                store.film_grain_intensity = value
            elif setting == "letterbox_enabled":
                store.letterbox_default_enabled = value
            elif setting == "particle_count":
                store.max_particles = value
            elif setting == "shader_quality":
                store.shader_quality_level = value
            elif setting == "anti_aliasing":
                store.anti_aliasing_enabled = value
        
        def create_effect(self, effect_type, parameters, duration=None, priority=1):
            """Create visual effect with performance consideration"""
            current_quality = self.performance_metrics["quality_level"]
            
            # Skip expensive effects on low-end systems
            if current_quality in ["low", "minimal"] and effect_type in ["particle_system", "complex_shader"]:
                return None
            
            # Adjust parameters based on quality
            adjusted_params = self.adjust_parameters_for_quality(effect_type, parameters, current_quality)
            
            # Create effect object
            effect = {
                "type": effect_type,
                "parameters": adjusted_params,
                "duration": duration,
                "priority": priority,
                "start_time": renpy.get_game_runtime(),
                "active": True
            }
            
            # Add to active effects
            self.active_effects.append(effect)
            
            # Execute effect
            self.execute_effect(effect)
            
            return effect
        
        def adjust_parameters_for_quality(self, effect_type, parameters, quality_level):
            """Adjust effect parameters based on quality level"""
            adjusted = parameters.copy()
            
            quality_multipliers = {
                "high": 1.0,
                "medium": 0.7,
                "low": 0.4,
                "minimal": 0.1
            }
            
            multiplier = quality_multipliers.get(quality_level, 1.0)
            
            # Adjust intensity-based parameters
            intensity_params = ["intensity", "alpha", "strength", "amount"]
            for param in intensity_params:
                if param in adjusted:
                    adjusted[param] *= multiplier
            
            # Adjust count-based parameters
            count_params = ["particle_count", "iterations", "samples"]
            for param in count_params:
                if param in adjusted:
                    adjusted[param] = int(adjusted[param] * multiplier)
            
            return adjusted
        
        def execute_effect(self, effect):
            """Execute visual effect based on type"""
            effect_type = effect["type"]
            parameters = effect["parameters"]
            
            effect_executors = {
                "screen_flash": self.execute_screen_flash,
                "screen_shake": self.execute_screen_shake,
                "color_transition": self.execute_color_transition,
                "particle_system": self.execute_particle_system,
                "shader_effect": self.execute_shader_effect,
                "atmosphere_change": self.execute_atmosphere_change
            }
            
            executor = effect_executors.get(effect_type)
            if executor:
                executor(parameters)
        
        def execute_screen_flash(self, parameters):
            """Execute screen flash effect"""
            color = parameters.get("color", "#FFFFFF")
            intensity = parameters.get("intensity", 0.8)
            duration = parameters.get("duration", 0.1)
            
            renpy.show("flash_overlay", what=Solid(color), at_list=[
                Transform(alpha=0.0),
                linear(duration/2, alpha=intensity),
                linear(duration/2, alpha=0.0)
            ])
            
            # Auto-hide after effect
            renpy.call_screen("effect_timer", duration)
            renpy.hide("flash_overlay")
        
        def execute_screen_shake(self, parameters):
            """Execute screen shake effect"""
            intensity = parameters.get("intensity", 10)
            duration = parameters.get("duration", 0.5)
            frequency = parameters.get("frequency", 0.1)
            
            # Apply shake transform to current screen
            shake_transform = self.create_shake_transform(intensity, duration, frequency)
            renpy.show("screen", at_list=[shake_transform])
        
        def create_shake_transform(self, intensity, duration, frequency):
            """Create shake transform with specified parameters"""
            import random
            
            def shake_function(trans, st, at):
                if st > duration:
                    trans.xoffset = 0
                    trans.yoffset = 0
                    return None
                
                # Calculate shake offset
                shake_x = random.randint(-intensity, intensity)
                shake_y = random.randint(-intensity, intensity)
                
                trans.xoffset = shake_x
                trans.yoffset = shake_y
                
                return frequency
            
            return Transform(function=shake_function)
        
        def execute_color_transition(self, parameters):
            """Execute color transition effect"""
            from_color = parameters.get("from_color", "#FFFFFF")
            to_color = parameters.get("to_color", "#000000")
            duration = parameters.get("duration", 1.0)
            
            # Create color transition overlay
            renpy.show("color_transition", what=Solid(from_color), at_list=[
                Transform(alpha=0.5),
                linear(duration, matrixcolor=TintMatrix(to_color))
            ])
        
        def execute_atmosphere_change(self, parameters):
            """Execute atmospheric change effect"""
            atmosphere_type = parameters.get("type", "default")
            transition_duration = parameters.get("duration", 2.0)
            
            # Apply atmospheric changes gradually
            atmosphere_settings = self.get_atmosphere_settings(atmosphere_type)
            
            for setting, target_value in atmosphere_settings.items():
                current_value = getattr(store, setting, 0)
                self.animate_setting_change(setting, current_value, target_value, transition_duration)
        
        def get_atmosphere_settings(self, atmosphere_type):
            """Get settings for specific atmosphere type"""
            atmosphere_presets = {
                "tense": {
                    "film_grain_intensity": 0.4,
                    "contrast_level": 1.3,
                    "red_tint": 0.1
                },
                "calm": {
                    "film_grain_intensity": 0.1,
                    "contrast_level": 1.0,
                    "red_tint": 0.0
                },
                "dramatic": {
                    "film_grain_intensity": 0.5,
                    "contrast_level": 1.4,
                    "red_tint": 0.2
                }
            }
            
            return atmosphere_presets.get(atmosphere_type, {})
        
        def animate_setting_change(self, setting, from_value, to_value, duration):
            """Animate gradual change of setting value"""
            steps = int(duration * 10)  # 10 steps per second
            step_duration = duration / steps
            value_step = (to_value - from_value) / steps
            
            def animate_step(step):
                if step >= steps:
                    setattr(store, setting, to_value)
                    return
                
                current_value = from_value + (value_step * step)
                setattr(store, setting, current_value)
                
                renpy.call_screen("effect_timer", step_duration)
                animate_step(step + 1)
            
            animate_step(0)
        
        def cleanup_effects(self):
            """Clean up completed effects"""
            current_time = renpy.get_game_runtime()
            
            self.active_effects = [
                effect for effect in self.active_effects
                if effect.get("duration") is None or 
                   current_time - effect["start_time"] < effect["duration"]
            ]
        
        def get_performance_report(self):
            """Generate performance report"""
            if not self.performance_metrics["frame_times"]:
                return "No performance data available"
            
            avg_frame_time = sum(self.performance_metrics["frame_times"]) / len(self.performance_metrics["frame_times"])
            avg_fps = 1.0 / max(avg_frame_time, 0.001)
            
            report = f"""
Performance Report:
- Average FPS: {avg_fps:.1f}
- Quality Level: {self.performance_metrics['quality_level']}
- Active Effects: {len(self.active_effects)}
- System Type: {'Mobile' if renpy.mobile else 'Desktop'}
- Shader Support: {self.performance_metrics.get('capabilities', {}).get('shader_support', 'Unknown')}
"""
            
            return report
    
    # Global adaptive effects manager
    effects_manager = AdaptiveEffectsManager()
```

These comprehensive examples demonstrate the full power and flexibility of the Snatchernauts Framework, from basic room setup to sophisticated systems that handle complex game mechanics, character relationships, and performance optimization. Each example is production-ready and can be adapted for your specific game development needs.

