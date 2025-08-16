# Game Development Tutorial

**Part II: Core Development - Chapter 7**

*A comprehensive hands-on tutorial for creating complete interactive experiences using the Snatchernauts Framework. Master the framework through practical application by building "The Missing Files" - a complete detective mystery game.*

---

## Chapter Overview

This chapter provides a complete, hands-on tutorial for developing games with the Snatchernauts Framework. Rather than abstract concepts, you'll learn by building a fully functional detective mystery game that demonstrates every major framework system. This tutorial bridges the gap between understanding the framework's capabilities and actually implementing them in a production environment.

The tutorial is structured as a progressive development process, where each section builds upon previous work while introducing new framework concepts and techniques. By the end, you'll have created a complete game and gained deep practical knowledge of the framework's development patterns.

**What makes this tutorial comprehensive:**
- **Real-World Implementation**: Build an actual game, not just examples
- **Progressive Complexity**: Start simple, gradually add advanced features
- **Production Practices**: Learn proper code organization, testing, and optimization
- **Complete Coverage**: Touch every major framework system through practical application
- **Debugging Guidance**: Learn to troubleshoot common issues and optimize performance

**By the end of this chapter, you will have mastered:**
- Complete game development workflow using the framework
- Advanced room system implementation with complex state management
- Sophisticated object interaction patterns and dialogue systems
- Visual effects integration for atmospheric storytelling
- Audio design and dynamic music systems
- Save/load system implementation and state persistence
- Performance optimization and cross-platform compatibility
- Production deployment and distribution preparation

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

## Character Interactions and Dialogue

The framework's dialogue system integrates seamlessly with room logic and state management, allowing for complex character interactions that respond to investigation progress.

### Character Definition and State Tracking

```python
# Character definitions with relationship tracking
define chief_watson = Character("Chief Watson", color="#4a4a4a")
define officer_martinez = Character("Officer Martinez", color="#2a5a2a")
define secretary_jane = Character("Secretary Jane", color="#5a2a5a")

# Dynamic character state system
init python:
    class CharacterState:
        def __init__(self, name, trust=50, suspicion=0):
            self.name = name
            self.trust = trust
            self.suspicion = suspicion
            self.talked_to = False
            self.topics_discussed = []
            self.evidence_shown = []
            self.relationship_status = "neutral"  # neutral, trusted, suspicious, hostile
        
        def modify_trust(self, amount):
            self.trust = max(0, min(100, self.trust + amount))
            self.update_relationship_status()
        
        def modify_suspicion(self, amount):
            self.suspicion = max(0, min(100, self.suspicion + amount))
            self.update_relationship_status()
        
        def update_relationship_status(self):
            if self.suspicion > 70:
                self.relationship_status = "hostile"
            elif self.suspicion > 40:
                self.relationship_status = "suspicious"
            elif self.trust > 70:
                self.relationship_status = "trusted"
            else:
                self.relationship_status = "neutral"
```

### Context-Sensitive Dialogue Trees

Implement dialogue that changes based on evidence collected and investigation progress:

