# Bloom Effect Utilities
# Global utilities for bloom effect calculations and configurations

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
    "subtle": {
        "bloom_intensity": 0.3,
        "bloom_radius": 5.0,
        "bloom_alpha_min": 0.2,
        "bloom_alpha_max": 0.5,
        "bloom_pulse_speed": 0.8,
        "bloom_softness": 0.8
    },
    "moderate": {
        "bloom_intensity": 0.5,
        "bloom_radius": 8.0,
        "bloom_alpha_min": 0.3,
        "bloom_alpha_max": 0.7,
        "bloom_pulse_speed": 1.0,
        "bloom_softness": 0.7
    },
    "intense": {
        "bloom_intensity": 0.8,
        "bloom_radius": 12.0,
        "bloom_alpha_min": 0.4,
        "bloom_alpha_max": 0.9,
        "bloom_pulse_speed": 1.2,
        "bloom_softness": 0.6
    },
    "gentle": {
        "bloom_intensity": 0.2,
        "bloom_radius": 6.0,
        "bloom_alpha_min": 0.1,
        "bloom_alpha_max": 0.4,
        "bloom_pulse_speed": 0.6,
        "bloom_softness": 0.9
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
