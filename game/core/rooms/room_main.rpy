# Room Exploration System - Main File
# Point-and-click interface with hover effects and floating descriptions
#
# INSTRUCTIONS: To modify objects, edit room_config.rpy

# Include the separated files
include "core/rooms/room_config.rpy"
include "ui/room_transforms.rpy"

# Core API
include "api/room_api.rpy"
include "api/display_api.rpy"
include "api/ui_api.rpy"
include "api/interactions_api.rpy"

include "core/rooms/room_editor.rpy"

# Shaders
include "shaders/bloom_shader.rpy"
include "shaders/crt_shader.rpy"

include "overlays/debug_overlay.rpy"
include "ui/room_descriptions.rpy"
include "ui/room_ui.rpy"
include "ui/screens_room.rpy"
include "ui/screens_bloom.rpy"
include "overlays/letterbox_gui.rpy"
include "ui/screens_interactions.rpy"
include "overlays/info_overlay.rpy"

## Main exploration screen moved to ui/screens_room.rpy for easier editing

## Defaults moved to game/script.rpy for central configuration
    
    
# Label to start room exploration
label explore_room:
    # Backward-compatible entry; prefer calling play_room from script.rpy
    call play_room("room1", "audio/room1.mp3")
    return
