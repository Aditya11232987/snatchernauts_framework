# Framework Examples

## Introduction

This page provides practical examples demonstrating how to use the Snatchernauts Framework's features. Examples are organized from simple to complex, with complete code samples you can adapt for your own projects.

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

These examples demonstrate the full range of capabilities available in the Snatchernauts Framework, from basic room setup to advanced interactive systems. Use them as starting points for your own implementations, adapting the patterns to fit your specific game's needs.

