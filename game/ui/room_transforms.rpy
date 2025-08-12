# Room Transforms
# Contains all animation transforms for the room exploration system

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