```python
# Evidence-aware dialogue system
label interrogate_chief_watson:
    scene black with fade
    
    # Dialogue changes based on evidence and relationship
    if store.character_relations["chief_watson"]["trust"] > 60:
        chief_watson "Detective Morgan, I'm glad you're handling this case personally."
    else:
        chief_watson "Detective. I trust you'll resolve this matter quickly and quietly."
    
    # Dynamic menu based on evidence collected
    menu:
        "Ask about file access" if "case_file_original" in store.evidence_collected:
            detective_player "Chief, I need to ask about access to the evidence files."
            
            if "security_logs" in store.evidence_collected:
                detective_player "The security logs show unusual activity Tuesday night."
                chief_watson "I was here late that night, reviewing case summaries."
                $ store.character_relations["chief_watson"]["suspicion"] += 10
            else:
                chief_watson "Of course. Only three people have access, including yourself."
        
        "Show evidence" if len(store.evidence_collected) > 2:
            call show_evidence_to_character("chief_watson") from _call_show_evidence_1
        
        "Ask about Officer Martinez" if "officer_martinez" in store.character_relations:
            detective_player "What can you tell me about Officer Martinez?"
            chief_watson "Good officer. Been with us for five years. Why do you ask?"
            
            if "martinez_message" in store.case_notes:
                detective_player "He left a message about seeing lights in the evidence room."
                chief_watson "Did he? That's... concerning. You should speak with him directly."
                $ store.investigation_points += 5
        
        "End conversation":
            detective_player "Thank you, Chief. I'll continue my investigation."
            $ store.character_relations["chief_watson"]["talked_to"] = True
            return
    
    jump interrogate_chief_watson

# Dynamic evidence presentation system
label show_evidence_to_character(character_name):
    "What evidence would you like to show?"
    
    # Build menu from collected evidence
    python:
        evidence_menu = []
        for evidence in store.evidence_collected:
            evidence_descriptions = {
                "case_file_original": "Original case file",
                "security_logs": "Security access logs",
                "backup_files": "Backup file copies",
                "contact_list": "Contact list"
            }
            desc = evidence_descriptions.get(evidence, evidence)
            evidence_menu.append((desc, evidence))
        
        if not evidence_menu:
            renpy.say(None, "You don't have any evidence to show.")
            return
    
    menu(evidence_menu):
        pass
    
    # Handle character reactions to specific evidence
    python:
        selected_evidence = _return
        character_state = store.character_relations.get(character_name, {})
        
        # Character-specific evidence reactions
        if character_name == "chief_watson":
            if selected_evidence == "security_logs":
                renpy.say(chief_watson, "These logs... where did you get these?")
                character_state["suspicion"] = character_state.get("suspicion", 0) + 15
            elif selected_evidence == "backup_files":
                renpy.say(chief_watson, "I didn't know we had backups of those files.")
                character_state["trust"] = character_state.get("trust", 50) + 5
        
        # Track what evidence was shown
        evidence_shown = character_state.get("evidence_shown", [])
        if selected_evidence not in evidence_shown:
            evidence_shown.append(selected_evidence)
            character_state["evidence_shown"] = evidence_shown
    
    return
```

## Visual Effects and Atmosphere

Integrate visual effects to enhance storytelling and create atmospheric immersion.

### Room-Specific Atmospheric Presets

```python
# Atmospheric configurations for different rooms
define ROOM_ATMOSPHERES = {
    "detective_office": {
        "color_grade": "detective_office",
        "lighting": "desk_lamp",
        "film_grain": 0.3,
        "crt_enabled": True,
        "letterbox": False,
        "mood": "contemplative"
    },
    "evidence_room": {
        "color_grade": "cold_fluorescent",
        "lighting": "overhead_harsh",
        "film_grain": 0.2,
        "crt_enabled": True,
        "letterbox": False,
        "mood": "clinical"
    },
    "interrogation_room": {
        "color_grade": "high_contrast",
        "lighting": "interrogation",
        "film_grain": 0.4,
        "crt_enabled": True,
        "letterbox": True,
        "mood": "tense"
    }
}

# Apply atmospheric presets based on story context
def set_room_atmosphere(room_id, intensity="normal"):
    """Apply atmospheric effects based on room and story context."""
    atmosphere = ROOM_ATMOSPHERES.get(room_id, {})
    
    # Modify intensity based on investigation progress
    tension_multiplier = 1.0
    if store.investigation_points > 50:
        tension_multiplier = 1.3
    elif store.investigation_points > 100:
        tension_multiplier = 1.5
    
    # Apply visual effects
    if atmosphere.get("color_grade"):
        set_color_grade(atmosphere["color_grade"])
    
    if atmosphere.get("lighting"):
        set_lighting(atmosphere["lighting"], intensity=tension_multiplier)
    
    # Film grain increases with tension
    if atmosphere.get("film_grain"):
        film_grain_intensity = atmosphere["film_grain"] * tension_multiplier
        set_film_grain(min(film_grain_intensity, 1.0))
    
    # CRT effects
    if atmosphere.get("crt_enabled"):
        store.crt_enabled = True
        store.crt_warp = 0.12 * tension_multiplier
        store.crt_scan = 0.25 + (0.1 * tension_multiplier)
    
    # Letterbox for dramatic scenes
    if atmosphere.get("letterbox") and intensity == "dramatic":
        enable_cinematic_mode()
```

