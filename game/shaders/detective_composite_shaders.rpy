# Detective Composite Shaders
# Combined shader effects for common detective game scenarios
#
# Overview
# - Pre-configured composite effects for atmosphere
# - Easy-to-use transforms for specific moods
# - Optimized layer combinations

# Combined effect transforms for common detective atmosphere combinations
transform detective_noir_atmosphere(grain_strength=0.15, sepia_strength=0.4, vignette=1.8):
    contains:
        At(Null(), film_grain_effect(grain_strength, 0.3))
    contains:
        At(Null(), vintage_sepia_effect(sepia_strength, 1.1, vignette))

transform foggy_night_scene(fog_density=0.4, light1_pos=(0.2, 0.1), light2_pos=(0.8, 0.3)):
    contains:
        At(Null(), atmospheric_fog_effect((0.1, 0.1, 0.2), fog_density, 1.8))
    contains:  
        At(Null(), dynamic_lighting_effect(light1_pos, light2_pos, 0.9, 0.5, 3.0, (1.0, 0.8, 0.6), 0.2))

transform rainy_detective_scene(rain_intensity=0.4, fog_density=0.2):
    contains:
        At(Null(), rain_effect(rain_intensity, 0.05, (0.7, 0.8, 0.9)))
    contains:
        At(Null(), atmospheric_fog_effect((0.4, 0.4, 0.5), fog_density, 1.2))
    contains:
        At(Null(), film_grain_effect(0.08, 0.15))

transform detective_investigation_mode(focus_point=(0.5, 0.5), reveal_progress=0.5):
    contains:
        At(Null(), depth_of_field_effect(focus_point, 0.4, 1.5))
    contains:
        At(Null(), color_grading_effect(0.0, 1.2, 0.9, 1.0, -0.1, (1.0, 0.95, 0.9)))
    contains:
        At(Null(), edge_detection_effect(0.3, (0.8, 0.9, 1.0), 0.15))

transform dark_room_exploration(flashlight_pos=(0.5, 0.5), flashlight_dir=(0.0, -1.0)):
    contains:
        At(Null(), flashlight_effect(flashlight_pos, flashlight_dir, 0.4, 0.6, 0.8, (1.0, 0.9, 0.7), 0.1))
    contains:
        At(Null(), color_grading_effect(-0.3, 1.5, 0.7, 1.2, 0.0, (0.8, 0.9, 1.1)))

transform evidence_highlight_mode():
    contains:
        At(Null(), edge_detection_effect(0.8, (1.0, 1.0, 0.5), 0.1))
    contains:
        At(Null(), color_grading_effect(0.1, 1.3, 1.2, 0.9, 0.0, (1.0, 1.0, 0.95)))

# Scene-specific atmosphere presets
transform crime_scene_atmosphere():
    contains:
        At(Null(), film_grain_effect(0.12, 0.25))
    contains:
        At(Null(), color_grading_effect(-0.05, 1.3, 0.8, 1.1, -0.2, (0.9, 0.95, 1.05)))
    contains:
        At(Null(), edge_detection_effect(0.4, (0.9, 0.9, 1.0), 0.12))

transform abandoned_building_atmosphere():
    contains:
        At(Null(), atmospheric_fog_effect((0.2, 0.2, 0.25), 0.3, 1.6))
    contains:
        At(Null(), vintage_sepia_effect(0.3, 1.2, 1.4))
    contains:
        At(Null(), dynamic_lighting_effect((0.1, 0.2), (0.9, 0.3), 0.4, 0.3, 4.0, (1.0, 0.8, 0.6), 0.1))

transform nighttime_street_atmosphere():
    contains:
        At(Null(), dynamic_lighting_effect((0.2, 0.1), (0.8, 0.1), 1.0, 0.8, 2.0, (1.0, 0.9, 0.7), 0.2))
    contains:
        At(Null(), atmospheric_fog_effect((0.3, 0.3, 0.4), 0.2, 1.0))
    contains:
        At(Null(), film_grain_effect(0.1, 0.2))

transform laboratory_atmosphere():
    contains:
        At(Null(), dynamic_lighting_effect((0.3, 0.2), (0.7, 0.2), 0.8, 0.6, 1.5, (0.9, 1.0, 1.2), 0.4))
    contains:
        At(Null(), color_grading_effect(0.05, 1.1, 1.05, 0.95, -0.3, (0.9, 0.95, 1.1)))
    contains:
        At(Null(), edge_detection_effect(0.2, (0.8, 1.0, 1.2), 0.18))

