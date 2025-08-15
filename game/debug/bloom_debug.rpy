# Bloom Debug System
# Centralized debug output for bloom effects and object interactions

init python:
    # Global debug flags
    bloom_debug_enabled = True  # Set to True to enable debug output
    bloom_debug_verbose = True  # Set to True for detailed positioning info
    bloom_debug_hover = False    # Gate hover spam separately
    
    def debug_bloom(message, category="BLOOM"):
        """Print bloom debug messages with consistent formatting"""
        if bloom_debug_enabled:
            print(f"[{category} DEBUG] {message}")
    
    def debug_bloom_positioning(obj_name, original_pos, bloom_pos, obj_size, bloom_size):
        """Debug object vs bloom positioning"""
        if not (bloom_debug_enabled and bloom_debug_verbose):
            return
            
        debug_bloom(f"=== POSITIONING DEBUG for {obj_name} ===")
        debug_bloom(f"  Original Object:")
        debug_bloom(f"    Position: ({original_pos[0]}, {original_pos[1]})")
        debug_bloom(f"    Size: {obj_size[0]}x{obj_size[1]}")
        debug_bloom(f"    Bounds: {original_pos[0]}-{original_pos[0] + obj_size[0]}, {original_pos[1]}-{original_pos[1] + obj_size[1]}")
        debug_bloom(f"  Bloom Effect:")
        debug_bloom(f"    Position: ({bloom_pos[0]}, {bloom_pos[1]})")
        debug_bloom(f"    Size: {bloom_size[0]}x{bloom_size[1]}")
        debug_bloom(f"    Bounds: {bloom_pos[0]}-{bloom_pos[0] + bloom_size[0]}, {bloom_pos[1]}-{bloom_pos[1] + bloom_size[1]}")
        debug_bloom(f"  Offset Analysis:")
        debug_bloom(f"    X offset: {bloom_pos[0] - original_pos[0]} pixels")
        debug_bloom(f"    Y offset: {bloom_pos[1] - original_pos[1]} pixels")
        debug_bloom(f"    Size difference: {bloom_size[0] - obj_size[0]}x{bloom_size[1] - obj_size[1]}")
        debug_bloom(f"=== END POSITIONING DEBUG ===")
    
    def debug_bloom_properties(obj_name, bloom_data, transform_name):
        """Debug bloom properties and parameters"""
        if not bloom_debug_enabled:
            return
            
        debug_bloom(f"=== BLOOM PROPERTIES for {obj_name} ===")
        debug_bloom(f"  Transform: {transform_name}")
        if bloom_data:
            debug_bloom(f"  Image: {bloom_data.get('image', 'None')}")
            debug_bloom(f"  Color: {bloom_data.get('color', 'None')}")
            params = bloom_data.get('parameters', {})
            debug_bloom(f"  Alpha Range: {params.get('bloom_alpha_min', 'N/A')} - {params.get('bloom_alpha_max', 'N/A')}")
            debug_bloom(f"  Intensity: {params.get('bloom_intensity', 'N/A')}")
            debug_bloom(f"  Pulse Speed: {params.get('desaturation_pulse_speed', params.get('bloom_pulse_speed', 'N/A'))}")
            dims = bloom_data.get('dimensions', {})
            debug_bloom(f"  Dimensions: {dims.get('x', 'N/A')}, {dims.get('y', 'N/A')}, {dims.get('width', 'N/A')}x{dims.get('height', 'N/A')}")
        else:
            debug_bloom(f"  Bloom Data: None (bloom disabled for this object)")
        debug_bloom(f"=== END BLOOM PROPERTIES ===")
    
    def debug_gamepad_navigation(current_object, selected_object, hover_object):
        """Debug gamepad navigation state"""
        if not bloom_debug_enabled:
            return
            
        debug_bloom("=== GAMEPAD NAVIGATION STATE ===", "NAV")
        debug_bloom(f"  Current Object: {current_object}", "NAV")
        debug_bloom(f"  Selected Object: {selected_object}", "NAV")
        debug_bloom(f"  Hover Object: {hover_object}", "NAV")
        debug_bloom(f"  Navigation Enabled: {getattr(store, 'gamepad_navigation_enabled', 'Unknown')}", "NAV")
        debug_bloom("=== END NAVIGATION STATE ===", "NAV")
    
    def debug_object_properties(obj_name, obj_data, props):
        """Debug object display properties"""
        if not (bloom_debug_enabled and bloom_debug_verbose):
            return
            
        debug_bloom(f"=== OBJECT PROPERTIES for {obj_name} ===", "OBJ")
        debug_bloom(f"  Raw Object Data:", "OBJ")
        for key, value in obj_data.items():
            debug_bloom(f"    {key}: {value}", "OBJ")
        debug_bloom(f"  Display Properties:", "OBJ")
        for key, value in props.items():
            debug_bloom(f"    {key}: {value}", "OBJ")
        debug_bloom(f"=== END OBJECT PROPERTIES ===", "OBJ")
    
    def debug_bloom_transform_call(transform_name, alpha_max, alpha_min, pulse_speed, color, blur_amount, offset=None):
        """Debug transform parameters"""
        if not bloom_debug_enabled:
            return
            
        debug_bloom(f"=== TRANSFORM CALL: {transform_name} ===", "TRANSFORM")
        debug_bloom(f"  Alpha: {alpha_min} - {alpha_max}", "TRANSFORM")
        debug_bloom(f"  Pulse Speed: {pulse_speed}", "TRANSFORM")
        debug_bloom(f"  Color: {color}", "TRANSFORM")
        debug_bloom(f"  Blur: {blur_amount}px", "TRANSFORM")
        if offset is not None:
            debug_bloom(f"  Offset: {offset}px", "TRANSFORM")
        debug_bloom(f"=== END TRANSFORM CALL ===", "TRANSFORM")

# Global debug toggle functions for easy control
init python:
    def toggle_bloom_debug():
        """Toggle bloom debug output"""
        global bloom_debug_enabled
        bloom_debug_enabled = not bloom_debug_enabled
        debug_bloom(f"Bloom debug {'ENABLED' if bloom_debug_enabled else 'DISABLED'}")
    
    def toggle_bloom_verbose():
        """Toggle verbose bloom debug output"""
        global bloom_debug_verbose
        bloom_debug_verbose = not bloom_debug_verbose
        debug_bloom(f"Verbose debug {'ENABLED' if bloom_debug_verbose else 'DISABLED'}")
    
    def toggle_bloom_hover():
        """Toggle hover-specific debug spam"""
        global bloom_debug_hover
        bloom_debug_hover = not bloom_debug_hover
        debug_bloom(f"Hover debug {'ENABLED' if bloom_debug_hover else 'DISABLED'}")
    
    def set_bloom_debug(enabled=True, verbose=True):
        """Set bloom debug state"""
        global bloom_debug_enabled, bloom_debug_verbose
        bloom_debug_enabled = enabled
        bloom_debug_verbose = verbose
        debug_bloom(f"Debug set to: enabled={enabled}, verbose={verbose}")