### Dynamic Visual Feedback System

```python
# Visual feedback for investigation progress
def update_investigation_visuals():
    """Update visual effects based on case progress."""
    progress_ratio = store.investigation_points / 150.0  # Max expected points
    
    # Increase tension as case progresses
    if progress_ratio > 0.8:  # Near resolution
        # High tension visuals
        renpy.set_shader_parameter("atmosphere_shader", "u_red_tint", 0.15)
        renpy.set_shader_parameter("atmosphere_shader", "u_contrast", 1.4)
        store.film_grain_intensity = 0.5
    elif progress_ratio > 0.5:  # Mid investigation
        # Moderate tension
        renpy.set_shader_parameter("atmosphere_shader", "u_desaturation", 0.3)
        renpy.set_shader_parameter("atmosphere_shader", "u_contrast", 1.2)
        store.film_grain_intensity = 0.3
    
    # Update object highlighting based on relevance
    for obj_name, obj_config in current_room_objects.items():
        if is_evidence_relevant(obj_name):
            apply_desaturation_preset(obj_name, "explosive_intense")
        elif has_been_examined(obj_name):
            apply_desaturation_preset(obj_name, "whisper_subtle")

# Evidence relevance system
def is_evidence_relevant(obj_name):
    """Determine if object is currently relevant to investigation."""
    relevance_map = {
        "case_file": not store.case_file_examined,
        "phone": not store.phone_messages_heard,
        "security_terminal": "security_logs" not in store.evidence_collected,
        "filing_cabinet": store.case_status == "investigating"
    }
    
    return relevance_map.get(obj_name, False)
```

## Building Multiple Rooms

Expand the detective game with additional investigation locations.

### Evidence Room Implementation

Create `game/rooms/evidence_room/scripts/evidence_room_config.rpy`:

```python
# Evidence Room Configuration
# Secure storage for case evidence and files

define EVIDENCE_BASE_PATH = "rooms/evidence_room/"
define EVIDENCE_SPRITES_PATH = EVIDENCE_BASE_PATH + "sprites/"
define EVIDENCE_BACKGROUND = EVIDENCE_BASE_PATH + "background_evidence.png"
define EVIDENCE_AMBIENT = "audio/evidence_room_hum.ogg"

# Evidence room objects
define EVIDENCE_ROOM_OBJECTS = {
    # Main filing system
    "filing_cabinet_a": merge_configs({
        "x": 200, "y": 350,
        "width": 120, "height": 200,
        "image": EVIDENCE_SPRITES_PATH + "filing_cabinet_a.png",
        "description": "Filing Cabinet A-M: Contains case files for suspects with last names A through M. Several drawers appear to have been recently accessed.",
        "object_type": "storage",
        "contains_evidence": ["morrison_witness_statements", "alibis_archive"],
        "z_order": 10
    },
    create_desaturation_config(DESATURATION_PRESETS["evidence_highlight"])),
    
    # Security terminal
    "security_terminal": merge_configs({
        "x": 500, "y": 300,
        "width": 150, "height": 100,
        "image": EVIDENCE_SPRITES_PATH + "security_terminal.png",
        "description": "Security access terminal. Shows entry logs and access history. The screen displays recent activity.",
        "object_type": "device",
        "requires_clearance": True,
        "z_order": 12
    },
    create_desaturation_config(DESATURATION_PRESETS["neon_normal"])),
    
    # Evidence storage boxes
    "storage_boxes": merge_configs({
        "x": 600, "y": 400,
        "width": 100, "height": 80,
        "image": EVIDENCE_SPRITES_PATH + "storage_boxes.png",
        "description": "Sealed evidence storage boxes. Some seals appear broken or tampered with.",
        "object_type": "storage",
        "tampered": True,
        "z_order": 8
    },
    create_desaturation_config(DESATURATION_PRESETS["explosive_subtle"])),
    
    # Exit back to office
    "exit_door": merge_configs({
        "x": 50, "y": 200,
        "width": 80, "height": 200,
        "image": EVIDENCE_SPRITES_PATH + "door_exit.png",
        "description": "Exit back to the detective office.",
        "object_type": "navigation",
        "destination": "detective_office",
        "z_order": 5
    },
    create_desaturation_config(DESATURATION_PRESETS["neon_subtle"]))
}

# Register evidence room
define ROOM_DEFINITIONS_EVIDENCE_ROOM = {
    "evidence_room": {
        "background": EVIDENCE_BACKGROUND,
        "objects": EVIDENCE_ROOM_OBJECTS,
        "ambient_audio": EVIDENCE_AMBIENT,
        "lighting_preset": "cold_fluorescent",
        "atmosphere": "clinical_investigation"
    }
}

init python:
    if 'ROOM_DEFINITIONS' in globals():
        ROOM_DEFINITIONS.update(ROOM_DEFINITIONS_EVIDENCE_ROOM)
```

