# Info Overlay System
# Shows framework information, controls, and debug keys

# Initialize continue button variable
default show_continue_button = False

# Info overlay content (shared between both screens)
screen info_overlay_content():
    vbox:
        spacing 20
        xalign 0.5
        yalign 0.5
        
        # Title
        text "Snatchernauts Framework [config.version]":
            xalign 0.5
            size 28
            color "#00ffff"
        
        text "Interactive Point-and-Click System":
            xalign 0.5
            size 18
            color "#ffffff"
        
        null height 20
        
        # Controls section
        vbox:
            spacing 8
            
            text "CONTROLS:":
                size 20
                color "#ffff00"
            
            text "• A/Enter/Space: Interact with selected object":
                size 16
                color "#ffffff"
            
            text "• Arrow Keys/WASD/D-pad: Navigate between objects":
                size 16
                color "#ffffff"
            
            text "• B/Escape: Cancel/Go back":
                size 16
                color "#ffffff"
            
            text "• Mouse: Hover and click objects directly":
                size 16
                color "#ffffff"
        
        null height 15
        
        # Debug keys section
        vbox:
            spacing 8
            
            text "DEBUG KEYS:":
                size 20
                color "#ff6666"
            
            text "• I: Toggle this info overlay":
                size 16
                color "#ffffff"
            
            text "• C: Toggle CRT effect":
                size 16
                color "#ffffff"
            
            text "• L: Toggle letterbox effect":
                size 16
                color "#ffffff"
            
            text "• F: Fade out room audio":
                size 16
                color "#ffffff"
            
            text "• R: Refresh/restart interaction":
                size 16
                color "#ffffff"
            
            text "• 1-4: Adjust CRT scanline size":
                size 16
                color "#ffffff"
            
            text "• Back/Select (Gamepad): Toggle gamepad navigation":
                size 16
                color "#ffffff"
        
        null height 20
        
        # Continue button (only shown in start screen)
        if show_continue_button:
            textbutton "Okay - Continue to Room1":
                xalign 0.5
                action Return()
                text_size 20
                text_color "#00ffff"
                text_hover_color "#ffffff"
                background "#333333dd"
                hover_background "#555555dd"
                padding (20, 10)
        else:
            # Footer for in-game overlay
            text "Press I to hide this overlay":
                xalign 0.5
                size 16
                color "#aaaaaa"
                italic True

# Start screen version with continue button
screen info_overlay_start():
    # Full screen overlay
    zorder 200
    
    # Semi-transparent background
    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        ysize 650
        background "#000000cc"
        padding (30, 30)
        
        use info_overlay_content

# In-game overlay version (toggleable with I key)
screen info_overlay():
    # Put info overlay on a high z-order to appear above letterbox
    zorder 180
    
    if show_info_overlay and not show_continue_button:
        # Semi-transparent background
        frame:
            xalign 0.5
            yalign 0.5
            xsize 800
            ysize 600
            background "#000000cc"
            padding (30, 30)
            
            use info_overlay_content
