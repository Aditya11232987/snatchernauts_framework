# Room1 Configuration and Initialization
# Comprehensive room setup including objects, sprites, animations, and assets
#
# Overview:
# - Defines all room1 objects with their properties
# - Sets up sprite animations and transforms
# - Configures audio assets (music, sfx, speech)
# - Manages room-specific visual effects

## Room1 Asset Paths
################################################################################

# Base path for room1 assets
define ROOM1_BASE_PATH = "rooms/room1/"

# Asset subdirectories
define ROOM1_SPRITES_PATH = ROOM1_BASE_PATH + "sprites/"
define ROOM1_AUDIO_PATH = ROOM1_BASE_PATH + "audio/"
define ROOM1_VIDEO_PATH = ROOM1_BASE_PATH + "video/"

# Audio subdirectories
define ROOM1_MUSIC_PATH = ROOM1_AUDIO_PATH + "music/"
define ROOM1_SFX_PATH = ROOM1_AUDIO_PATH + "sfx/"
define ROOM1_SPEECH_PATH = ROOM1_AUDIO_PATH + "speech/"

## Room1 Sprite Animations
################################################################################

# Detective sprite animations
transform detective_idle():
    # Subtle breathing animation
    linear 3.0 yoffset -2
    linear 3.0 yoffset 2
    repeat

transform detective_talk():
    # Slight head movement during conversation
    linear 1.5 xoffset -1 yoffset -1
    linear 1.5 xoffset 1 yoffset 1
    repeat

transform detective_investigate():
    # Looking around animation
    linear 2.0 xoffset -3
    linear 2.0 xoffset 3
    linear 2.0 xoffset 0
    repeat

# Patreon flyer animations
transform flyer_flutter():
    # Paper flutter effect
    linear 2.5 rotate 1
    linear 2.5 rotate -1
    repeat

transform flyer_highlight():
    # Glow effect when interacted with
    linear 0.5 matrixcolor BrightnessMatrix(0.2)
    linear 0.5 matrixcolor BrightnessMatrix(0.0)
    repeat 3

## Room1 Audio Configuration
################################################################################

# Background music for room1
define ROOM1_AMBIENT_MUSIC = ROOM1_MUSIC_PATH + "room1_ambient.ogg"
define ROOM1_TENSION_MUSIC = ROOM1_MUSIC_PATH + "room1_tension.ogg"

# Sound effects
define ROOM1_DETECTIVE_FOOTSTEPS = ROOM1_SFX_PATH + "footsteps_detective.ogg"
define ROOM1_PAPER_RUSTLE = ROOM1_SFX_PATH + "paper_rustle.ogg"
define ROOM1_DOOR_CREAK = ROOM1_SFX_PATH + "door_creak.ogg"

# Speech audio files for dialogue
define ROOM1_DETECTIVE_INTRO = ROOM1_SPEECH_PATH + "detective_intro.ogg"
define ROOM1_DETECTIVE_CASE = ROOM1_SPEECH_PATH + "detective_case_details.ogg"

## Room1 Object Definitions
################################################################################

# Enhanced object configuration with animations
define ROOM1_OBJECTS = {
    "detective": merge_configs({
        # Basic object properties
        "x": 211, "y": 124, 
        "scale_percent": 100,
        "width": 328,
        "height": 499,
        "image": ROOM1_SPRITES_PATH + "detective.png",
        "description": "Detective Blake stands with a weathered expression, investigating the mysterious disappearances. Years of experience show in every line on their face.",
        "box_position": "right",
        "float_intensity": 0.5,
        "object_type": "character",
        
        # Animation settings
        "idle_animation": "detective_idle",
        "talk_animation": "detective_talk",
        "investigate_animation": "detective_investigate",
        "current_animation": "detective_idle",
        
        # Audio settings
        "footstep_sound": ROOM1_DETECTIVE_FOOTSTEPS,
        "interaction_sounds": {
            "talk": ROOM1_DETECTIVE_INTRO,
            "ask_about": ROOM1_DETECTIVE_CASE
        },
        
        # State tracking
        "conversation_state": 0,
        "investigation_progress": 0,
        "trust_level": 0
    },
    # Bloom configuration
    create_bloom_config(BLOOM_PRESETS["neon_normal"]),
    # Animation configuration
    create_animation_config({
        "hover_scale_boost": 1.00,
        "hover_brightness_boost": 0.2
    })),

    "patreon": merge_configs({
        # Basic object properties
        "x": 690, "y": 167, 
        "scale_percent": 100,
        "width": 364,
        "height": 450,
        "image": ROOM1_SPRITES_PATH + "patreon.png",
        "description": "A mysterious flyer with strange symbols. It seems important to the investigation, though its purpose isn't immediately clear.",
        "box_position": "right+40",
        "float_intensity": 0.5,
        "object_type": "item",
        
        # Animation settings
        "idle_animation": "flyer_flutter",
        "highlight_animation": "flyer_highlight",
        "current_animation": "flyer_flutter",
        
        # Audio settings
        "interaction_sounds": {
            "take": ROOM1_PAPER_RUSTLE,
            "investigate": ROOM1_PAPER_RUSTLE
        },
        
        # Investigation properties
        "investigation_clues": [
            "Strange symbols that don't match any known language",
            "Paper feels unusually cold to the touch",
            "Faint scent of ozone emanates from the flyer"
        ],
        "clue_index": 0
    },
    # Bloom configuration
    create_bloom_config(BLOOM_PRESETS["neon_subtle"]),
    # Animation configuration
    create_animation_config({
        "hover_scale_boost": 1.00,
        "hover_brightness_boost": 0.0
    }))
}