### Cross-Room State Management

Implement systems that track player actions across multiple rooms:

```python
# Global investigation state tracker
init python:
    class InvestigationTracker:
        def __init__(self):
            self.rooms_searched = set()
            self.evidence_chain = []  # Tracks order evidence was found
            self.timeline = []  # Investigation timeline
            self.breakthrough_moments = []
        
        def add_evidence(self, evidence_id, room_id, method="found"):
            """Add evidence with context tracking."""
            import time
            evidence_entry = {
                "id": evidence_id,
                "room": room_id,
                "method": method,
                "timestamp": time.time(),
                "investigation_points": store.investigation_points
            }
            
            self.evidence_chain.append(evidence_entry)
            self.timeline.append(f"Found {evidence_id} in {room_id}")
            
            # Check for breakthrough moments
            self.check_breakthroughs()
        
        def check_breakthroughs(self):
            """Identify key investigation breakthroughs."""
            evidence_count = len(store.evidence_collected)
            
            if evidence_count == 3 and "first_breakthrough" not in self.breakthrough_moments:
                self.breakthrough_moments.append("first_breakthrough")
                renpy.notify("Investigation Breakthrough: Pattern Emerging")
                # Trigger special visual effects
                update_investigation_visuals()
            
            elif evidence_count >= 6 and "major_breakthrough" not in self.breakthrough_moments:
                self.breakthrough_moments.append("major_breakthrough")
                renpy.notify("Major Breakthrough: Suspect Identified")
                # Enable new dialogue options
                self.enable_confrontation_dialogue()
        
        def enable_confrontation_dialogue(self):
            """Enable final confrontation options."""
            store.case_status = "confrontation"
            # Update all character relationship options
            for char_name in store.character_relations:
                store.character_relations[char_name]["confrontation_available"] = True
    
    # Initialize global tracker
    investigation_tracker = InvestigationTracker()
```

## Testing and Debugging

### Comprehensive Testing Framework

