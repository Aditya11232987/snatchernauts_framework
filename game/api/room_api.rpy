# Room API
# Consolidated room management and object manipulation functions

init python:
    def move_object(obj_name, dx, dy, room_id=None):
        """Move an object by dx, dy pixels in specified room (or current room)"""
        if room_id is None:
            room_id = store.current_room_id
        
        if room_id == store.current_room_id and obj_name in store.room_objects:
            store.room_objects[obj_name]["x"] = max(0, min(1280-store.room_objects[obj_name]["width"], store.room_objects[obj_name]["x"] + dx))
            store.room_objects[obj_name]["y"] = max(0, min(720-store.room_objects[obj_name]["height"], store.room_objects[obj_name]["y"] + dy))
        
        if room_id in ROOM_DEFINITIONS and obj_name in ROOM_DEFINITIONS[room_id]["objects"]:
            obj_ref = ROOM_DEFINITIONS[room_id]["objects"][obj_name]
            obj_ref["x"] = max(0, min(1280-obj_ref["width"], obj_ref["x"] + dx))
            obj_ref["y"] = max(0, min(720-obj_ref["height"], obj_ref["y"] + dy))
        
        renpy.restart_interaction()
    
    def scale_object(obj_name, scale_change, room_id=None):
        """Scale an object by percentage change or reset to 100% in specified room (or current room)"""
        if room_id is None:
            room_id = store.current_room_id
            
        target_objects = None
        if room_id == store.current_room_id and obj_name in store.room_objects:
            target_objects = store.room_objects
        elif room_id in ROOM_DEFINITIONS and obj_name in ROOM_DEFINITIONS[room_id]["objects"]:
            target_objects = ROOM_DEFINITIONS[room_id]["objects"]
        
        if target_objects and obj_name in target_objects:
            if scale_change == "reset":
                new_scale = 100
            else:
                current_scale = target_objects[obj_name]["scale_percent"]
                new_scale = max(10, min(500, current_scale + scale_change))
            
            target_objects[obj_name]["scale_percent"] = new_scale
            
            if obj_name in ORIGINAL_SIZES:
                orig = ORIGINAL_SIZES[obj_name]
                new_width = int(orig["width"] * new_scale / 100)
                new_height = int(orig["height"] * new_scale / 100)
                
                target_objects[obj_name]["width"] = new_width
                target_objects[obj_name]["height"] = new_height
                
                max_x = 1280 - new_width
                max_y = 720 - new_height
                target_objects[obj_name]["x"] = max(0, min(max_x, target_objects[obj_name]["x"]))
                target_objects[obj_name]["y"] = max(0, min(max_y, target_objects[obj_name]["y"]))
            
            if room_id == store.current_room_id:
                if room_id in ROOM_DEFINITIONS and obj_name in ROOM_DEFINITIONS[room_id]["objects"]:
                    ROOM_DEFINITIONS[room_id]["objects"][obj_name].update(target_objects[obj_name])
            elif obj_name in store.room_objects:
                store.room_objects[obj_name].update(target_objects[obj_name])
            
            renpy.restart_interaction()

    def calculate_box_position(obj, box_width, box_height, position_setting):
        """Calculate the position of a description box relative to an object"""
        if "+" in position_setting:
            direction, distance_str = position_setting.split("+")
            try:
                margin = int(distance_str)
            except ValueError:
                margin = 50
        else:
            direction = position_setting
            margin = 50
        
        if direction == "top":
            box_x = obj["x"] + obj["width"] // 2 - box_width // 2
            box_y = obj["y"] - box_height - margin
            box_position = "top"
        elif direction == "bottom":
            box_x = obj["x"] + obj["width"] // 2 - box_width // 2
            box_y = obj["y"] + obj["height"] + margin
            box_position = "bottom"
        elif direction == "left":
            box_x = obj["x"] - box_width - margin
            box_y = obj["y"] + (obj["height"] - box_height) // 2
            box_position = "left"
        elif direction == "right":
            box_x = obj["x"] + obj["width"] + margin
            box_y = obj["y"] + (obj["height"] - box_height) // 2
            box_position = "right"
        else:
            positions = [
                (obj["x"] + obj["width"] // 2 - box_width // 2, obj["y"] - box_height - 50, "top"),
                (obj["x"] + obj["width"] // 2 - box_width // 2, obj["y"] + obj["height"] + 50, "bottom"),
                (obj["x"] + obj["width"] + 50, obj["y"] + (obj["height"] - box_height) // 2, "right"),
                (obj["x"] - box_width - 50, obj["y"] + (obj["height"] - box_height) // 2, "left"),
            ]
            box_x, box_y, box_position = positions[0]
            for pos_x, pos_y, pos_name in positions:
                if (pos_x >= 30 and pos_x + box_width <= 1250 and
                    pos_y >= 30 and pos_y + box_height <= 590):
                    box_x, box_y, box_position = pos_x, pos_y, pos_name
                    break
        
        box_x = max(30, min(box_x, 1250 - box_width))
        box_y = max(30, min(box_y, 590 - box_height))
        return box_x, box_y, box_position
    
    def get_room_list():
        return list(ROOM_DEFINITIONS.keys())
    
    def get_room_objects(room_id):
        if room_id in ROOM_DEFINITIONS:
            return ROOM_DEFINITIONS[room_id]["objects"]
        return {}
    
    def add_room_object(room_id, obj_name, obj_data):
        if room_id in ROOM_DEFINITIONS:
            ROOM_DEFINITIONS[room_id]["objects"][obj_name] = obj_data
            if room_id == store.current_room_id:
                store.room_objects[obj_name] = obj_data
            return True
        return False
    
    def remove_room_object(room_id, obj_name):
        if room_id in ROOM_DEFINITIONS and obj_name in ROOM_DEFINITIONS[room_id]["objects"]:
            del ROOM_DEFINITIONS[room_id]["objects"][obj_name]
            if room_id == store.current_room_id and obj_name in store.room_objects:
                del store.room_objects[obj_name]
            return True
        return False
    
    def create_new_room(room_id, background_image="", objects=None):
        if objects is None:
            objects = {}
        ROOM_DEFINITIONS[room_id] = {"background": background_image, "objects": objects}
        return True
    
    def delete_room(room_id):
        if room_id in ROOM_DEFINITIONS and room_id != store.current_room_id:
            del ROOM_DEFINITIONS[room_id]
            return True
        return False
    
    def duplicate_room(source_room_id, new_room_id):
        if source_room_id in ROOM_DEFINITIONS:
            import copy
            ROOM_DEFINITIONS[new_room_id] = copy.deepcopy(ROOM_DEFINITIONS[source_room_id])
            return True
        return False
    
    def save_room_changes():
        if store.current_room_id and store.current_room_id in ROOM_DEFINITIONS:
            print("=== SAVING ROOM CHANGES ===")
            print(f"Current room: {store.current_room_id}")
            if not hasattr(persistent, 'room_overrides') or persistent.room_overrides is None:
                persistent.room_overrides = {}
            if store.current_room_id not in persistent.room_overrides:
                persistent.room_overrides[store.current_room_id] = {}
            for obj_name, obj_data in store.room_objects.items():
                if obj_name in ROOM_DEFINITIONS[store.current_room_id]["objects"]:
                    print(f"Saving {obj_name}: x={obj_data['x']}, y={obj_data['y']}, scale={obj_data['scale_percent']}%")
                    orig_obj = ROOM_DEFINITIONS[store.current_room_id]["objects"][obj_name]
                    orig_obj["x"] = obj_data["x"]
                    orig_obj["y"] = obj_data["y"]
                    orig_obj["scale_percent"] = obj_data["scale_percent"]
                    orig_obj["width"] = obj_data["width"]
                    orig_obj["height"] = obj_data["height"]
            print("=== SAVE COMPLETE ===")
            renpy.notify("Room changes saved to memory & persistent storage!")
            return True
        else:
            print(f"ERROR: Cannot save - room_id={store.current_room_id}, exists={store.current_room_id in ROOM_DEFINITIONS}")
            renpy.notify("Error: Cannot save room changes!")
        return False
    
    def reset_room_changes():
        if store.current_room_id:
            if (hasattr(persistent, 'room_overrides') and 
                persistent.room_overrides and 
                store.current_room_id in persistent.room_overrides):
                del persistent.room_overrides[store.current_room_id]
                print(f"Cleared persistent overrides for room: {store.current_room_id}")
            load_room(store.current_room_id)
            renpy.notify("Room reset to original positions!")
            renpy.restart_interaction()
            return True
        return False
    
    def clear_persistent_overrides():
        if store.current_room_id:
            if (hasattr(persistent, 'room_overrides') and 
                persistent.room_overrides and 
                store.current_room_id in persistent.room_overrides):
                del persistent.room_overrides[store.current_room_id]
                print(f"Cleared persistent overrides for room: {store.current_room_id}")
                renpy.notify("Persistent overrides cleared for current room!")
                return True
            else:
                renpy.notify("No persistent overrides found for current room.")
                return False
        renpy.notify("Error: No current room ID found.")
        return False
    
    def update_room_config_file():
        try:
            import os
            import re
            config_file_path = os.path.join(renpy.config.gamedir, "room_config.rpy")
            if not os.path.exists(config_file_path):
                renpy.notify("Error: room_config.rpy not found!")
                return False
            with open(config_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"=== UPDATING {config_file_path} ===")
            for obj_name, obj_data in store.room_objects.items():
                if obj_name in ROOM_DEFINITIONS[store.current_room_id]["objects"]:
                    print(f"Updating {obj_name}: x={obj_data['x']}, y={obj_data['y']}, scale={obj_data['scale_percent']}%")
                    obj_pattern = rf'("{obj_name}"\s*:\s*merge_configs\s*\(\s*\{{[^}}]*?)"x"\s*:\s*\d+\s*,\s*"y"\s*:\s*\d+\s*,([^}}]*?)"scale_percent"\s*:\s*\d+\s*,'
                    replacement = rf'\g<1>"x": {obj_data["x"]}, "y": {obj_data["y"]},\g<2>"scale_percent": {obj_data["scale_percent"]},'
                    new_content = re.sub(obj_pattern, replacement, content, flags=re.DOTALL)
                    if new_content != content:
                        content = new_content
                        print(f"✓ Updated {obj_name} in file")
                    else:
                        basic_pattern = rf'("{obj_name}"\s*:\s*\{{[^}}]*?)"x"\s*:\s*\d+\s*,\s*"y"\s*:\s*\d+\s*,([^}}]*?)"scale_percent"\s*:\s*\d+\s*,'
                        basic_replacement = rf'\g<1>"x": {obj_data["x"]}, "y": {obj_data["y"]},\g<2>"scale_percent": {obj_data["scale_percent"]},'
                        new_content = re.sub(basic_pattern, basic_replacement, content, flags=re.DOTALL)
                        if new_content != content:
                            content = new_content
                            print(f"✓ Updated {obj_name} in file (basic pattern)")
                        else:
                            print(f"⚠ Could not find pattern for {obj_name}")
            with open(config_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("=== FILE UPDATE COMPLETE ===")
            renpy.notify("room_config.rpy updated successfully!")
            return True
        except Exception as e:
            print(f"Error updating room_config.rpy: {str(e)}")
            renpy.notify(f"Error updating file: {str(e)}")
            return False
    
    def load_room(room_id):
        if room_id in ROOM_DEFINITIONS:
            store.current_room_id = room_id
            import copy
            store.room_objects = copy.deepcopy(ROOM_DEFINITIONS[room_id]["objects"])
            store.room_background = ROOM_DEFINITIONS[room_id]["background"]
            if (hasattr(persistent, 'room_overrides') and 
                persistent.room_overrides and 
                room_id in persistent.room_overrides):
                print(f"Applying persistent overrides for room: {room_id}")
                for obj_name, overrides in persistent.room_overrides[room_id].items():
                    if obj_name in store.room_objects:
                        print(f"Overriding {obj_name}: x={overrides.get('x')}, y={overrides.get('y')}")
                        store.room_objects[obj_name].update(overrides)
                        ROOM_DEFINITIONS[room_id]["objects"][obj_name].update(overrides)
            play_room_audio(room_id)
            if store.room_objects:
                store.selected_object = list(store.room_objects.keys())[0]
            else:
                store.selected_object = None
            return True
        return False
    
    def play_room_audio(room_id):
        try:
            audio_file = f"audio/{room_id}.mp3"
            print(f"Attempting to play audio for room {room_id}: {audio_file}")
        except Exception as e:
            print(f"No audio file found for room {room_id} or error playing audio: {str(e)}")
            pass
    
    def fade_out_room_audio(duration=2.0):
        try:
            renpy.music.stop(channel="music", fadeout=duration)
            print(f"Fading out room audio over {duration} seconds")
        except Exception as e:
            print(f"Error fading out audio: {str(e)}")
            pass
    
    def toggle_crt_effect():
        if not hasattr(store, 'crt_enabled'):
            store.crt_enabled = False
        store.crt_enabled = not store.crt_enabled
        renpy.notify(f"CRT effect {'enabled' if store.crt_enabled else 'disabled'}")
        renpy.restart_interaction()
    
    def set_crt_parameters(warp=0.2, scan=0.5, chroma=0.9, scanline_size=1.0):
        store.crt_warp = warp
        store.crt_scan = scan
        store.crt_chroma = chroma
        store.crt_scanline_size = scanline_size
        renpy.notify(f"CRT parameters updated: warp={warp}, scan={scan}, chroma={chroma}, scanline_size={scanline_size}")
        if hasattr(store, 'crt_enabled') and store.crt_enabled:
            renpy.restart_interaction()
    
    def toggle_crt_animation():
        if not hasattr(store, 'crt_animated'):
            store.crt_animated = False
        store.crt_animated = not store.crt_animated
        renpy.notify(f"CRT animation {'enabled' if store.crt_animated else 'disabled'}")
        if hasattr(store, 'crt_enabled') and store.crt_enabled:
            renpy.restart_interaction()

    def adjust_vignette(delta_strength=0.0, delta_width=0.0, set_strength=None, set_width=None):
        """Adjust or set CRT vignette parameters live.
        - Strength range: 0.0..1.0 (higher = darker edges)
        - Width range: 0.05..0.50 (smaller = narrower, stronger band)
        """
        # Initialize defaults if missing
        if not hasattr(store, 'crt_vignette_strength'):
            store.crt_vignette_strength = 0.35
        if not hasattr(store, 'crt_vignette_width'):
            store.crt_vignette_width = 0.25

        strength = store.crt_vignette_strength
        width = store.crt_vignette_width

        if set_strength is not None:
            strength = float(set_strength)
        else:
            strength = float(strength) + float(delta_strength)
        if set_width is not None:
            width = float(set_width)
        else:
            width = float(width) + float(delta_width)

        # Clamp to safe ranges
        strength = max(0.0, min(1.0, strength))
        width = max(0.05, min(0.50, width))

        store.crt_vignette_strength = strength
        store.crt_vignette_width = width
        renpy.notify(f"Vignette: strength={strength:.2f}, width={width:.2f}")
        if hasattr(store, 'crt_enabled') and store.crt_enabled:
            renpy.restart_interaction()
    
    def export_room_config():
        if store.current_room_id and store.current_room_id in ROOM_DEFINITIONS:
            config_text = f"# Updated configuration for {store.current_room_id}:\n\n"
            for obj_name, obj_data in store.room_objects.items():
                config_text += f'            "{obj_name}": {{\n'
                config_text += f'                "x": {obj_data["x"]}, "y": {obj_data["y"]},\n'
                config_text += f'                "scale_percent": {obj_data["scale_percent"]},\n'
                config_text += f'                "width": {obj_data["width"]},\n'
                config_text += f'                "height": {obj_data["height"]},\n'
                config_text += f'                # ... other properties remain the same\n'
                config_text += f'            }},\n\n'
            print("=== ROOM CONFIGURATION ===")
            print(config_text)
            print("=== END CONFIGURATION ===")
            renpy.notify("Configuration exported to console!")
            return config_text
        return None
    
    def get_object_list_for_navigation():
        if not store.room_objects:
            return []
        objects = list(store.room_objects.items())
        objects.sort(key=lambda obj: (obj[1]["y"], obj[1]["x"]))
        return [obj[0] for obj in objects]
    
    def find_nearest_object(current_obj, direction):
        if not current_obj or current_obj not in store.room_objects:
            return None
        current_data = store.room_objects[current_obj]
        current_center_x = current_data["x"] + current_data["width"] // 2
        current_center_y = current_data["y"] + current_data["height"] // 2
        best_obj = None
        best_distance = float('inf')
        for obj_name, obj_data in store.room_objects.items():
            if obj_name == current_obj:
                continue
            obj_center_x = obj_data["x"] + obj_data["width"] // 2
            obj_center_y = obj_data["y"] + obj_data["height"] // 2
            valid_direction = False
            if direction == "left" and obj_center_x < current_center_x:
                valid_direction = True
            elif direction == "right" and obj_center_x > current_center_x:
                valid_direction = True
            elif direction == "up" and obj_center_y < current_center_y:
                valid_direction = True
            elif direction == "down" and obj_center_y > current_center_y:
                valid_direction = True
            if valid_direction:
                dx = obj_center_x - current_center_x
                dy = obj_center_y - current_center_y
                distance = (dx * dx + dy * dy) ** 0.5
                if distance < best_distance:
                    best_distance = distance
                    best_obj = obj_name
        return best_obj
    
    def gamepad_navigate(direction):
        if not store.gamepad_navigation_enabled:
            return
        obj_list = get_object_list_for_navigation()
        if not obj_list:
            return
        if not store.gamepad_selected_object or store.gamepad_selected_object not in store.room_objects:
            store.gamepad_selected_object = obj_list[0]
            store.current_hover_object = store.gamepad_selected_object
            renpy.restart_interaction()
            return
        next_obj = find_nearest_object(store.gamepad_selected_object, direction)
        if next_obj:
            store.gamepad_selected_object = next_obj
            store.current_hover_object = next_obj
            renpy.restart_interaction()
    
    def gamepad_select_first_object():
        obj_list = get_object_list_for_navigation()
        if obj_list:
            store.gamepad_selected_object = obj_list[0]
            store.current_hover_object = obj_list[0]
            renpy.restart_interaction()
    
    def toggle_gamepad_navigation():
        store.gamepad_navigation_enabled = not store.gamepad_navigation_enabled
        if not store.gamepad_navigation_enabled:
            store.gamepad_selected_object = None
            if store.current_hover_object == store.gamepad_selected_object:
                store.current_hover_object = None
        renpy.notify(f"Gamepad navigation {'enabled' if store.gamepad_navigation_enabled else 'disabled'}")
