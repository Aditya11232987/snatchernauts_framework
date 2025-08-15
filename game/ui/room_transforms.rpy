# Room Transforms
# Contains all animation transforms for the room exploration system
#
# Overview
# - Reusable transforms and helpers for floating descriptions and bloom.

init python:
    import hashlib

    def compute_float_phase(key, intensity=1.0, max_delay=0.8):
        """Deterministic per-key offsets and a small start delay.
        Produces mid-amplitude starting offsets so motion feels in-progress.
        """
        try:
            s = f"{key}|float_phase|{float(intensity):.3f}"
        except Exception:
            s = f"{key}|float_phase"
        h = hashlib.sha256(s.encode("utf-8")).hexdigest()

        def unit(idx):
            # 8 hex chars -> 32-bit int -> [0,1)
            return int(h[idx:idx+8], 16) / 0x100000000

        rx, ry, rr, rd = unit(0), unit(8), unit(16), unit(24)
        sx = -1 if int(h[32:34], 16) % 2 == 0 else 1
        sy = -1 if int(h[34:36], 16) % 2 == 0 else 1
        sr = -1 if int(h[36:38], 16) % 2 == 0 else 1

        amp_x = 8.0 * intensity
        amp_y = 6.0 * intensity
        amp_r = 1.5 * intensity

        # Start near mid amplitude (35%..65%) for a natural in-progress feel
        scale = lambda u: 0.35 + 0.30 * u
        x0 = sx * amp_x * scale(rx)
        y0 = sy * amp_y * scale(ry)
        r0 = sr * amp_r * scale(rr)
        delay = rd * max_delay
        return x0, y0, r0, delay

# Transform for dynamic floating animation of speech bubble with configurable intensity
transform floating_bubble(intensity=1.0, x0=0.0, y0=0.0, r0=0.0, start_delay=0.0):
    # Set initial offsets/rotation and wait a tiny per-instance delay
    xoffset x0
    yoffset y0
    rotate r0
    pause start_delay

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

# Mask-aligned bloom transform that creates feathered glow around object edges
transform mask_aligned_bloom(alpha_min=0.2, alpha_max=0.6, pulse_speed=2.0, intensity=0.5, bloom_color="#ffffff"):
    # Start from invisible
    alpha 0.0
    # Apply color tint and brightness boost
    matrixcolor TintMatrix(bloom_color) * BrightnessMatrix(intensity)
    # Add soft feathering with multiple blur layers for smooth edge transition
    blur 3  # Soft feathering around edges
    
    # Fade in to minimum bloom
    linear 0.3 alpha alpha_min
    # Pulse between min and max alpha
    block:
        linear pulse_speed alpha alpha_max
        linear pulse_speed alpha alpha_min
        repeat

# Enhanced mask-aligned bloom with multi-layer feathering for smoother edges
transform enhanced_mask_bloom(alpha_min=0.2, alpha_max=0.6, pulse_speed=2.0, intensity=0.5, bloom_color="#ffffff"):
    # Composite multiple layers for better feathering
    alpha 0.0
    matrixcolor TintMatrix(bloom_color) * BrightnessMatrix(intensity)
    
    # Multi-stage blur for smooth falloff
    # Inner glow (sharp)
    subpixel True
    blur 2
    
    # Fade in smoothly
    linear 0.3 alpha alpha_min
    # Smooth pulsing
    block:
        ease pulse_speed alpha alpha_max
        ease pulse_speed alpha alpha_min
        repeat

# Individual feathered bloom layer transform (used for multi-layer bloom)
transform feather_bloom_layer(alpha_min=0.2, alpha_max=0.6, pulse_speed=2.0, intensity=0.5, bloom_color="#ffffff", blur_amount=3):
    # Start invisible
    alpha 0.0
    # Apply subtle color tint and brightness - much more restrained
    matrixcolor TintMatrix(bloom_color) * BrightnessMatrix(intensity) * SaturationMatrix(0.8)
    # Apply the specified blur amount for this layer
    blur blur_amount
    # Enable subpixel positioning for smoother rendering and perfect alignment
    subpixel True
    # Ensure no offset issues
    anchor (0, 0)
    
    # Very smooth and slow fade in for subtlety
    ease 0.6 alpha alpha_min
    # Gentle, slow pulsing synchronized with other layers
    block:
        ease pulse_speed * 1.5 alpha alpha_max  # Slower pulse for more subtlety
        ease pulse_speed * 1.5 alpha alpha_min
        repeat

# Subtle edge highlight transform for outlining objects without obscuring them
transform subtle_edge_highlight(alpha_max=0.2, alpha_min=0.05, pulse_speed=2.0, bloom_color="#ffffff", blur_amount=2, offset=0):
    # Start completely invisible
    alpha 0.0
    # Use the highlight color with very subtle tinting - much more restrained
    matrixcolor TintMatrix(bloom_color) * BrightnessMatrix(0.6) * SaturationMatrix(0.9)
    # Light blur for soft edge without obscuring the object
    blur blur_amount
    # Perfect pixel alignment
    subpixel True
    anchor (0, 0)
    
    # Very slow, gentle fade in
    ease 1.2 alpha alpha_min
    # Extremely subtle, slow pulsing
    block:
        ease pulse_speed * 3.0 alpha alpha_max  # Even slower pulse
        ease pulse_speed * 3.0 alpha alpha_min
        repeat

# Desaturation highlight transform - desaturates and slightly darkens object for clear selection
transform object_desaturation_highlight(pulse_speed=2.0):
    # Start at normal saturation and brightness
    matrixcolor SaturationMatrix(1.0) * BrightnessMatrix(0.0)
    alpha 1.0
    subpixel True
    anchor (0, 0)
    
    # Initial transition to desaturated state matches pulse timing
    ease pulse_speed * 0.8 matrixcolor SaturationMatrix(0.3) * BrightnessMatrix(-0.08)  # Desaturate to 30% and slightly darken
    
    # Consistent pulsing between desaturated/dark and normal
    block:
        ease pulse_speed * 0.8 matrixcolor SaturationMatrix(1.0) * BrightnessMatrix(0.0)     # Back to normal
        ease pulse_speed * 0.8 matrixcolor SaturationMatrix(0.3) * BrightnessMatrix(-0.08)   # Desaturated and slightly dark again
        repeat

# Graceful desaturation fade-out transform - for when leaving an object during pulse animation
transform object_desaturation_fadeout(fade_duration=0.4):
    # This transform smoothly fades from whatever desaturated state back to normal
    # It's designed to be applied when unhover occurs during active pulsing
    alpha 1.0
    subpixel True
    anchor (0, 0)
    
    # Quick but smooth fade from current state to normal
    ease fade_duration matrixcolor SaturationMatrix(1.0) * BrightnessMatrix(0.0)

# Normal saturation reset transform - for objects that were never hovered or already normal
transform object_normal_saturation:
    # Instantly set to normal saturation and brightness for objects that should be normal
    matrixcolor SaturationMatrix(1.0) * BrightnessMatrix(0.0)
    alpha 1.0
    subpixel True
    anchor (0, 0)