```python
# Testing and debugging utilities
init python:
    class GameTester:
        def __init__(self):
            self.test_results = []
            self.performance_metrics = {}
        
        def test_room_functionality(self, room_id):
            """Test all room interactions and state changes."""
            results = {"room_id": room_id, "tests": []}
            
            try:
                # Test room loading
                load_room(room_id)
                results["tests"].append({"test": "room_loading", "passed": True})
                
                # Test object interactions
                room_config = ROOM_DEFINITIONS.get(room_id, {})
                objects = room_config.get("objects", {})
                
                for obj_name in objects:
                    # Test hover functionality
                    try:
                        on_object_hover(room_id, obj_name)
                        results["tests"].append({"test": f"hover_{obj_name}", "passed": True})
                    except Exception as e:
                        results["tests"].append({"test": f"hover_{obj_name}", "passed": False, "error": str(e)})
                    
                    # Test interaction functionality
                    try:
                        on_object_interact(room_id, obj_name, "examine")
                        results["tests"].append({"test": f"interact_{obj_name}", "passed": True})
                    except Exception as e:
                        results["tests"].append({"test": f"interact_{obj_name}", "passed": False, "error": str(e)})
                        
            except Exception as e:
                results["tests"].append({"test": "room_loading", "passed": False, "error": str(e)})
            
            self.test_results.append(results)
            return results
        
        def test_investigation_flow(self):
            """Test complete investigation workflow."""
            # Reset game state
            self.reset_test_state()
            
            # Test progression through investigation stages
            test_stages = [
                {"action": lambda: self.simulate_case_file_examination(), "expected_status": "investigating"},
                {"action": lambda: self.simulate_evidence_collection(), "expected_points_min": 20},
                {"action": lambda: self.simulate_character_interviews(), "expected_relations_updated": True}
            ]
            
            for stage in test_stages:
                try:
                    stage["action"]()
                    # Validate expected outcomes
                    if "expected_status" in stage and store.case_status != stage["expected_status"]:
                        raise Exception(f"Expected status {stage['expected_status']}, got {store.case_status}")
                    if "expected_points_min" in stage and store.investigation_points < stage["expected_points_min"]:
                        raise Exception(f"Expected at least {stage['expected_points_min']} points, got {store.investigation_points}")
                except Exception as e:
                    print(f"Investigation flow test failed: {e}")
                    return False
            
            return True
        
        def reset_test_state(self):
            """Reset game state for testing."""
            store.case_status = "briefing"
            store.evidence_collected = []
            store.investigation_points = 0
            store.case_notes = []
            store.rooms_visited = []
        
        def simulate_case_file_examination(self):
            """Simulate examining the case file."""
            store.case_file_examined = True
            store.case_status = "investigating"
            store.investigation_points += 10
        
        def simulate_evidence_collection(self):
            """Simulate collecting evidence."""
            test_evidence = ["case_file_original", "security_logs", "backup_files"]
            for evidence in test_evidence:
                store.evidence_collected.append(evidence)
                store.investigation_points += 5
        
        def simulate_character_interviews(self):
            """Simulate interviewing characters."""
            for char_name in store.character_relations:
                store.character_relations[char_name]["talked_to"] = True
    
    # Initialize tester
    game_tester = GameTester()

# Debug console commands
label debug_menu:
    menu:
        "Test Current Room":
            python:
                results = game_tester.test_room_functionality(store.current_room_id)
                print(f"Room test results: {results}")
        
        "Test Investigation Flow":
            python:
                success = game_tester.test_investigation_flow()
                print(f"Investigation flow test: {'PASSED' if success else 'FAILED'}")
        
        "Show Game State":
            python:
                print(f"Case Status: {store.case_status}")
                print(f"Investigation Points: {store.investigation_points}")
                print(f"Evidence: {store.evidence_collected}")
                print(f"Rooms Visited: {store.rooms_visited}")
        
        "Reset Game State":
            python:
                game_tester.reset_test_state()
                renpy.notify("Game state reset for testing")
        
        "Exit Debug Menu":
            return
    
    jump debug_menu
```

### Performance Optimization

```python
# Performance monitoring and optimization
init python:
    class PerformanceMonitor:
        def __init__(self):
            self.frame_times = []
            self.shader_costs = {}
            self.room_load_times = {}
        
        def monitor_frame_performance(self):
            """Monitor frame rate performance."""
            import time
            start_time = time.time()
            
            # Your frame processing here
            
            frame_time = time.time() - start_time
            self.frame_times.append(frame_time)
            
            # Keep only recent measurements
            if len(self.frame_times) > 60:
                self.frame_times.pop(0)
            
            # Warn if performance drops
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            if avg_frame_time > 1/30:  # Below 30 FPS
                self.optimize_for_performance()
        
        def optimize_for_performance(self):
            """Apply performance optimizations."""
            # Reduce visual effects if performance is poor
            if store.film_grain_intensity > 0.3:
                store.film_grain_intensity = 0.2
                renpy.notify("Performance optimization: Reduced film grain")
            
            if store.crt_enabled and store.crt_scan > 0.2:
                store.crt_scan = 0.1
                renpy.notify("Performance optimization: Reduced CRT effects")
    
    performance_monitor = PerformanceMonitor()
```