transform interrogation_room_atmosphere():
    contains:
        At(Null(), dynamic_lighting_effect((0.5, 0.1), (0.5, 0.1), 1.2, 0.0, 2.5, (1.0, 0.95, 0.85), 0.3))
    contains:
        At(Null(), vintage_sepia_effect(0.2, 1.4, 1.6))
    contains:
        At(Null(), film_grain_effect(0.08, 0.2))

transform warehouse_atmosphere():
    contains:
        At(Null(), atmospheric_fog_effect((0.25, 0.25, 0.3), 0.4, 2.0))
    contains:
        At(Null(), dynamic_lighting_effect((0.15, 0.15), (0.85, 0.2), 0.6, 0.4, 3.5, (1.0, 0.8, 0.6), 0.15))
    contains:
        At(Null(), color_grading_effect(-0.1, 1.4, 0.75, 1.15, 0.0, (0.95, 0.95, 1.0)))

transform office_atmosphere():
    contains:
        At(Null(), dynamic_lighting_effect((0.25, 0.1), (0.75, 0.1), 0.7, 0.5, 1.8, (1.0, 0.95, 0.9), 0.45))
    contains:
        At(Null(), color_grading_effect(0.02, 1.1, 0.95, 0.98, 0.1, (1.02, 1.0, 0.98)))
    contains:
        At(Null(), film_grain_effect(0.05, 0.15))

transform alley_atmosphere():
    contains:
        At(Null(), atmospheric_fog_effect((0.2, 0.2, 0.25), 0.35, 1.8))
    contains:
        At(Null(), dynamic_lighting_effect((0.1, 0.15), (0.9, 0.2), 0.5, 0.3, 4.0, (1.0, 0.85, 0.7), 0.12))
    contains:
        At(Null(), vintage_sepia_effect(0.25, 1.3, 1.5))
    contains:
        At(Null(), film_grain_effect(0.15, 0.3))

# Weather and time-specific combinations
transform stormy_night_atmosphere():
    contains:
        At(Null(), rain_effect(0.7, 0.2, (0.6, 0.7, 0.8)))
    contains:
        At(Null(), atmospheric_fog_effect((0.15, 0.15, 0.2), 0.5, 2.2))
    contains:
        At(Null(), dynamic_lighting_effect((0.2, 0.1), (0.8, 0.15), 0.4, 0.3, 5.0, (0.9, 0.9, 1.2), 0.08))
    contains:
        At(Null(), film_grain_effect(0.18, 0.35))

transform misty_morning_atmosphere():
    contains:
        At(Null(), atmospheric_fog_effect((0.7, 0.7, 0.75), 0.25, 1.4))
    contains:
        At(Null(), color_grading_effect(0.05, 1.05, 0.9, 0.95, 0.2, (1.05, 1.02, 0.95)))
    contains:
        At(Null(), film_grain_effect(0.06, 0.12))

transform sunset_atmosphere():
    contains:
        At(Null(), dynamic_lighting_effect((0.3, 0.2), (0.7, 0.3), 0.9, 0.7, 1.2, (1.2, 0.9, 0.6), 0.3))
    contains:
        At(Null(), color_grading_effect(0.03, 1.15, 1.1, 0.9, 0.4, (1.1, 1.0, 0.85)))
    contains:
        At(Null(), film_grain_effect(0.08, 0.18))

# Investigation-specific modes
transform evidence_analysis_mode():
    contains:
        At(Null(), depth_of_field_effect((0.5, 0.6), 0.3, 2.0))
    contains:
        At(Null(), edge_detection_effect(0.6, (1.0, 1.0, 0.7), 0.1))
    contains:
        At(Null(), color_grading_effect(0.1, 1.25, 1.15, 0.9, 0.0, (1.0, 1.0, 0.95)))

transform suspect_tracking_mode():
    contains:
        At(Null(), edge_detection_effect(0.5, (1.0, 0.8, 0.8), 0.12))
    contains:
        At(Null(), color_grading_effect(0.0, 1.2, 1.0, 1.0, -0.1, (1.0, 0.95, 0.95)))

transform memory_flashback_mode():
    contains:
        At(Null(), vintage_sepia_effect(0.6, 1.1, 1.2))
    contains:
        At(Null(), film_grain_effect(0.2, 0.4))
    contains:
        At(Null(), atmospheric_fog_effect((0.5, 0.5, 0.55), 0.15, 1.0))

transform revelation_moment_mode():
    contains:
        At(Null(), mystery_reveal_effect(0.0, (0.5, 0.5), 1.2, (0.0, 0.0, 0.0)))
    contains:
        At(Null(), edge_detection_effect(0.4, (1.0, 1.0, 0.9), 0.1))
    contains:
        At(Null(), color_grading_effect(0.05, 1.2, 1.1, 0.95, 0.0, (1.0, 1.0, 0.98)))
