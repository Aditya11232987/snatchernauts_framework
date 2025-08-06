# Room Description Box System
# Floating and fixed description boxes with dynamic sizing

# Include common utilities
include "common_utils.rpy"

# Description box configuration
define DESCRIPTION_BOX_CONFIG = {
    "min_width": 200,
    "max_width": 350,
    "min_height": 60,
    "max_height": 120,
    "padding": {"horizontal": 15, "vertical": 10},
    "text_margin": 30,
    "background": "curved_box_small.png",
    "border_size": 20
}

define DESCRIPTION_TEXT_CONFIG = {
    "color": "#ffffff",
    "size": 16,
    "align": 0.5,
    "font": "fonts/quaver.ttf"
}

define BOTTOM_DESCRIPTION_CONFIG = {
    "xpos": 0,
    "ypos": 620,
    "width": 1280,
    "height": 100,
    "background": "#000000cc",
    "padding": {"horizontal": 30, "vertical": 20},
    "title_color": "#ffff00",
    "title_size": 24,
    "text_color": "#ffffff",
    "text_size": 16,
    "default_color": "#cccccc",
    "default_size": 16
}

init python:
    def calculate_description_box_size(description):
        """Calculate dynamic box dimensions based on description length"""
        text_length = len(description)
        
        box_width = min(
            DESCRIPTION_BOX_CONFIG["max_width"],
            max(DESCRIPTION_BOX_CONFIG["min_width"], text_length * 3 + 100)
        )
        
        # Add extra height for better line spacing with pixel font
        line_height = 26  # 16px font + 10px extra spacing
        estimated_lines = (text_length // 40 + 2)
        calculated_height = estimated_lines * line_height
        
        box_height = min(
            DESCRIPTION_BOX_CONFIG["max_height"] + 20,  # Allow slightly taller boxes
            max(DESCRIPTION_BOX_CONFIG["min_height"], calculated_height)
        )
        
        return box_width, box_height

# Screen fragment for floating description box - using property functions to eliminate duplication
screen floating_description_box(obj, box_width, box_height, box_x, box_y, float_intensity):
    # Put description boxes on high z-order to appear above letterbox
    zorder 150
    
    $ frame_props = get_description_frame_properties(box_x, box_y, box_width, box_height)
    $ text_props = get_description_text_properties(box_width)
    
    if float_intensity > 0.0:
        frame at floating_bubble(float_intensity):
            xpos frame_props["xpos"]
            ypos frame_props["ypos"]
            xsize frame_props["xsize"]
            ysize frame_props["ysize"]
            background frame_props["background"]
            padding frame_props["padding"]
            
            text obj["description"]:
                xalign text_props["xalign"]
                yalign text_props["yalign"]
                color text_props["color"]
                size text_props["size"]
                text_align text_props["text_align"]
                xmaximum text_props["xmaximum"]
                font text_props["font"]
                line_spacing 2
    else:
        frame at no_float:
            xpos frame_props["xpos"]
            ypos frame_props["ypos"]
            xsize frame_props["xsize"]
            ysize frame_props["ysize"]
            background frame_props["background"]
            padding frame_props["padding"]
            
            text obj["description"]:
                xalign text_props["xalign"]
                yalign text_props["yalign"]
                color text_props["color"]
                size text_props["size"]
                text_align text_props["text_align"]
                xmaximum text_props["xmaximum"]
                font text_props["font"]
                line_spacing 2

# Python function to create shared frame properties
init python:
    def get_description_frame_properties(box_x, box_y, box_width, box_height):
        """Get common frame properties for description boxes"""
        return {
            "xpos": box_x,
            "ypos": box_y,
            "xsize": box_width,
            "ysize": box_height,
            "background": Frame(
                DESCRIPTION_BOX_CONFIG["background"], 
                DESCRIPTION_BOX_CONFIG["border_size"], 
                DESCRIPTION_BOX_CONFIG["border_size"], 
                tile=False
            ),
            "padding": (
                DESCRIPTION_BOX_CONFIG["padding"]["horizontal"], 
                DESCRIPTION_BOX_CONFIG["padding"]["vertical"]
            )
        }
    
    def get_description_text_properties(box_width):
        """Get common text properties for description text"""
        return {
            "xalign": DESCRIPTION_TEXT_CONFIG["align"],
            "yalign": DESCRIPTION_TEXT_CONFIG["align"],
            "color": DESCRIPTION_TEXT_CONFIG["color"],
            "size": DESCRIPTION_TEXT_CONFIG["size"],
            "text_align": DESCRIPTION_TEXT_CONFIG["align"],
            "xmaximum": box_width - DESCRIPTION_BOX_CONFIG["text_margin"],
            "font": get_font()
        }

# Screen fragment for bottom description area
screen bottom_description_area():
    frame:
        xpos BOTTOM_DESCRIPTION_CONFIG["xpos"]
        ypos BOTTOM_DESCRIPTION_CONFIG["ypos"]
        xsize BOTTOM_DESCRIPTION_CONFIG["width"]
        ysize BOTTOM_DESCRIPTION_CONFIG["height"]
        background BOTTOM_DESCRIPTION_CONFIG["background"]
        padding (
            BOTTOM_DESCRIPTION_CONFIG["padding"]["horizontal"], 
            BOTTOM_DESCRIPTION_CONFIG["padding"]["vertical"]
        )
        
        if current_hover_object:
            vbox:
                text "Examining: [format_object_name(current_hover_object)]":
                    color BOTTOM_DESCRIPTION_CONFIG["title_color"]
                    size BOTTOM_DESCRIPTION_CONFIG["title_size"]
                    font get_font()
                text room_objects[current_hover_object]["description"]:
                    color BOTTOM_DESCRIPTION_CONFIG["text_color"]
                    size BOTTOM_DESCRIPTION_CONFIG["text_size"]
                    font get_font()
        else:
            text "Hover over objects in the room to examine them.":
                color BOTTOM_DESCRIPTION_CONFIG["default_color"]
                size BOTTOM_DESCRIPTION_CONFIG["default_size"]
                font get_font()
