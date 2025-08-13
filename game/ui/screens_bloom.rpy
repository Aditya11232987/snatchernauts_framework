# Bloom Effect Screens
#
# Overview
# - Renders bloom overlays for hovered objects, inside or outside CRT path.

# Internal bloom effects screen (used inside CRT frame)
screen room_bloom_effects_internal():
    if current_hover_object and current_hover_object in room_objects:
        $ bloom_data = apply_bloom_to_object(room_objects[current_hover_object], current_hover_object, current_hover_object)
        if bloom_data:
            add bloom_data["image"] at configurable_bloom(
                bloom_data["parameters"]["bloom_alpha_min"],
                bloom_data["parameters"]["bloom_alpha_max"],
                1.0/bloom_data["parameters"]["bloom_pulse_speed"]
            ):
                xpos bloom_data["dimensions"]["x"]
                ypos bloom_data["dimensions"]["y"]
                xsize bloom_data["dimensions"]["width"]
                ysize bloom_data["dimensions"]["height"]
                matrixcolor TintMatrix(bloom_data["color"]) * BrightnessMatrix(bloom_data["parameters"]["bloom_intensity"])
                blur bloom_data["parameters"]["blur_amount"]
                alpha bloom_data["parameters"]["bloom_alpha_max"] * room_objects[current_hover_object].get("bloom_softness", 0.7)

# External bloom effects screen (legacy/fallback for no CRT)
screen room_bloom_effects():
    if not (hasattr(store, 'crt_enabled') and store.crt_enabled):
        use room_bloom_effects_internal
