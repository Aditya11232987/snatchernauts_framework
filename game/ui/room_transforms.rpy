# Room Transforms
# Contains all animation transforms for the room exploration system

# Transform for dynamic floating animation of speech bubble with configurable intensity
transform floating_bubble(intensity=1.0):
    # Multi-directional floating motion scaled by intensity
    parallel:
        ease 1.8 xoffset -(8 * intensity)
        ease 1.8 xoffset (8 * intensity)
        repeat
    parallel:
        ease 2.2 yoffset -(6 * intensity)
        ease 2.2 yoffset (6 * intensity)
        repeat
    parallel:
        # Subtle rotation for more organic feel scaled by intensity
        ease 3.0 rotate -(1.5 * intensity)
        ease 3.0 rotate (1.5 * intensity)
        repeat

# Static transform for no floating (when intensity is 0)
transform no_float:
    pass

# Configurable bloom transform with fade-in and natural fade-out
transform configurable_bloom(alpha_min=0.2, alpha_max=0.6, pulse_speed=2.0):
    # Start from completely normal (no bloom)
    alpha 0.0
    # Fade in to minimum bloom over 0.3 seconds
    linear 0.3 alpha alpha_min
    # Then start the normal pulsing cycle between min and max (never back to 0)
    block:
        linear pulse_speed alpha alpha_max
        linear pulse_speed alpha alpha_min
        repeat

# Bloom transform with graceful fade-out - simple approach with default dissolve
transform bloom_with_fadeout(alpha_min=0.2, alpha_max=0.6, pulse_speed=2.0):
    # Start from completely normal (no bloom)
    alpha 0.0
    # Fade in to minimum bloom over 0.3 seconds
    linear 0.3 alpha alpha_min
    # Then start the normal pulsing cycle between min and max
    block:
        linear pulse_speed alpha alpha_max
        linear pulse_speed alpha alpha_min
        repeat

# Pulsing border transform for interaction buttons
transform pulsing_border:
    alpha 1.0
    block:
        linear 0.8 alpha 0.3
        linear 0.8 alpha 1.0
        repeat

# Static border transform for non-selected buttons
transform static_border:
    alpha 1.0