## Room1 Environmental Effects
################################################################################

# Lighting configuration
define ROOM1_LIGHTING = {
    "ambient_light": 0.7,
    "shadow_intensity": 0.8,
    "light_temperature": "cool",  # cool/warm/neutral
    "flickering_lights": True,
    "flicker_intensity": 0.1
}

# Weather/atmosphere effects
define ROOM1_ATMOSPHERE = {
    "weather": "overcast",
    "wind_intensity": 0.3,
    "temperature_feel": "cold",
    "time_of_day": "late_afternoon"
}

## Room1 Initialization Functions
################################################################################

init python:
    def initialize_room1_objects():
        """Initialize all room1 objects with their animations and properties"""
        try:
            # Set up detective animations
            detective_obj = ROOM1_OBJECTS.get("detective", {})
            if detective_obj:
                # Apply idle animation by default
                detective_obj["transform"] = detective_idle()
            
            # Set up patreon flyer animations  
            patreon_obj = ROOM1_OBJECTS.get("patreon", {})
            if patreon_obj:
                # Apply flutter animation by default
                patreon_obj["transform"] = flyer_flutter()
            
            # Log successful initialization
            print("[Room1] Objects initialized successfully")
            
        except Exception as e:
            print(f"[Room1] Error initializing objects: {e}")
    
    def setup_room1_audio():
        """Set up room1 audio channels and preload sounds"""
        try:
            # Define room-specific audio channels
            renpy.music.register_channel("room1_ambient", "sfx", True)
            renpy.music.register_channel("room1_effects", "sfx", False)
            renpy.music.register_channel("room1_speech", "voice", False)
            
            # Preload frequently used sounds
            renpy.cache.preload(ROOM1_DETECTIVE_FOOTSTEPS)
            renpy.cache.preload(ROOM1_PAPER_RUSTLE)
            
            print("[Room1] Audio system initialized")
            
        except Exception as e:
            print(f"[Room1] Error setting up audio: {e}")
    
    def apply_room1_effects():
        """Apply room1 specific visual effects and lighting"""
        try:
            # Apply lighting configuration
            lighting = ROOM1_LIGHTING
            store.room_ambient_light = lighting["ambient_light"]
            store.room_shadow_intensity = lighting["shadow_intensity"]
            
            # Apply atmospheric effects based on configuration
            atmosphere = ROOM1_ATMOSPHERE
            if atmosphere["weather"] == "overcast":
                store.crt_vignette_strength = 0.95  # Stronger vignette for overcast
                
            if atmosphere["flickering_lights"]:
                # Enable subtle screen flicker effect
                store.crt_animated = True
                
            print("[Room1] Visual effects applied")
            
        except Exception as e:
            print(f"[Room1] Error applying effects: {e}")
    
    def switch_object_animation(obj_name, animation_name):
        """Switch an object to a different animation state"""
        try:
            if obj_name in ROOM1_OBJECTS:
                obj = ROOM1_OBJECTS[obj_name]
                if animation_name in obj:
                    obj["current_animation"] = animation_name
                    print(f"[Room1] Switched {obj_name} to {animation_name} animation")
                    return True
            return False
        except Exception as e:
            print(f"[Room1] Error switching animation: {e}")
            return False
    
    def play_room1_sfx(sound_name, channel="room1_effects"):
        """Play a room1 sound effect"""
        try:
            renpy.sound.play(sound_name, channel=channel)
        except Exception as e:
            print(f"[Room1] Error playing SFX: {e}")

## Room1 Integration with Main System
################################################################################

# Update the main room definition to use room1 objects
define ROOM_DEFINITIONS_ROOM1 = {
    "room1": {
        "background": ROOM1_SPRITES_PATH + "room1.png",
        "objects": ROOM1_OBJECTS,
        # Room-specific settings
        "initialization_func": initialize_room1_objects,
        "audio_setup_func": setup_room1_audio,
        "effects_func": apply_room1_effects,
        "music": ROOM1_AMBIENT_MUSIC,
        "ambient_channel": "room1_ambient"
    }
}

## Initialization Call
################################################################################

# Initialize room1 when this script loads
init python:
    # Call initialization functions
    initialize_room1_objects()
    setup_room1_audio()
    apply_room1_effects()
