# Module Index

This index lists all Ren'Py `.rpy` modules in the project and their purpose. Each file also contains an inline header with Overview/Contracts/Integration to help you navigate quickly.

API
- game/api/display_api.rpy: Backgrounds and object visibility helpers.
- game/api/ui_api.rpy: Hotspots, hover/unhover, and UI button customization.
- game/api/interactions_api.rpy: Interaction menu routines and action execution.
- game/api/room_api.rpy: Room/object manipulation and CRT/navigation helpers.

Core
- game/core/common_utils.rpy: Shared helpers (fonts, dev mode, mouse).
- game/core/common_logging.rpy: Color-coded, truncating logs; function wrappers; print interception.
- game/core/bloom_utils.rpy: Bloom parameters, dimensions, presets.
- game/core/bloom_colors.rpy: Color extraction for bloom.
- game/core/config_builders.rpy: Build configs for rooms/objects.
- game/core/object_factory.rpy: Instantiate objects from configs.
- game/core/room_utils.rpy: Image size registry and scaling helpers.
- game/core/font_config.rpy: Font settings.
- game/core/options.rpy: Project options and defaults (log toggles).
- game/core/rooms/room_config.rpy: Room definitions.
- game/core/rooms/room_editor.rpy: Editor tooling for rooms.
- game/legacy/room_functions.rpy: Legacy room functions (use api/room_api.rpy).
- game/legacy/room_main.rpy: Legacy entry label (use script.rpy:play_room).

Logic
- game/logic/game_logic.rpy: Global hooks and room handler registry.
- game/logic/rooms/room1_logic.rpy: Example room handler.

UI
- game/ui/screens_room.rpy: Room composition (backgrounds, objects, bloom, CRT).
- game/ui/screens_interactions.rpy: Interaction menu and input.
- game/ui/screens_bloom.rpy: Bloom overlay screens.
- game/ui/room_ui.rpy: Overlay buttons and object hotspots.
- game/ui/room_transforms.rpy: Reusable transforms for motion and bloom.
- game/ui/room_descriptions.rpy: Floating and bottom description boxes.
- game/ui/gui.rpy: GUI styles and assets.
- game/ui/screens.rpy: Base Ren'Py screens (save/load, preferences, etc.).

Overlays & Shaders
- game/overlays/letterbox_gui.rpy: Cinematic bars overlay.
- game/overlays/info_overlay.rpy: Info/help overlay.
- game/overlays/debug_overlay.rpy: Draggable debug panel (Cmd+Shift+F12 / Ctrl+Shift+F12).
- game/overlays/fade_overlay.rpy: Modal fade to block input at scene entry.
- game/shaders/crt_shader.rpy: CRT shader and transforms.
- game/shaders/bloom_shader.rpy: Optional bloom shader parts and model.

Entry Points
- game/script.rpy: `label start`, `label play_room`, and `label go`.

Conventions
- Use public APIs (game/api/*) inside logic.
- Avoid UI internals in logic; emit events to hooks.
- Keep module headers up to date when modifying files.
