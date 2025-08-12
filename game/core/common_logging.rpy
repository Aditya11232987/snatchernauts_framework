init 900 python:
    # Global logging utilities
    def log(msg):
        try:
            print(":: " + str(msg))
        except Exception:
            pass

    def _wrap(name, fn):
        def wrapped(*args, **kwargs):
            try:
                print(":: ENTER {} args={} kwargs={}".format(name, args, kwargs))
            except Exception:
                pass
            rv = fn(*args, **kwargs)
            try:
                print(":: EXIT {} -> {}".format(name, rv))
            except Exception:
                pass
            return rv
        return wrapped

    def _try_wrap(attr_name):
        import renpy.store as store
        if hasattr(store, attr_name):
            fn = getattr(store, attr_name)
            if callable(fn) and not getattr(fn, '_is_wrapped', False):
                wrapped = _wrap(attr_name, fn)
                wrapped._is_wrapped = True
                setattr(store, attr_name, wrapped)

    # Wrap a curated set of public API helpers for trace output.
    for name in [
        # display_api
        'get_room_background','get_fallback_background','should_display_object','get_object_display_properties',
        'set_fallback_background_color','set_default_background','hide_object','show_object','is_object_hidden',
        # ui_api
        'create_object_hotspot','get_all_object_hotspots','get_room_exit_action','get_editor_mode_action',
        'handle_object_hover','handle_object_unhover','customize_exit_button','customize_editor_button','add_custom_button',
        # room_api
        'move_object','scale_object','calculate_box_position','get_room_list','get_room_objects','add_room_object',
        'remove_room_object','create_new_room','delete_room','duplicate_room','save_room_changes','reset_room_changes',
        'clear_persistent_overrides','play_room_audio','fade_out_room_audio','toggle_crt_effect','set_crt_parameters',
        'toggle_crt_animation','export_room_config','get_object_list_for_navigation','gamepad_navigate',
        'gamepad_select_first_object','toggle_gamepad_navigation','adjust_vignette'
    ]:
        _try_wrap(name)