## Advanced Features

### Save/Load System Integration

```python
# Advanced save/load with investigation state
init python:
    def save_investigation_state():
        """Save complete investigation state."""
        save_data = {
            "case_status": store.case_status,
            "investigation_points": store.investigation_points,
            "evidence_collected": store.evidence_collected[:],  # Copy list
            "case_notes": store.case_notes[:],
            "character_relations": dict(store.character_relations),  # Copy dict
            "rooms_visited": store.rooms_visited[:],
            "current_room": store.current_room_id,
            "visual_effects_state": {
                "crt_enabled": store.crt_enabled,
                "film_grain_intensity": getattr(store, 'film_grain_intensity', 0.0),
                "current_atmosphere": getattr(store, 'current_atmosphere', 'default')
            },
            "investigation_timeline": investigation_tracker.timeline[:],
            "breakthrough_moments": investigation_tracker.breakthrough_moments[:]
        }
        
        store.save_game_data = save_data
        return save_data
    
    def load_investigation_state(save_data):
        """Load complete investigation state."""
        if not save_data:
            return False
        
        try:
            # Restore game state
            store.case_status = save_data.get("case_status", "briefing")
            store.investigation_points = save_data.get("investigation_points", 0)
            store.evidence_collected = save_data.get("evidence_collected", [])
            store.case_notes = save_data.get("case_notes", [])
            store.character_relations = save_data.get("character_relations", {})
            store.rooms_visited = save_data.get("rooms_visited", [])
            
            # Restore visual effects
            visual_state = save_data.get("visual_effects_state", {})
            store.crt_enabled = visual_state.get("crt_enabled", True)
            store.film_grain_intensity = visual_state.get("film_grain_intensity", 0.0)
            
            # Restore investigation timeline
            if hasattr(investigation_tracker, 'timeline'):
                investigation_tracker.timeline = save_data.get("investigation_timeline", [])
                investigation_tracker.breakthrough_moments = save_data.get("breakthrough_moments", [])
            
            # Load the saved room
            saved_room = save_data.get("current_room", "detective_office")
            load_room(saved_room)
            
            return True
            
        except Exception as e:
            print(f"Error loading investigation state: {e}")
            return False

# Custom save/load screens with investigation preview
screen save_slot_investigation(slot):
    button:
        xsize 300
        ysize 150
        
        has vbox spacing 5
        
        # Standard save info
        text "[slot]" size 16
        text "[FileTime(slot)]" size 12
        
        # Investigation-specific info
        if FileSave(slot):
            $ save_data = FileJson(slot, "save_game_data", {})
            text "Case: [save_data.get('case_status', 'Unknown')]" size 12 color "#ffff00"
            text "Evidence: [len(save_data.get('evidence_collected', []))]" size 12 color "#00ff00"
            text "Points: [save_data.get('investigation_points', 0)]" size 12 color "#00ffff"
        
        action [
            FileAction(slot),
            Function(load_investigation_state, FileJson(slot, "save_game_data", {}))
        ]
```

## Best Practices

### Code Organization and Architecture

