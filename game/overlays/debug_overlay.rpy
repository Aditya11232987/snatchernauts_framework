# Room Debug Display System
# Debug information and development utilities (verbose + compact modes)

# Common utilities are loaded elsewhere in the project.

init python:
    def get_debug_mouse_text():
        """Get formatted mouse position text"""
        x, y = get_mouse_position()
        return "Mouse: ({}, {})".format(x, y)
    
    def get_debug_room_info():
        """Get current room debug information"""
        room_id = getattr(store, 'current_room_id', None)
        bg = getattr(store, 'room_background', None)
        total = len(getattr(store, 'room_objects', {}) or {})
        visible = 0
        hidden = 0
        for _, od in (getattr(store, 'room_objects', {}) or {}).items():
            if should_display_object(od) and not is_object_hidden(od):
                visible += 1
            else:
                hidden += 1

        info = [
            "Room: {}".format(room_id),
            "Background: {}".format(bg),
            "Objects: total={} visible={} hidden={}".format(total, visible, hidden),
        ]

        # Interaction/state
        info.extend([
            "Hover: {}".format(getattr(store, 'current_hover_object', None)),
            "Interaction menu: {}".format('on' if getattr(store, 'interaction_menu_active', False) else 'off'),
            "Gamepad nav: {}".format('on' if getattr(store, 'gamepad_navigation_enabled', False) else 'off'),
            "Fade complete: {}".format('yes' if getattr(store, 'room_has_faded_in', False) else 'no'),
            "Letterbox: {} (h={})".format('on' if globals().get('letterbox_active', False) else 'off', globals().get('letterbox_bar_height', 0)),
        ])

        # CRT parameters (if present)
        if hasattr(store, 'crt_enabled'):
            info.extend([
                "CRT: {} warp={:.2f} scan={:.2f} chroma={:.2f} size={:.2f} anim={}".format(
                    'on' if store.crt_enabled else 'off',
                    float(getattr(store, 'crt_warp', 0.0)),
                    float(getattr(store, 'crt_scan', 0.0)),
                    float(getattr(store, 'crt_chroma', 0.0)),
                    float(getattr(store, 'crt_scanline_size', 1.0)),
                    'on' if getattr(store, 'crt_animated', False) else 'off'
                ),
                "CRT vignette: strength={:.2f} width={:.2f}".format(
                    float(getattr(store, 'crt_vignette_strength', 0.0)),
                    float(getattr(store, 'crt_vignette_width', 0.0))
                ),
            ])

        # Hovered object details + bloom color
        hov = getattr(store, 'current_hover_object', None)
        objs = getattr(store, 'room_objects', {}) or {}
        if hov and hov in objs:
            o = objs[hov]
            info.extend([
                "Obj [{}]: pos=({},{}) size={}x{} scale={}%%".format(
                    hov, o.get('x'), o.get('y'), o.get('width'), o.get('height'), o.get('scale_percent', 100)
                ),
                "  desc len={} float_intensity={} box_pos={}".format(
                    len(o.get('description', '') or ''), o.get('float_intensity', 1.0), o.get('box_position', 'auto')
                ),
                "  bloom: en={} int={:.2f} rad={:.2f} soft={:.2f} a=({:.2f}-{:.2f}) speed={:.2f}".format(
                    o.get('bloom_enabled', True),
                    float(o.get('bloom_intensity', 0.5)),
                    float(o.get('bloom_radius', 8.0)),
                    float(o.get('bloom_softness', 0.7)),
                    float(o.get('bloom_alpha_min', 0.2)),
                    float(o.get('bloom_alpha_max', 0.6)),
                    float(o.get('bloom_pulse_speed', 1.0))
                ),
            ])
            try:
                fallback_color = o.get("bloom_color", "#ffffff")
                bloom_color = get_bloom_color(o["image"], fallback_color)
                info.append("  bloom color={}".format(bloom_color))
            except Exception:
                pass

        return info

    def get_debug_compact_info():
        """Short one-line summary for compact mode"""
        room_id = getattr(store, 'current_room_id', None)
        hov = getattr(store, 'current_hover_object', None)
        total = len(getattr(store, 'room_objects', {}) or {})
        return [
            "Room={} objs={} hover={} CRT={} Letterbox={} FadeDone={}".format(
                room_id, total, hov,
                'on' if getattr(store, 'crt_enabled', False) else 'off',
                'on' if globals().get('letterbox_active', False) else 'off',
                'yes' if getattr(store, 'room_has_faded_in', False) else 'no'
            )
        ]

# Debug display styles
define DEBUG_TEXT_STYLE = {
    "color": "#ffffff",
    "size": 16
}

default debug_verbose = True

# Screen fragment for debug display (appears above letterbox)
screen debug_overlay():
    # Put debug info on a high z-order to appear above letterbox
    zorder 200

    if is_developer_mode():
        # Toggle verbosity with V
        key "v" action ToggleVariable("debug_verbose")

        $ info_lines = get_debug_room_info() if debug_verbose else get_debug_compact_info()

        frame:
            background "#00000088"
            padding (8, 8)
            xpos 10
            ypos 10
            vbox:
                spacing 4
                text get_debug_mouse_text():
                    color DEBUG_TEXT_STYLE["color"]
                    size DEBUG_TEXT_STYLE["size"]
                    substitute False
                for line in info_lines:
                    text line:
                        color DEBUG_TEXT_STYLE["color"]
                        size DEBUG_TEXT_STYLE["size"]
                        substitute False
