################################################################################
## Letterbox GUI System
################################################################################
##
## This file contains the letterbox functionality to create cinematic
## widescreen effects similar to classic film noir movies.
##
## Overview
## - Draws top/bottom bars for a cinematic look.
## - Exposes show/hide/toggle functions and integrates with overlay screens.
##

init offset = -1

## Letterbox Configuration Variables
################################################################################

## Height of the letterbox bars (top and bottom)
define letterbox_bar_height = 100

## Color of the letterbox bars
define letterbox_color = "#000000"

## Animation duration for letterbox show/hide
define letterbox_animation_duration = 1.0

## Whether letterbox is currently active
default letterbox_active = False

## Letterbox integration with existing systems
define letterbox_adjust_ui = True  # Automatically adjust UI elements
define letterbox_adjust_descriptions = True  # Adjust floating descriptions

################################################################################
## Letterbox Screen
################################################################################

## Letterbox animation state tracking
default letterbox_hiding = False

# DISABLED: Old letterbox overlay replaced by shader-based letterbox
# screen letterbox_overlay():
#     pass
            

## Letterbox control screen (for testing/debugging)
screen letterbox_controls():
    zorder 200
    
    if config.developer:
        vbox:
            xalign 0.02
            yalign 0.02
            spacing 10
            
            # No letterbox toggle button - letterbox is permanent

################################################################################
## Letterbox Styles
################################################################################

style letterbox_bar:
    padding (0, 0, 0, 0)

################################################################################
## Letterbox Functions
################################################################################

init python:
    # Redirect legacy GUI functions to shader-backed implementations
    def show_letterbox(duration=None, wait_for_animation=True):
        try:
            return renpy.store.show_letterbox_shader(duration=duration, wait_for_animation=wait_for_animation)
        except Exception:
            return None

    def hide_letterbox(duration=None, wait_for_animation=True):
        try:
            return renpy.store.hide_letterbox_shader(duration=duration, wait_for_animation=wait_for_animation)
        except Exception:
            return None

    def toggle_letterbox():
        try:
            return renpy.store.toggle_letterbox_shader()
        except Exception:
            return None

    def set_letterbox_height(height):
        try:
            return renpy.store.set_letterbox_shader_params(height=height)
        except Exception:
            return None

## Initialize letterbox overlay screen
init python:
    # COMPLETELY DISABLED: GUI-based letterbox overlay is replaced by shader-based letterbox
    # The old screen is no longer registered to prevent UI conflicts
    pass

################################################################################
## Letterbox Transforms and Animations
################################################################################

## Transform for smooth letterbox appearance
transform letterbox_appear:
    on show:
        ysize 0
        linear letterbox_animation_duration ysize letterbox_bar_height
    on hide:
        linear letterbox_animation_duration ysize 0

## Top letterbox bar slide down animation
transform letterbox_top_bar:
    yoffset -letterbox_bar_height
    
    on show:
        ease letterbox_animation_duration yoffset 0
    
    on hide:
        ease letterbox_animation_duration yoffset -letterbox_bar_height

## Bottom letterbox bar slide up animation
transform letterbox_bottom_bar:
    yoffset letterbox_bar_height
    
    on show:
        ease letterbox_animation_duration yoffset 0
    
    on hide:
        ease letterbox_animation_duration yoffset letterbox_bar_height


################################################################################
## Enhanced Say Screen with Letterbox Support
################################################################################

## Enhanced say screen that works well with letterbox
screen letterbox_say(who, what):
    ## Ensure dialogue appears in the letterbox-safe area
    
    window:
        id "window"
        
        ## Adjust positioning for letterbox
        if letterbox_active:
            ypos letterbox_bar_height + 20
            ymaximum config.screen_height - (letterbox_bar_height * 2) - 40
        
        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

    ## Side images adjusted for letterbox
    if not renpy.variant("small") and letterbox_active:
        add SideImage() xalign 0.0 yalign 1.0 yoffset -letterbox_bar_height
    elif not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

################################################################################
## Letterbox-compatible Choice Screen
################################################################################

screen letterbox_choice(items):
    style_prefix "choice"

    vbox:
        ## Adjust choice positioning for letterbox
        if letterbox_active:
            ypos 270 + (letterbox_bar_height // 2)
        else:
            ypos 270
        yanchor 0.5
        
        for i in items:
            textbutton i.caption action i.action

################################################################################
## Utility Functions
################################################################################

init python:
    def letterbox_scene(scene_name, **kwargs):
        """Show a scene with letterbox effect"""
        show_letterbox()
        renpy.scene(scene_name, **kwargs)