```
/game/
├── core/                           # Framework core (don't modify)
├── logic/                          # Game-specific logic
│   ├── game_state.rpy             # Global state management
│   ├── investigation_tracker.rpy   # Investigation-specific logic
│   └── character_manager.rpy       # Character relationship system
├── rooms/                          # Room-specific code
│   ├── detective_office/
│   │   ├── scripts/
│   │   │   ├── config.rpy          # Room configuration
│   │   │   ├── logic.rpy           # Room logic handler
│   │   │   └── scenes.rpy          # Dialogue and cutscenes
│   │   └── sprites/                # Room-specific assets
│   └── [other rooms]/
├── systems/                        # Game systems
│   ├── evidence_system.rpy         # Evidence collection and tracking
│   ├── dialogue_system.rpy         # Advanced dialogue features
│   └── atmosphere_system.rpy       # Visual atmosphere management
└── ui/                            # Custom UI components
    ├── investigation_ui.rpy        # Investigation-specific screens
    └── save_load_ui.rpy           # Custom save/load interface
```

### Performance Best Practices

1. **Efficient State Management**: Use dictionaries for fast lookups, avoid unnecessary list iterations
2. **Visual Effect Optimization**: Apply effects only when needed, disable during transitions
3. **Asset Management**: Preload critical assets, use appropriate image formats and sizes
4. **Memory Management**: Clean up temporary variables, avoid memory leaks in logic handlers

### Debugging and Troubleshooting

```python
# Comprehensive logging system
init python:
    import logging
    
    # Set up game-specific logger
    game_logger = logging.getLogger("MissingFiles")
    game_logger.setLevel(logging.DEBUG)
    
    def log_interaction(room_id, obj_name, action):
        game_logger.info(f"Interaction: {room_id}.{obj_name} -> {action}")
    
    def log_state_change(variable_name, old_value, new_value):
        game_logger.info(f"State change: {variable_name} {old_value} -> {new_value}")
    
    def log_investigation_progress(event_type, details):
        game_logger.info(f"Investigation: {event_type} - {details}")

# Error handling in room logic
def safe_room_interaction(room_id, obj_name, action):
    """Safely handle room interactions with error recovery."""
    try:
        return on_object_interact(room_id, obj_name, action)
    except Exception as e:
        game_logger.error(f"Interaction error: {room_id}.{obj_name}.{action} - {e}")
        renpy.notify(f"Interaction error: {str(e)[:50]}...")
        return False
```

---

## Recommended Learning Path

### Phase 1: Foundation (Basic Room and Object Setup)
- [ ] Complete the detective office room with all interactions
- [ ] Implement basic object highlighting and description system
- [ ] Test room navigation and state persistence
- [ ] Set up basic visual atmosphere and audio

### Phase 2: Expansion (Multiple Rooms and Complex Logic)
- [ ] Add evidence room with advanced object interactions
- [ ] Implement cross-room state management
- [ ] Create character dialogue system with relationship tracking
- [ ] Add investigation progress tracking and feedback

### Phase 3: Polish (Advanced Features and Optimization)
- [ ] Implement complete save/load system with investigation state
- [ ] Add performance monitoring and optimization
- [ ] Create comprehensive testing framework
- [ ] Design and implement final confrontation sequence

### Phase 4: Production (Testing, Distribution, and Deployment)
- [ ] Conduct thorough playtesting across different devices
- [ ] Optimize for various performance levels and screen sizes
- [ ] Prepare assets and build distribution packages
- [ ] Document code and create maintenance guides

---

## Next Steps

Having completed this comprehensive tutorial, you now have practical experience with every major aspect of the Snatchernauts Framework. The next chapters will help you refine and expand your development skills:

- **Chapter 8: Examples and Case Studies** - Additional game examples and advanced implementation patterns
- **Chapter 9: Build and Distribution** - Preparing your game for release across multiple platforms
- **Chapter 10-13: API References** - Detailed technical references for each framework API
- **Chapter 14: Developer Manual** - Advanced development techniques and framework customization
- **Chapter 15: Troubleshooting** - Common issues, solutions, and optimization strategies

This tutorial demonstrates the real-world application of framework concepts, providing you with both the theoretical understanding and practical experience needed to create compelling interactive experiences with the Snatchernauts Framework.

---

**Continue to:** [Chapter 8: Examples and Case Studies](08-Examples.md)
