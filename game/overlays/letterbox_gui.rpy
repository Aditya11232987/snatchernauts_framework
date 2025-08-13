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
default letterbox_active = True

## Letterbox integration with existing systems
define letterbox_adjust_ui = True  # Automatically adjust UI elements
define letterbox_adjust_descriptions = True  # Adjust floating descriptions

################################################################################
## Letterbox Screen
################################################################################

screen letterbox_overlay():
    ## Ensure this appears on top of other screens but below menus
    zorder 90
    
    if letterbox_active:
        ## Top letterbox bar
        frame:
            style "letterbox_bar"
            xalign 0.0
            yalign 0.0
            xsize config.screen_width
            ysize letterbox_bar_height
            background letterbox_color
            
        ## Bottom letterbox bar  
        frame:
            style "letterbox_bar"
            xalign 0.0
            yalign 1.0
            xsize config.screen_width
            ysize letterbox_bar_height
            background letterbox_color
            

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
    def show_letterbox(duration=None):
        """Show the letterbox effect with optional custom duration"""
        global letterbox_active
        if duration is None:
            duration = letterbox_animation_duration
            
        letterbox_active = True
        
        # Add the letterbox overlay to the screen
        if not renpy.get_screen("letterbox_overlay"):
            renpy.show_screen("letterbox_overlay")
            
        return

    def hide_letterbox(duration=None):
        """Hide the letterbox effect with optional custom duration"""
        global letterbox_active
        if duration is None:
            duration = letterbox_animation_duration
            
        letterbox_active = False
        
        # Hide the letterbox overlay screen
        if renpy.get_screen("letterbox_overlay"):
            renpy.hide_screen("letterbox_overlay")
            
        return

    def toggle_letterbox():
        """Toggle letterbox on/off"""
        if letterbox_active:
            hide_letterbox()
        else:
            show_letterbox()

    def set_letterbox_height(height):
        """Set custom letterbox bar height"""
        global letterbox_bar_height
        letterbox_bar_height = height
        
        # Refresh the screen if letterbox is active
        if letterbox_active and renpy.get_screen("letterbox_overlay"):
            renpy.restart_interaction()

## Initialize letterbox overlay screen
init python:
    config.overlay_screens.append("letterbox_overlay")
    
    # Add developer controls if in developer mode
    if config.developer:
        config.overlay_screens.append("letterbox_controls")

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
