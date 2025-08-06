# Room and Image Utilities
# General utilities for room management and image processing

# Original image dimensions for percentage calculations
define ORIGINAL_SIZES = {
    "detective": {"width": 325, "height": 495},
    "patreon": {"width": 364, "height": 450}
}

init python:
    def calc_size(image_name, scale_percent):
        """Calculate width and height from percentage of original size"""
        if image_name in ORIGINAL_SIZES:
            orig = ORIGINAL_SIZES[image_name]
            width = int(orig["width"] * scale_percent / 100)
            height = int(orig["height"] * scale_percent / 100)
            return width, height
        return 100, 100  # fallback
    
    def add_original_size(image_name, width, height):
        """Add a new image to the original sizes dictionary"""
        ORIGINAL_SIZES[image_name] = {"width": width, "height": height}
    
    def get_original_size(image_name):
        """Get the original dimensions of an image"""
        return ORIGINAL_SIZES.get(image_name, {"width": 100, "height": 100})
    
    def calculate_scale_from_dimensions(image_name, target_width, target_height):
        """Calculate what scale percentage would give the target dimensions"""
        if image_name in ORIGINAL_SIZES:
            orig = ORIGINAL_SIZES[image_name]
            scale_x = (target_width / orig["width"]) * 100
            scale_y = (target_height / orig["height"]) * 100
            # Return the average scale or the smaller one to maintain aspect ratio
            return min(scale_x, scale_y)
        return 100.0
