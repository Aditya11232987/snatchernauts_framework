# Room Display Screens (Room & Objects)
#
# Overview
# - Composes background, objects, bloom, and CRT into the exploration scene.
# - Honors fade-in state and routes object display via display_api helpers.

# Common utilities are loaded by Ren'Py loader already.

# Display configuration
define ROOM_DISPLAY_CONFIG = {
    "fallback_background_color": "#000000",
    "default_background": "images/room1.png",
    "fade_duration": 2.0
}

# Transforms
transform room_fade_in(duration=2.0):
    alpha 0.0
    ease duration alpha 1.0

transform room_no_fade():
    alpha 1.0

transform room_fade_out(duration=2.0):
    alpha 1.0
    ease duration alpha 0.0

transform black_background():
    alpha 1.0

init python:
    # Display helpers live in api/display_api.rpy
    pass

# Combined screen for room background and objects
screen room_background_and_objects():
    $ room_has_faded_in = getattr(store, 'room_has_faded_in', False)
    if not room_has_faded_in:
        timer ROOM_DISPLAY_CONFIG["fade_duration"] action SetVariable('room_has_faded_in', True)

    if hasattr(store, 'crt_enabled') and store.crt_enabled:
        $ crt_warp = getattr(store, 'crt_warp', 0.2)
        $ crt_scan = getattr(store, 'crt_scan', 0.5)
        $ crt_chroma = getattr(store, 'crt_chroma', 0.9)
        $ crt_scanline_size = getattr(store, 'crt_scanline_size', 1.0)
        $ crt_vignette_strength = getattr(store, 'crt_vignette_strength', 0.35)
        $ crt_vignette_width = getattr(store, 'crt_vignette_width', 0.25)
        $ crt_animated = getattr(store, 'crt_animated', False)
        frame at (animated_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size, vignette_strength=crt_vignette_strength, vignette_width=crt_vignette_width) if crt_animated else static_chroma_crt(crt_warp, crt_scan, crt_chroma, crt_scanline_size, vignette_strength=crt_vignette_strength, vignette_width=crt_vignette_width)):
            background None
            add get_fallback_background() at black_background()
            if not room_has_faded_in:
                add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
            else:
                add get_room_background() at room_no_fade()
            for obj_name, obj_data in room_objects.items():
                if should_display_object(obj_data) and not is_object_hidden(obj_data):
                    $ props = get_object_display_properties(obj_data)
                    if not room_has_faded_in:
                        add props["image"] at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]):
                            xpos props["xpos"]
                            ypos props["ypos"]
                            xsize props["xsize"]
                            ysize props["ysize"]
                    else:
                        add props["image"] at room_no_fade():
                            xpos props["xpos"]
                            ypos props["ypos"]
                            xsize props["xsize"]
                            ysize props["ysize"]
            use room_bloom_effects_internal
    else:
        add get_fallback_background() at black_background()
        if not room_has_faded_in:
            add get_room_background() at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"])
        else:
            add get_room_background() at room_no_fade()
        for obj_name, obj_data in room_objects.items():
            if should_display_object(obj_data) and not is_object_hidden(obj_data):
                $ props = get_object_display_properties(obj_data)
                if not room_has_faded_in:
                    add props["image"] at room_fade_in(ROOM_DISPLAY_CONFIG["fade_duration"]):
                        xpos props["xpos"]
                        ypos props["ypos"]
                        xsize props["xsize"]
                        ysize props["ysize"]
                else:
                    add props["image"] at room_no_fade():
                        xpos props["xpos"]
                        ypos props["ypos"]
                        xsize props["xsize"]
                        ysize props["ysize"]
        use room_bloom_effects_internal

screen room_background():
    use room_background_and_objects

screen room_objects():
    pass

