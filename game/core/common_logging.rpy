init 900 python:
    # Global logging utilities
    import builtins as _builtins
    try:
        ORIG_PRINT = _builtins.print
    except Exception:
        ORIG_PRINT = None
    def _enabled():
        try:
            return bool(getattr(renpy.store, 'sn_log_enabled', True))
        except Exception:
            return True

    def _use_color():
        try:
            return bool(getattr(renpy.store, 'sn_log_color', True))
        except Exception:
            return True

    C = {
        'reset': "\033[0m",
        'dim': "\033[2m",
        'gray': "\033[90m",
        'cyan': "\033[36m",
        'magenta': "\033[35m",
        'yellow': "\033[33m",
    }
    def _short_repr(val, limit=120):
        try:
            s = val if isinstance(val, str) else repr(val)
        except Exception:
            s = '<unrepr>'
        if s is None:
            s = 'None'
        if len(s) > limit:
            return s[: max(0, limit - 1) ] + '…'
        return s

    def _truncate_line(s, line_limit=200):
        if len(s) > line_limit:
            return s[: max(0, line_limit - 1) ] + '…'
        return s

    def _out(s):
        try:
            if ORIG_PRINT:
                ORIG_PRINT(s)
        except Exception:
            pass

    def log(msg, line_limit=200):
        if not _enabled():
            return
        try:
            line = _truncate_line(str(msg), line_limit)
            if _use_color():
                _out(f"{C['gray']}::{C['reset']} " + line)
            else:
                _out(":: " + line)
        except Exception:
            pass

    def log_multiline(text, line_limit=200):
        if not _enabled():
            return
        try:
            for line in str(text).splitlines():
                line = _truncate_line(line, line_limit)
                if _use_color():
                    _out(f"{C['gray']}::{C['reset']} " + line)
                else:
                    _out(":: " + line)
        except Exception:
            pass

    def _wrap(name, fn):
        def wrapped(*args, **kwargs):
            if _enabled():
                try:
                    args_s = ', '.join(_short_repr(a, 80) for a in args)
                    kwargs_s = ', '.join(f"{k}={_short_repr(v, 80)}" for k, v in kwargs.items())
                    if kwargs_s:
                        call_sig = f"{args_s} | {kwargs_s}" if args_s else kwargs_s
                    else:
                        call_sig = args_s
                    if _use_color():
                        msg = f"{C['cyan']}ENTER{C['reset']} {C['yellow']}{name}{C['reset']}({C['dim']}{call_sig}{C['reset']})"
                    else:
                        msg = f"ENTER {name}({call_sig})"
                    log(msg)
                except Exception:
                    pass
            rv = fn(*args, **kwargs)
            if _enabled():
                try:
                    rv_s = _short_repr(rv, 120)
                    if _use_color():
                        msg = f"{C['magenta']}EXIT{C['reset']} {C['yellow']}{name}{C['reset']} -> {C['dim']}{rv_s}{C['reset']}"
                    else:
                        msg = f"EXIT {name} -> {rv_s}"
                    log(msg)
                except Exception:
                    pass
            return rv
        return wrapped

    # Intercept built-in print to auto-prefix and truncate.
    def _sn_print(*args, **kwargs):
        try:
            intercept = getattr(renpy.store, 'sn_log_intercept_prints', True)
        except Exception:
            intercept = True
        if not ORIG_PRINT:
            return
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '\n')
        text = sep.join(str(a) for a in args)
        if '\n' in text:
            lines = text.splitlines()
        else:
            lines = [text]
        use_color = _use_color()
        if intercept and _enabled():
            for i, line in enumerate(lines):
                pline = _truncate_line(line, 200)
                if not pline.startswith('::'):
                    if use_color:
                        pline = f"{C['gray']}::{C['reset']} " + pline
                    else:
                        pline = ":: " + pline
                ORIG_PRINT(pline, end=(end if i == len(lines)-1 else '\n'))
        else:
            # Pass through untouched
            ORIG_PRINT(text, end=end)

    try:
        if ORIG_PRINT and getattr(_builtins.print, '_sn_wrapped', False) is False:
            pass
    except Exception:
        pass
    try:
        # Replace built-in print with our wrapper (idempotent)
        if not getattr(_builtins.print, '_sn_wrapped', False):
            _builtins.print = _sn_print
            _builtins.print._sn_wrapped = True  # type: ignore
    except Exception:
        pass

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
