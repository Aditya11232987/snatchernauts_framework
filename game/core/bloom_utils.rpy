# Bloom Effect Utilities
# Global utilities for bloom effect calculations and configurations
#
# Overview
# - Computes bloom parameters/dimensions and presets.
# - Extracts colors via get_bloom_color in bloom_colors.rpy.
#
# Contracts
# - calculate_bloom_parameters(obj_config) -> dict
# - get_bloom_dimensions(obj_config) -> dict{x,y,width,height}
# - apply_bloom_to_object(obj_config, hover, obj_name) -> displayable data or None
# - BLOOM_PRESETS: preset dictionaries for common feel styles.

init python:
    def calculate_bloom_parameters(obj_config, scale_factor=None):
        """Calculate bloom effect parameters for an object"""
        if scale_factor is None:
            scale_factor = obj_config.get("scale_percent", 100) / 100.0
        
        bloom_radius = obj_config.get("bloom_radius", 8.0)
        bloom_softness = obj_config.get("bloom_softness", 0.7)
        
        # Calculate enhanced bloom parameters
        bloom_offset = max(1, int(bloom_radius * scale_factor))
        blur_amount = max(1, int(bloom_radius * bloom_softness))
        
        return {
            "bloom_offset": bloom_offset,
            "blur_amount": blur_amount,
            "bloom_intensity": obj_config.get("bloom_intensity", 0.5),
            "bloom_alpha_min": obj_config.get("bloom_alpha_min", 0.2),
            "bloom_alpha_max": obj_config.get("bloom_alpha_max", 0.6),
            "bloom_pulse_speed": obj_config.get("bloom_pulse_speed", 1.0),
            "bloom_threshold": obj_config.get("bloom_threshold", 0.05),
            "bloom_enabled": obj_config.get("bloom_enabled", True)
        }
    
    def get_bloom_dimensions(obj_config, bloom_offset=None):
        """Calculate bloom effect dimensions for positioning"""
        if bloom_offset is None:
            params = calculate_bloom_parameters(obj_config)
            bloom_offset = params["bloom_offset"]
        
        return {
            "x": obj_config["x"] - bloom_offset,
            "y": obj_config["y"] - bloom_offset,
            "width": obj_config["width"] + (bloom_offset * 2),
            "height": obj_config["height"] + (bloom_offset * 2)
        }
    
    def should_show_bloom(obj_config, hover_object=None, obj_name=None):
        """Check if bloom should be displayed for an object"""
        if not obj_config.get("bloom_enabled", True):
            return False
        
        # If hover_object is provided, check if this object is hovered
        if hover_object is not None and obj_name is not None:
            return hover_object == obj_name
        
        return True
    
    def create_bloom_config_dict(
        bloom_color="#ffffff", 
        bloom_intensity=0.5, 
        bloom_radius=8.0,
        bloom_threshold=0.05, 
        bloom_softness=0.7, 
        bloom_alpha_min=0.2, 
        bloom_alpha_max=0.6, 
        bloom_pulse_speed=1.0,
        bloom_enabled=True
    ):
        """Create a standardized bloom configuration dictionary"""
        return {
            "bloom_color": bloom_color,
            "bloom_intensity": bloom_intensity,
            "bloom_radius": bloom_radius,
            "bloom_threshold": bloom_threshold,
            "bloom_softness": bloom_softness,
            "bloom_alpha_min": bloom_alpha_min,
            "bloom_alpha_max": bloom_alpha_max,
            "bloom_pulse_speed": bloom_pulse_speed,
            "bloom_enabled": bloom_enabled
        }
    
    def apply_bloom_to_object(obj_config, current_hover_object=None, obj_name=None):
        """Apply bloom effect to an object configuration (returns displayable data)"""
        if not should_show_bloom(obj_config, current_hover_object, obj_name):
            return None
        
        # Get bloom color (extracted or fallback)
        fallback_color = obj_config.get("bloom_color", "#ffffff")
        bloom_color = get_bloom_color(obj_config["image"], fallback_color)
        
        # Calculate bloom parameters
        bloom_params = calculate_bloom_parameters(obj_config)
        bloom_dims = get_bloom_dimensions(obj_config, bloom_params["bloom_offset"])
        
        return {
            "image": obj_config["image"],
            "color": bloom_color,
            "dimensions": bloom_dims,
            "parameters": bloom_params
        }

