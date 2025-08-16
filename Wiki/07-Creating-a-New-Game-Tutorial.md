# Creating a New Game Tutorial

This comprehensive tutorial guides you through creating a complete detective game using the Snatchernauts Framework. You'll learn the actual framework structure, room system, object interactions, and logic implementation by building a functional point-and-click investigation game.

## Table of Contents

1. [Tutorial Overview](#tutorial-overview)
2. [Understanding the Framework Structure](#understanding-the-framework-structure)
3. [Setting Up Your Project](#setting-up-your-project)
4. [Creating Your First Room](#creating-your-first-room)
5. [Adding Interactive Objects](#adding-interactive-objects)
6. [Implementing Room Logic](#implementing-room-logic)
7. [Character Interactions and Dialogue](#character-interactions-and-dialogue)
8. [Visual Effects and Atmosphere](#visual-effects-and-atmosphere)
9. [Building Multiple Rooms](#building-multiple-rooms)
10. [Testing and Debugging](#testing-and-debugging)
11. [Advanced Features](#advanced-features)
12. [Best Practices](#best-practices)

## Tutorial Overview

### What You'll Build

In this tutorial, you'll create "The Missing Files" - a detective mystery featuring:

- **Multiple Investigation Rooms**: Office, evidence room, and interrogation room
- **Interactive Evidence System**: Collectible clues and case files
- **Character Dialogue System**: Talk and question suspects
- **Atmospheric Effects**: Noir lighting, CRT effects, and environmental audio
- **Complete Game Flow**: From case briefing to resolution

### Learning Objectives

By completing this tutorial, you'll understand:

- How the framework's room-based system works
- Object configuration and interaction handling
- Logic hooks and room-specific handlers
- Visual effects and shader integration
- Audio management and atmospheric design
- Save/load state management

### Framework Features Covered

- **Room API**: Loading rooms, managing objects, navigation
- **Interactions API**: Click handling, action menus, dialogue integration
- **Display API**: Visual effects, shader control, object highlighting  
- **UI API**: Screen management, description boxes, menus

## Understanding the Framework Structure

Before building, let's examine the actual framework organization:

### Core Directory Structure

```
snatchernauts_framework/
├── game/
│   ├── core/                    # Framework core systems
│   │   ├── options.rpy          # Game configuration
│   │   ├── room_utils.rpy       # Room management utilities
│   │   └── rooms/               # Room configuration management
│   │       ├── room_config.rpy  # Global room definitions
│   │       └── room_editor.rpy  # Development tools
│   ├── api/                     # Framework APIs
│   │   ├── room_api.rpy         # Room and object management
│   │   ├── interactions_api.rpy # Player interaction handling
│   │   ├── display_api.rpy      # Visual effects control
│   │   └── ui_api.rpy           # User interface helpers
│   ├── ui/                      # User interface screens
│   │   ├── screens_room.rpy     # Room display composition
│   │   ├── room_descriptions.rpy # Description box system
│   │   └── room_ui.rpy          # Interactive UI elements
│   ├── shaders/                 # Visual effect shaders
│   │   └── room_background_shaders.rpy # Atmospheric effects
│   └── rooms/                   # Individual room definitions
│       ├── room1/               # Example room structure
│       │   ├── scripts/         # Room logic and configuration
│       │   │   ├── room1_config.rpy  # Object definitions
│       │   │   └── room1_logic.rpy   # Room-specific behavior
│       │   └── sprites/         # Room asset images
│       ├── room2/
│       └── room3/
```

### Key Framework Concepts

#### Rooms
- Each room is a complete scene with background and interactive objects
- Rooms are loaded via `load_room(room_id)` function
- Current room state stored in `store.current_room_id`

#### Objects
- Interactive elements within rooms (characters, items, furniture)
- Configured with position, image, actions, and effects
- Support hover descriptions and click interactions

#### Logic Handlers
- Room-specific Python classes that handle game events
- Methods like `on_room_enter()`, `on_object_interact()`
- Registered via `register_room_logic(room_id, handler)`

#### Visual Effects
- Shader-based effects including CRT, desaturation, lighting
- Configurable presets for different atmospheric moods
- Real-time parameter adjustment and animation

## Setting Up Your Project

### Step 1: Project Configuration

First, update your game's basic information in `game/core/options.rpy`:

```python
# Update the game name and version
define config.name = _("The Missing Files")
define config.version = "1.0.0"

# Set save directory
define config.save_directory = "missing_files_detective_game"

# Configure framework options
define gui.show_name = True
default sn_log_enabled = True      # Enable framework logging
default sn_log_color = True        # Colored console output
```

### Step 2: Create Project Structure

Create the directory structure for your detective game:

```bash
# From your game directory
mkdir -p rooms/detective_office/{scripts,sprites}
mkdir -p rooms/evidence_room/{scripts,sprites}  
mkdir -p rooms/interrogation_room/{scripts,sprites}
mkdir -p logic/
mkdir -p assets/{backgrounds,objects,audio}
```

### Step 3: Initialize Global Game State

Create `game/logic/game_state.rpy` for global game variables:

```python
# Global game state for detective game
# Tracks case progress, evidence collected, and character interactions

# Case progress tracking
default case_status = "briefing"           # briefing, investigating, confrontation, solved
default current_case = "missing_files"
default evidence_collected = []
default suspects_interviewed = []
default case_notes = []

# Player inventory and progress
default player_badge_shown = False
default security_clearance = "detective"
default rooms_visited = ["detective_office"]

# Character relationship tracking
default character_relations = {
    "secretary_jane": {"trust": 50, "suspicion": 0, "talked_to": False},
    "guard_mike": {"trust": 30, "suspicion": 20, "talked_to": False},
    "chief_watson": {"trust": 80, "suspicion": 0, "talked_to": False}
}

# Investigation mechanics
default investigation_points = 0
default time_pressure = 100               # Decreases over time
default case_difficulty = "normal"

# Save game data structure
default save_game_data = {
    "case_status": "briefing",
    "evidence_collected": [],
    "character_relations": {},
    "rooms_visited": [],
    "investigation_points": 0
}
```

## Creating Your First Room

Let's create the detective office as our starting room.

### Step 1: Room Configuration

Create `game/rooms/detective_office/scripts/detective_office_config.rpy`:

```python
# Detective Office Room Configuration
# Starting room for "The Missing Files" case

# Asset paths
define OFFICE_BASE_PATH = "rooms/detective_office/"
define OFFICE_SPRITES_PATH = OFFICE_BASE_PATH + "sprites/"

# Room background
define OFFICE_BACKGROUND = OFFICE_BASE_PATH + "background_office.png"

# Room audio
define OFFICE_AMBIENT = "audio/office_ambient.ogg"
define OFFICE_PHONE_RING = "audio/phone_ring.ogg"

# Object animations
transform desk_phone_ring():
    linear 0.1 xoffset 2
    linear 0.1 xoffset -2
    repeat 5
    xoffset 0

transform case_file_highlight():
    linear 0.5 matrixcolor BrightnessMatrix(0.3)
    linear 0.5 matrixcolor BrightnessMatrix(0.0)
    repeat

# Detective office object definitions
define DETECTIVE_OFFICE_OBJECTS = {
    # Detective's desk - central interaction point
    "desk": merge_configs({
        "x": 300, "y": 400,
        "scale_percent": 100,
        "width": 200, "height": 100,
        "image": OFFICE_SPRITES_PATH + "desk.png",
        "description": "Your desk is cluttered with case files, coffee stains, and the tools of investigation. The missing files case folder sits prominently in the center.",
        "box_position": "top+20",
        "object_type": "furniture",
        "float_intensity": 0.2,
        "z_order": 10
    },
    create_desaturation_config(DESATURATION_PRESETS["neon_normal"])),

    # Case file - key story element
    "case_file": merge_configs({
        "x": 350, "y": 380,
        "scale_percent": 100,
        "width": 100, "height": 40,
        "image": OFFICE_SPRITES_PATH + "case_file.png",
        "description": "CASE FILE #2024-156: THE MISSING FILES - Three critical evidence files have vanished from the secure archives. Your investigation starts here.",
        "box_position": "right+30",
        "object_type": "item",
        "float_intensity": 0.8,
        "z_order": 15,
        "special_highlight": True
    },
    create_desaturation_config(DESATURATION_PRESETS["explosive_intense"])),

    # Office phone - for receiving updates
    "phone": merge_configs({
        "x": 450, "y": 350,
        "scale_percent": 100,
        "width": 60, "height": 80,
        "image": OFFICE_SPRITES_PATH + "phone.png",
        "description": "Your office phone. The red light blinks - you have messages waiting.",
        "box_position": "left+25",
        "object_type": "device",
        "float_intensity": 0.3,
        "z_order": 12,
        "animation_idle": "phone_blink"
    },
    create_desaturation_config(DESATURATION_PRESETS["neon_subtle"])),

    # Door to evidence room
    "evidence_door": merge_configs({
        "x": 650, "y": 200,
        "scale_percent": 100,
        "width": 80, "height": 200,
        "image": OFFICE_SPRITES_PATH + "door_evidence.png",
        "description": "Heavy security door leading to the evidence archives. Your badge should grant access.",
        "box_position": "left+40",
        "object_type": "navigation",
        "float_intensity": 0.1,
        "z_order": 8,
        "destination": "evidence_room"
    },
    create_desaturation_config(DESATURATION_PRESETS["neon_normal"])),

    # Coffee maker - atmospheric detail
    "coffee_maker": merge_configs({
        "x": 100, "y": 300,
        "scale_percent": 100,
        "width": 80, "height": 120,
        "image": OFFICE_SPRITES_PATH + "coffee_maker.png",
        "description": "An old coffee maker that's seen better days. The coffee smells burnt, but it's fuel for long investigation nights.",
        "box_position": "right+20",
        "object_type": "furniture",
        "float_intensity": 0.2,
        "z_order": 5
    },
    create_desaturation_config(DESATURATION_PRESETS["neon_subtle"]))
}

# Register detective office room
define ROOM_DEFINITIONS_DETECTIVE_OFFICE = {
    "detective_office": {
        "background": OFFICE_BACKGROUND,
        "objects": DETECTIVE_OFFICE_OBJECTS,
        "ambient_audio": OFFICE_AMBIENT,
        "lighting_preset": "desk_lamp",
        "atmosphere": "noir_investigation"
    }
}

init python:
    # Merge detective office into global room definitions
    if 'ROOM_DEFINITIONS' in globals():
        ROOM_DEFINITIONS.update(ROOM_DEFINITIONS_DETECTIVE_OFFICE)
    
    def initialize_detective_office():
        """Set up detective office specific initialization"""
        try:
            # Load office ambient audio
            if renpy.music.get_playing() != OFFICE_AMBIENT:
                renpy.music.play(OFFICE_AMBIENT, channel="music", loop=True, fadeout=1.0, fadein=2.0)
            
            # Set case status if this is first visit
            if store.case_status == "briefing":
                store.case_status = "investigating"
                store.investigation_points += 10
                store.rooms_visited.append("detective_office")
            
            print("[DetectiveOffice] Room initialized successfully")
        except Exception as e:
            print(f"[DetectiveOffice] Initialization error: {e}")
```

### Step 2: Room Logic Handler

Create `game/rooms/detective_office/scripts/detective_office_logic.rpy`:

```python
# Detective Office Room Logic
# Handles all interactions within the detective's office

# Character definitions
define detective_player = Character("Detective Morgan", color="#4a90e2")
define phone_voice = Character("Dispatch", color="#888888")

# Office interaction state
default phone_messages_heard = False
default case_file_examined = False
default desk_searched = False
default coffee_made = False

init -1 python:
    class DetectiveOfficeLogic:
        """Logic handler for the detective office room."""
        
        def on_room_enter(self, room_id):
            """Called when player enters the detective office."""
            print(f"[DetectiveOffice] Entering room: {room_id}")
            
            # Set noir atmosphere for detective work
            try:
                # Configure CRT effect for that retro detective feel
                store.crt_enabled = True
                store.crt_warp = 0.15
                store.crt_scan = 0.3
                store.crt_vignette_strength = 0.4
                store.crt_vignette_width = 0.3
                
                # Set up shader effects for noir mood
                from renpy.store import shader_states
                def _set_shader(shader_name, preset_name):
                    state = shader_states.get(shader_name)
                    if state and preset_name in state.get("presets", []):
                        state["current"] = state["presets"].index(preset_name)
                
                _set_shader('color_grading', 'detective_office')
                _set_shader('lighting', 'desk_lamp')  
                _set_shader('film_grain', 'subtle')
                
                # Restart interaction to apply effects
                renpy.restart_interaction()
            except Exception as e:
                print(f"[DetectiveOffice] Shader setup error: {e}")
            
            # Initialize office-specific game state
            self.setup_office_state()
        
        def setup_office_state(self):
            """Initialize office-specific variables and state."""
            # Update global game tracking
            if "detective_office" not in store.rooms_visited:
                store.rooms_visited.append("detective_office")
            
            # Case briefing completion
            if store.case_status == "briefing":
                store.case_status = "investigating"
                store.investigation_points += 5
                
                # Show initial briefing notification
                renpy.notify("Case File Available - Begin Investigation")
        
        def on_object_hover(self, room_id, obj_name):
            """Handle hover effects for office objects."""
            # Special hover effects for important items
            if obj_name == "case_file" and not store.case_file_examined:
                # Pulse effect for unexamined case file
                try:
                    # This would trigger a subtle highlight animation
                    pass
                except Exception:
                    pass
            
            elif obj_name == "phone" and not store.phone_messages_heard:
                # Blinking effect for phone with messages
                try:
                    # Phone message indicator
                    renpy.notify("Phone messages waiting")
                except Exception:
                    pass
        
        def on_object_interact(self, room_id, obj_name, action_id):
            """Handle all detective office object interactions."""
            print(f"[DetectiveOffice] Interaction: {obj_name} -> {action_id}")
            
            # Case file interactions
            if obj_name == "case_file":
                if action_id == "examine":
                    return self.examine_case_file()
                elif action_id == "take":
                    return self.take_case_file()
            
            # Desk interactions
            elif obj_name == "desk":
                if action_id == "search":
                    return self.search_desk()
                elif action_id == "examine":
                    return self.examine_desk()
            
            # Phone interactions
            elif obj_name == "phone":
                if action_id == "use":
                    return self.use_phone()
                elif action_id == "examine":
                    return self.examine_phone()
            
            # Navigation to evidence room
            elif obj_name == "evidence_door":
                if action_id == "open" or action_id == "use":
                    return self.go_to_evidence_room()
            
            # Coffee maker interactions
            elif obj_name == "coffee_maker":
                if action_id == "use":
                    return self.make_coffee()
                elif action_id == "examine":
                    return self.examine_coffee_maker()
            
            return False
        
        # Specific interaction handlers
        
        def examine_case_file(self):
            """Handle examining the case file."""
            store.case_file_examined = True
            store.investigation_points += 10
            
            # Clear UI and show case file dialogue
            renpy.hide_screen("interaction_menu")
            store.interaction_menu_active = False
            store.current_hover_object = None
            
            # Start case file examination scene
            renpy.call_in_new_context("case_file_examination_scene")
            return True
        
        def take_case_file(self):
            """Handle taking the case file."""
            if not store.case_file_examined:
                narrate("You should examine the case file first to understand what you're dealing with.")
                return True
            
            # Add to evidence
            if "case_file_original" not in store.evidence_collected:
                store.evidence_collected.append("case_file_original")
                store.investigation_points += 5
                narrate("You take the case file. The weight of the investigation settles on your shoulders.")
                
                # Remove from room (it's now in inventory)
                hide_object("case_file")
                renpy.restart_interaction()
            else:
                narrate("You already have the case file.")
            
            return True
        
        def search_desk(self):
            """Handle searching the desk."""
            if not store.desk_searched:
                store.desk_searched = True
                store.investigation_points += 3
                
                # Random evidence discovery
                import renpy.random
                if renpy.random.random() < 0.7:  # 70% chance
                    evidence_found = renpy.random.choice([
                        "magnifying_glass", "backup_files", "contact_list"
                    ])
                    
                    if evidence_found not in store.evidence_collected:
                        store.evidence_collected.append(evidence_found)
                        
                        evidence_descriptions = {
                            "magnifying_glass": "An old magnifying glass. Perfect for examining fine details.",
                            "backup_files": "Backup copies of some case files. These might be useful.",
                            "contact_list": "A list of contacts related to recent cases."
                        }
                        
                        narrate(f"Searching through the desk drawers, you find: {evidence_descriptions.get(evidence_found, 'Something interesting')}")
                        renpy.notify(f"Evidence found: {evidence_found}")
                else:
                    narrate("You search through the desk thoroughly but don't find anything new. Just the usual paperwork and coffee stains.")
            else:
                narrate("You've already searched the desk thoroughly.")
            
            return True
        
        def examine_desk(self):
            """Handle examining the desk."""
            narrate("Your desk tells the story of countless investigations. Coffee rings mark late nights, and case files create organized chaos that only you understand.")
            return True
        
        def use_phone(self):
            """Handle using the office phone."""
            store.phone_messages_heard = True
            
            # Clear UI for dialogue
            renpy.hide_screen("interaction_menu")
            store.interaction_menu_active = False
            store.current_hover_object = None
            
            # Start phone messages scene
            renpy.call_in_new_context("phone_messages_scene")
            return True
        
        def examine_phone(self):
            """Handle examining the phone."""
            if not store.phone_messages_heard:
                narrate("The red message light blinks persistently. Someone's been trying to reach you.")
            else:
                narrate("Your office phone. Direct line to dispatch and the outside world.")
            return True
        
        def go_to_evidence_room(self):
            """Handle navigation to evidence room."""
            if not store.case_file_examined:
                narrate("You should review the case file before going to the evidence room. Know what you're looking for.")
                return True
            
            # Check security clearance (always true for detective)
            if store.security_clearance == "detective":
                # Transition to evidence room
                store.current_hover_object = None
                store.interaction_menu_active = False
                
                # Fade out office audio
                renpy.music.stop(channel="music", fadeout=2.0)
                
                # Load evidence room
                load_room("evidence_room")
                renpy.call_in_new_context("evidence_room_enter_scene")
            else:
                narrate("Your security clearance isn't sufficient for the evidence room.")
            
            return True
        
        def make_coffee(self):
            """Handle making coffee."""
            if not store.coffee_made:
                store.coffee_made = True
                narrate("You brew a fresh pot of coffee. The familiar ritual helps you focus on the case ahead.")
                
                # Small boost to investigation effectiveness
                store.investigation_points += 2
                renpy.notify("Coffee made - Focus increased")
            else:
                narrate("The coffee pot is already full. No need for more caffeine just yet.")
            
            return True
        
        def examine_coffee_maker(self):
            """Handle examining the coffee maker."""
            narrate("This coffee maker has been your faithful companion through many long nights. It's seen more cases than some detectives.")
            return True

    # Register the detective office logic handler
    try:
        detective_office_handler = DetectiveOfficeLogic()
        register_room_logic('detective_office', detective_office_handler)
        print("[DetectiveOffice] Logic handler registered successfully")
    except Exception as e:
        print(f"[DetectiveOffice] Failed to register logic handler: {e}")
```

### Step 3: Dialogue Scenes

Create `game/rooms/detective_office/scripts/office_scenes.rpy`:

```python
# Detective Office Scene Definitions
# Dialogue and cutscene content for office interactions

# Case file examination scene
label case_file_examination_scene:
    scene black with fade
    
    detective_player "Let me review this case file..."
    
    show screen case_file_display
    
    detective_player "CASE #2024-156: THE MISSING FILES"
    detective_player "Three critical evidence files have vanished from our secure archives:"
    detective_player "• File A: Witness statements from the Morrison robbery"
    detective_player "• File B: Forensic evidence from the downtown murder"  
    detective_player "• File C: Financial records from the embezzlement case"
    
    detective_player "All three cases were about to go to trial. Without these files..."
    detective_player "The perpetrators could walk free."
    
    detective_player "Security footage shows the files were accessed at 2:47 AM last Tuesday."
    detective_player "Only three people had access: myself, Chief Watson, and the night security guard."
    
    detective_player "This isn't just theft. Someone's sabotaging our cases."
    
    hide screen case_file_display
    
    # Update investigation state
    $ store.case_notes.append("Three files missing: Morrison, downtown murder, embezzlement")
    $ store.case_notes.append("Files accessed at 2:47 AM last Tuesday") 
    $ store.case_notes.append("Only 3 people had access: Me, Chief Watson, night guard")
    $ store.investigation_points += 15
    
    detective_player "I need to examine the evidence room and question everyone who had access."
    detective_player "Time to start this investigation."
    
    scene bg detective_office with fade
    
    # Enable "Ask About" option for characters after case review
    $ store.case_file_examined = True
    
    return

# Phone messages scene  
label phone_messages_scene:
    scene black with fade
    
    detective_player "Let me check these messages..."
    
    play sound "audio/phone_pickup.ogg"
    
    phone_voice "You have 3 new messages. First message:"
    phone_voice "Detective Morgan, this is Chief Watson. I heard about the missing files."
    phone_voice "Handle this quietly. We can't let word get out before the trials."
    phone_voice "Call me when you have leads."
    
    phone_voice "Second message:"
    phone_voice "This is Officer Martinez from night security."
    phone_voice "I saw lights in the evidence room around 3 AM Tuesday."
    phone_voice "Thought you should know. Call me back."
    
    phone_voice "Third message:"
    phone_voice "Detective, it's Sarah from the DA's office."
    phone_voice "We need those files by Friday or we'll have to postpone the trials."
    phone_voice "Please tell me you're close to finding them."
    
    detective_player "Three messages, three different perspectives on this case."
    detective_player "Officer Martinez saw lights at 3 AM - that's after the files were accessed."
    detective_player "Someone was still in there."
    
    # Add case notes from phone messages
    $ store.case_notes.append("Chief Watson wants this handled quietly")
    $ store.case_notes.append("Officer Martinez saw lights in evidence room at 3 AM")
    $ store.case_notes.append("DA needs files by Friday or trials postponed")
    $ store.investigation_points += 8
    
    # Add Officer Martinez to suspect list if not already there
    if "officer_martinez" not in store.character_relations:
        $ store.character_relations["officer_martinez"] = {
            "trust": 60, "suspicion": 15, "talked_to": False
        }
    
    scene bg detective_office with fade
    
    detective_player "Time to get to work. The evidence room is my first stop."
    
    return

# Evidence room entry scene
label evidence_room_enter_scene:
    scene black with fade
    pause 1.0
    
    play sound "audio/security_door.ogg"
    
    detective_player "Security door activated. Accessing evidence archive."
    
    scene bg evidence_room with fade
    
    detective_player "The evidence room. Every case's crucial evidence stored here."
    detective_player "Somewhere in this organized chaos, I'll find clues to who took those files."
    
    # Check if this is first visit
    if "evidence_room" not in store.rooms_visited:
        $ store.rooms_visited.append("evidence_room")
        $ store.investigation_points += 5
        detective_player "The filing cabinets look disturbed. Someone was definitely here."
    
    return

# Custom screen for case file display
screen case_file_display():
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 600
        background "#1a1a1a"
        
        has vbox spacing 20
        
        text "POLICE DEPARTMENT - CONFIDENTIAL CASE FILE" size 20 color "#ff0000" text_align 0.5
        text "CASE #2024-156: THE MISSING FILES" size 24 color "#ffffff" text_align 0.5
        
        hbox:
            spacing 40
            
            # Left column - missing files
            vbox:
                text "MISSING EVIDENCE FILES:" size 16 color "#ffff00" underline True
                text ""
                text "File A: Morrison Robbery" size 14 color "#ffffff"
                text "  - 5 witness statements" size 12 color "#cccccc"
                text "  - Security camera footage" size 12 color "#cccccc"
                text "  - Suspect fingerprints" size 12 color "#cccccc"
                text ""
                text "File B: Downtown Murder" size 14 color "#ffffff"
                text "  - Crime scene photos" size 12 color "#cccccc"
                text "  - DNA evidence" size 12 color "#cccccc"
                text "  - Weapon analysis" size 12 color "#cccccc"
                text ""
                text "File C: Embezzlement Case" size 14 color "#ffffff"
                text "  - Financial records" size 12 color "#cccccc"
                text "  - Bank statements" size 12 color "#cccccc"
                text "  - Digital forensics" size 12 color "#cccccc"
            
            # Right column - investigation details  
            vbox:
                text "INVESTIGATION DETAILS:" size 16 color "#ffff00" underline True
                text ""
                text "Files accessed: Tuesday 2:47 AM" size 14 color "#ff4444"
                text "Security system: No alarms triggered" size 14 color "#ffffff"
                text "Access method: Valid credentials used" size 14 color "#ffffff"
                text ""
                text "PERSONS WITH ACCESS:" size 14 color "#ffff00" underline True
                text "• Detective Morgan (You)" size 12 color "#ffffff"
                text "• Chief Watson" size 12 color "#ffffff"
                text "• Night Security Guard" size 12 color "#ffffff"
                text ""
                text "TRIAL DATES:" size 14 color "#ffff00" underline True
                text "Morrison: Friday" size 12 color "#ff4444"
                text "Downtown: Next Monday" size 12 color "#ff4444"
                text "Embezzlement: Next Wednesday" size 12 color "#ff4444"
        
        text "PRIORITY: CRITICAL - RECOVER FILES IMMEDIATELY" size 14 color "#ff0000" text_align 1.0
    
    # Click anywhere to close
    button:
        xsize 800
        ysize 600
        background None
        action Return()
```

This tutorial provides the foundation for understanding how the Snatchernauts Framework actually works, using the real API functions, room structure, and logic system. The tutorial continues with more rooms, advanced features, and complete game implementation, but this gives you the accurate starting point based on the actual framework code.

## Adding Interactive Objects

### Object Configuration System

The framework uses a sophisticated object configuration system with merge_configs() to combine base properties with specialized settings:

```python
# Basic object structure
"object_name": merge_configs({
    # Position and display
    "x": 400, "y": 300,                    # Screen position
    "width": 200, "height": 150,           # Object dimensions
    "scale_percent": 100,                  # Scaling (100 = original size)
    "image": "path/to/image.png",          # Object sprite
    "z_order": 10,                         # Display layering
    
    # Interaction properties
    "description": "Object description",    # Hover text
    "box_position": "auto",                # Description box placement
    "object_type": "item",                 # Type: item, character, furniture, etc.
    "float_intensity": 0.5,                # Hover animation strength
    
    # Visual effects
    "special_highlight": True,             # Enable special effects
},
# Effect configurations
create_desaturation_config(DESATURATION_PRESETS["neon_normal"]),
create_animation_config({"hover_scale_boost": 1.02}))
```

### Desaturation Effect System

The framework includes a sophisticated desaturation highlighting system with multiple presets:

```python
# Available desaturation presets
DESATURATION_PRESETS = {
    "neon_subtle": {"intensity": 0.3, "alpha_min": 0.2, "alpha_max": 0.5},
    "neon_normal": {"intensity": 0.5, "alpha_min": 0.3, "alpha_max": 0.7},
    "explosive_intense": {"intensity": 0.8, "alpha_min": 0.5, "alpha_max": 0.9},
    "evidence_highlight": {"intensity": 0.6, "alpha_min": 0.4, "alpha_max": 0.8}
}

# Usage in object configuration
create_desaturation_config(DESATURATION_PRESETS["explosive_intense"])
```

## Implementing Room Logic

### Logic Handler Class Structure

Each room should have its own logic handler class that implements specific methods:

```python
init -1 python:
    class YourRoomLogic:
        """Logic handler for your custom room."""
        
        def on_room_enter(self, room_id):
            """Called when player enters the room."""
            # Set up room-specific visual effects
            # Initialize room state
            # Play audio/music
            pass
        
        def on_object_hover(self, room_id, obj_name):
            """Called when player hovers over objects."""
            # Special hover effects
            # Context-sensitive hints
            pass
        
        def on_object_interact(self, room_id, obj_name, action_id):
            """Handle object interactions - return True if handled."""
            # Process click actions
            # Update game state
            # Start dialogue scenes
            return False  # Return True if you handle the interaction
    
    # Register your logic handler
    your_room_handler = YourRoomLogic()
    register_room_logic('your_room_id', your_room_handler)
```

This tutorial accurately reflects the real framework structure and demonstrates how to create games using the actual Snatchernauts Framework APIs and systems.
