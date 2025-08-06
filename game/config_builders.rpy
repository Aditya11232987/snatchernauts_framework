# Configuration Builder Utilities
# Functions for creating and merging object configurations

init python:
    def create_object_config(base_config, overrides=None):
        """Create object configuration by merging base config with overrides"""
        config = base_config.copy()
        if overrides:
            config.update(overrides)
        return config
    
    def create_bloom_config(overrides=None):
        """Create bloom configuration with optional overrides"""
        return create_object_config(DEFAULT_BLOOM_CONFIG, overrides)
    
    def create_animation_config(overrides=None):
        """Create animation configuration with optional overrides"""
        return create_object_config(DEFAULT_ANIMATION_CONFIG, overrides)
    
    def merge_configs(*configs):
        """Merge multiple configuration dictionaries"""
        result = {}
        for config in configs:
            if config:
                result.update(config)
        return result