# Bloom presets for common object types
define BLOOM_PRESETS = {
    # Original legacy presets (kept for compatibility)
    "subtle": {
        "bloom_intensity": 0.3,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 0.5,
        "bloom_pulse_speed": 0.8,
        "bloom_softness": 0.8,
        "bloom_fade_duration": 0.4
    },
    "moderate": {
        "bloom_intensity": 0.5,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 1.0,
        "bloom_softness": 0.7,
        "bloom_fade_duration": 0.3
    },
    "intense": {
        "bloom_intensity": 0.8,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.4,
        "bloom_alpha_max": 0.9,
        "bloom_pulse_speed": 1.2,
        "bloom_softness": 0.6,
        "bloom_fade_duration": 0.2
    },
    "gentle": {
        "bloom_intensity": 0.2,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.4,
        "bloom_pulse_speed": 0.6,
        "bloom_softness": 0.9,
        "bloom_fade_duration": 0.8
    },
    
    # EXPLOSIVE variants
    "explosive_subtle": {
        "bloom_intensity": 0.7,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 1.2,
        "bloom_softness": 0.6,
        "bloom_fade_duration": 0.15
    },
    "explosive_normal": {
        "bloom_intensity": 1.0,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.5,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 1.5,
        "bloom_softness": 0.5,
        "bloom_fade_duration": 0.1
    },
    "explosive_intense": {
        "bloom_intensity": 1.2,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.7,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 2.0,
        "bloom_softness": 0.4,
        "bloom_fade_duration": 0.05
    },
    
    # WHISPER variants
    "whisper_subtle": {
        "bloom_intensity": 0.1,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.02,
        "bloom_alpha_max": 0.15,
        "bloom_pulse_speed": 0.3,
        "bloom_softness": 0.98,
        "bloom_fade_duration": 1.2
    },
    "whisper_normal": {
        "bloom_intensity": 0.15,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.05,
        "bloom_alpha_max": 0.25,
        "bloom_pulse_speed": 0.4,
        "bloom_softness": 0.95,
        "bloom_fade_duration": 1.0
    },
    "whisper_intense": {
        "bloom_intensity": 0.25,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.4,
        "bloom_pulse_speed": 0.6,
        "bloom_softness": 0.9,
        "bloom_fade_duration": 0.8
    },
    
    # HEARTBEAT variants
    "heartbeat_subtle": {
        "bloom_intensity": 0.4,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.05,
        "bloom_alpha_max": 0.6,
        "bloom_pulse_speed": 1.5,
        "bloom_softness": 0.8
    },
    "heartbeat_normal": {
        "bloom_intensity": 0.6,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.8,
        "bloom_pulse_speed": 1.8,
        "bloom_softness": 0.7
    },
    "heartbeat_intense": {
        "bloom_intensity": 0.8,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 2.2,
        "bloom_softness": 0.6
    },
    
    # FLICKER variants
    "flicker_subtle": {
        "bloom_intensity": 0.5,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 2.0,
        "bloom_softness": 0.7
    },
    "flicker_normal": {
        "bloom_intensity": 0.7,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 0.9,
        "bloom_pulse_speed": 2.5,
        "bloom_softness": 0.6
    },
    "flicker_intense": {
        "bloom_intensity": 0.9,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 3.0,
        "bloom_softness": 0.5
    },
    
    # ETHEREAL variants
    "ethereal_subtle": {
        "bloom_intensity": 0.25,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.4,
        "bloom_pulse_speed": 0.5,
        "bloom_softness": 0.95
    },
    "ethereal_normal": {
        "bloom_intensity": 0.4,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.15,
        "bloom_alpha_max": 0.6,
        "bloom_pulse_speed": 0.7,
        "bloom_softness": 0.9
    },
    "ethereal_intense": {
        "bloom_intensity": 0.6,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.25,
        "bloom_alpha_max": 0.8,
        "bloom_pulse_speed": 0.9,
        "bloom_softness": 0.85
    },
    
    # LIGHTNING variants
    "lightning_subtle": {
        "bloom_intensity": 0.7,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.4,
        "bloom_alpha_max": 0.8,
        "bloom_pulse_speed": 2.5,
        "bloom_softness": 0.5
    },
    "lightning_normal": {
        "bloom_intensity": 0.9,
        "bloom_radius": 3.0,
        "bloom_alpha_min": 0.6,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 3.0,
        "bloom_softness": 0.4
    },
    "lightning_intense": {
        "bloom_intensity": 1.1,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.8,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 3.5,
        "bloom_softness": 0.3
    },
    
    # DREAM variants
    "dream_subtle": {
        "bloom_intensity": 0.2,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.05,
        "bloom_alpha_max": 0.3,
        "bloom_pulse_speed": 0.4,
        "bloom_softness": 0.98
    },
    "dream_normal": {
        "bloom_intensity": 0.3,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.5,
        "bloom_pulse_speed": 0.5,
        "bloom_softness": 0.95
    },
    "dream_intense": {
        "bloom_intensity": 0.5,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 0.7,
        "bloom_softness": 0.9
    },
    
    # EMBER variants
    "ember_subtle": {
        "bloom_intensity": 0.4,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 0.5,
        "bloom_pulse_speed": 1.0,
        "bloom_softness": 0.7
    },
    "ember_normal": {
        "bloom_intensity": 0.6,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 1.3,
        "bloom_softness": 0.6
    },
    "ember_intense": {
        "bloom_intensity": 0.8,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.4,
        "bloom_alpha_max": 0.9,
        "bloom_pulse_speed": 1.6,
        "bloom_softness": 0.5
    },
    
    # AURORA variants
    "aurora_subtle": {
        "bloom_intensity": 0.3,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.4,
        "bloom_pulse_speed": 0.6,
        "bloom_softness": 0.9
    },
    "aurora_normal": {
        "bloom_intensity": 0.5,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 0.6,
        "bloom_pulse_speed": 0.8,
        "bloom_softness": 0.85
    },
    "aurora_intense": {
        "bloom_intensity": 0.7,
        "bloom_radius": 6.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.8,
        "bloom_pulse_speed": 1.0,
        "bloom_softness": 0.8
    },
    
    # CRYSTAL variants
    "crystal_subtle": {
        "bloom_intensity": 0.5,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.6,
        "bloom_pulse_speed": 0.9,
        "bloom_softness": 0.8
    },
    "crystal_normal": {
        "bloom_intensity": 0.7,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.4,
        "bloom_alpha_max": 0.8,
        "bloom_pulse_speed": 1.1,
        "bloom_softness": 0.75
    },
    "crystal_intense": {
        "bloom_intensity": 0.9,
        "bloom_radius": 6.0,
        "bloom_alpha_min": 0.5,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 1.3,
        "bloom_softness": 0.7
    },
    
    # PHANTOM variants
    "phantom_subtle": {
        "bloom_intensity": 0.15,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.02,
        "bloom_alpha_max": 0.25,
        "bloom_pulse_speed": 0.5,
        "bloom_softness": 0.95
    },
    "phantom_normal": {
        "bloom_intensity": 0.25,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.05,
        "bloom_alpha_max": 0.4,
        "bloom_pulse_speed": 0.6,
        "bloom_softness": 0.9
    },
    "phantom_intense": {
        "bloom_intensity": 0.4,
        "bloom_radius": 6.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.6,
        "bloom_pulse_speed": 0.8,
        "bloom_softness": 0.85
    },
    
    # NEON variants
    "neon_subtle": {
        "bloom_intensity": 0.6,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 1.2,
        "bloom_softness": 0.6
    },
    "neon_normal": {
        "bloom_intensity": 0.8,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.5,
        "bloom_alpha_max": 0.9,
        "bloom_pulse_speed": 1.4,
        "bloom_softness": 0.5
    },
    "neon_intense": {
        "bloom_intensity": 1.0,
        "bloom_radius": 6.0,
        "bloom_alpha_min": 0.7,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 1.6,
        "bloom_softness": 0.4
    },
    
    # CANDLE variants
    "candle_subtle": {
        "bloom_intensity": 0.3,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.4,
        "bloom_pulse_speed": 0.7,
        "bloom_softness": 0.85
    },
    "candle_normal": {
        "bloom_intensity": 0.4,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 0.6,
        "bloom_pulse_speed": 0.9,
        "bloom_softness": 0.8
    },
    "candle_intense": {
        "bloom_intensity": 0.6,
        "bloom_radius": 6.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.8,
        "bloom_pulse_speed": 1.1,
        "bloom_softness": 0.75
    },
    
    # STARLIGHT variants
    "starlight_subtle": {
        "bloom_intensity": 0.25,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.05,
        "bloom_alpha_max": 0.35,
        "bloom_pulse_speed": 0.5,
        "bloom_softness": 0.95
    },
    "starlight_normal": {
        "bloom_intensity": 0.35,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.5,
        "bloom_pulse_speed": 0.7,
        "bloom_softness": 0.9
    },
    "starlight_intense": {
        "bloom_intensity": 0.5,
        "bloom_radius": 6.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 0.9,
        "bloom_softness": 0.85,
        "bloom_fade_duration": 0.6
    },
    
    # VOLCANIC variants
    "volcanic_subtle": {
        "bloom_intensity": 0.7,
        "bloom_radius": 2.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 1.3,
        "bloom_softness": 0.7
    },
    "volcanic_normal": {
        "bloom_intensity": 0.9,
        "bloom_radius": 4.0,
        "bloom_alpha_min": 0.4,
        "bloom_alpha_max": 0.95,
        "bloom_pulse_speed": 1.6,
        "bloom_softness": 0.6
    },
    "volcanic_intense": {
        "bloom_intensity": 1.1,
        "bloom_radius": 6.0,
        "bloom_alpha_min": 0.6,
        "bloom_alpha_max": 1.0,
        "bloom_pulse_speed": 2.0,
        "bloom_softness": 0.5
    }
}

init python:
    def apply_bloom_preset(obj_config, preset_name):
        """Apply a bloom preset to an object configuration"""
        if preset_name in BLOOM_PRESETS:
            preset = BLOOM_PRESETS[preset_name]
            for key, value in preset.items():
                obj_config[key] = value
        return obj_config