# Main exploration composition screen (easy to edit)
screen room_exploration():
    # Lock input until the initial fade completes
    $ input_locked = not room_has_faded_in
    # Room background and objects on the same layer
    use room_background_and_objects
    use room_bloom_effects

    # Interactive elements
    if not input_locked:
        use object_hotspots

    # Description system - show floating descriptions on hover
    if (not input_locked) and current_hover_object and not interaction_menu_active:
        $ obj = room_objects[current_hover_object]
        $ box_width, box_height = calculate_description_box_size(obj["description"])
        $ position_setting = obj.get("box_position", "auto")
        $ box_x, box_y, box_position = calculate_box_position(obj, box_width, box_height, position_setting)
        $ float_intensity = obj.get("float_intensity", 1.0)
        use floating_description_box(obj, box_width, box_height, box_x, box_y, float_intensity)

    # UI and debug overlays
    if not input_locked:
        use room_ui_buttons
    # Debug overlay is registered as an overlay screen; no need to include here
    use info_overlay

    # Keyboard navigation for interaction menus
    if (not input_locked) and interaction_menu_active:
        key "K_UP" action Function(navigate_interaction_menu, "up")
        key "K_DOWN" action Function(navigate_interaction_menu, "down")
        key "K_RETURN" action Function(execute_selected_action)
        key "K_ESCAPE" action Function(keyboard_cancel_action)

    # Gamepad controls
    if (not input_locked) and gamepad_navigation_enabled:
        if interaction_menu_active:
            key "pad_dpup_press" action Function(navigate_interaction_menu, "up")
            key "pad_dpdown_press" action Function(navigate_interaction_menu, "down")
            key "pad_lefty_neg" action Function(navigate_interaction_menu, "up")
            key "pad_lefty_pos" action Function(navigate_interaction_menu, "down")
        else:
            key "pad_dpleft_press" action Function(gamepad_navigate, "left")
            key "pad_dpright_press" action Function(gamepad_navigate, "right")
            key "pad_dpup_press" action Function(gamepad_navigate, "up")
            key "pad_dpdown_press" action Function(gamepad_navigate, "down")
            key "pad_leftx_neg" action Function(gamepad_navigate, "left")
            key "pad_leftx_pos" action Function(gamepad_navigate, "right")
            key "pad_lefty_neg" action Function(gamepad_navigate, "up")
            key "pad_lefty_pos" action Function(gamepad_navigate, "down")

        key "pad_a_press" action Function(gamepad_confirm_action)
        if interaction_menu_active:
            key "pad_b_press" action Function(gamepad_cancel_action)
        else:
            key "pad_b_press" action Function(gamepad_select_first_object)
        key "pad_back_press" action Function(toggle_gamepad_navigation)

    # Global shortcuts
    if not input_locked:
        key "c" action Function(toggle_crt_effect)
        key "f" action Function(fade_out_room_audio)
        key "l" action Function(toggle_letterbox)
        key "r" action Function(renpy.restart_interaction)
        key "i" action ToggleVariable("show_info_overlay")
        # Toggle CRT scanline animation
        key "a" action Function(toggle_crt_animation)

    # Scanline size testing
    if not input_locked:
        key "1" action Function(set_crt_parameters, scanline_size=0.5)
        key "2" action Function(set_crt_parameters, scanline_size=1.0)
        key "3" action Function(set_crt_parameters, scanline_size=1.5)
        key "4" action Function(set_crt_parameters, scanline_size=3.0)

    # Vignette live tuning
    if not input_locked:
        # Strength: [ decreases, ] increases
        key "[" action Function(adjust_vignette, delta_strength=-0.05)
        key "]" action Function(adjust_vignette, delta_strength=0.05)
        # Width: - narrows (stronger edges), = widens (softer edges)
        key "-" action Function(adjust_vignette, delta_width=-0.02)
        key "=" action Function(adjust_vignette, delta_width=0.02)
        # Reset to defaults quickly
        key "0" action Function(adjust_vignette, set_strength=0.35, set_width=0.25)
