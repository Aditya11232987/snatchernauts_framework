# Troubleshooting Guide

## Introduction

This guide provides solutions to common issues encountered when working with the Snatchernauts Framework. Issues are organized by category with symptoms, causes, and step-by-step solutions.

## Installation and Setup Issues

### RENPY_SDK Not Found

**Symptoms:**
- Error message: "RENPY_SDK directory not found"
- Launcher script fails to start
- Commands like `scripts/run-game.sh` don't work

**Causes:**
- Ren'Py SDK not installed in expected location
- Environment variable not set or incorrectly configured
- Permissions issues on SDK directory

**Solutions:**

1. **Verify SDK Installation:**
   ```bash
   ls ~/renpy-8.4.1-sdk/
   # Should show renpy.sh and other files
   ```

2. **Set Environment Variable:**
   ```bash
   # For bash/zsh (add to ~/.bashrc or ~/.zshrc)
   export RENPY_SDK=~/renpy-8.4.1-sdk
   
   # Apply immediately
   source ~/.bashrc
   ```

3. **Check Permissions:**
   ```bash
   # Make sure renpy.sh is executable
   chmod +x ~/renpy-8.4.1-sdk/renpy.sh
   ```

4. **Alternative: Use Absolute Paths:**
   ```bash
   # If relative paths cause issues
   export RENPY_SDK=/home/username/renpy-8.4.1-sdk
   ```

### Permission Denied Errors

**Symptoms:**
- "Permission denied" when running scripts
- Can't execute launcher or renpy.sh
- Files appear locked or inaccessible

**Solutions:**

1. **Make Scripts Executable:**
   ```bash
   chmod +x scripts/run-game.sh
   chmod +x scripts/lint.sh
   chmod +x $RENPY_SDK/renpy.sh
   ```

2. **Check Directory Permissions:**
   ```bash
   # Ensure you can read/write in the project directory
   ls -la /path/to/snatchernauts_framework/
   ```

3. **Fix Ownership (if needed):**
   ```bash
   # Only if files are owned by another user
   sudo chown -R $USER:$USER /path/to/snatchernauts_framework/
   ```

## Game Runtime Issues

### Nothing Happens on Object Interaction

**Symptoms:**
- Clicking objects produces no response
- Interaction menus don't appear
- Objects seem non-interactive

**Diagnostic Steps:**

1. **Enable Debug Mode:**
   ```bash
   scripts/run-game.sh --debug
   ```

2. **Check Console Output:**
   - Look for error messages during object interaction
   - Check if hover events are being detected

3. **Verify Object Configuration:**
   ```python
   # Ensure objects have proper actions defined
   ROOM_OBJECTS = {
       "desk": {
           "image": "desk.png",
           "position": (100, 200),
           "actions": ["Examine", "Search"]  # ← Required
       }
   }
   ```

**Common Causes and Solutions:**

1. **Handler Return Value Issues:**
   ```python
   def on_object_interact(room_id, obj, action):
       if obj == "desk" and action == "Examine":
           renpy.say(None, "A wooden desk.")
           return True  # ← Must return True to prevent defaults
       return False  # ← Allow framework to handle other actions
   ```

2. **Missing Object Registration:**
   ```python
   # Make sure room objects are properly registered
   init python:
       # Room objects must be loaded into the system
       room_api.register_room_objects("room1", ROOM1_OBJECTS)
   ```

3. **Z-Order Issues:**
   ```python
   # Objects might be hidden behind background
   show desk zorder 10
   show background zorder 0
   ```

### Visual Artifacts and Display Issues

#### Shader-Related Problems

**Symptoms:**
- Weird colors or visual distortions
- Black screens when effects are enabled
- Flickering or unstable visual effects

**Immediate Solutions:**

1. **Reset All Effects:**
   - Press `R` during gameplay to reset shaders
   - Press `0` to reset CRT settings

2. **Disable Problem Effects:**
   - Press `C` to toggle CRT off
   - Press `L` to toggle letterbox off
   - Check if issue persists

**GPU Compatibility Issues:**

1. **Check GPU Support:**
   ```python
   # Enable shader debugging
   define config.log_gl_shaders = True
   define shader_debug_enabled = True
   ```

2. **Use Software Fallbacks:**
   ```python
   init python:
       # Detect and handle unsupported GPUs
       renderer_info = renpy.get_renderer_info()
       if renderer_info["renderer"] == "sw":
           # Disable complex shaders
           crt_enabled = False
           shader_debug_enabled = True
   ```

3. **Mobile Device Adjustments:**
   ```python
   init python:
       if renpy.mobile:
           # Use simplified effects on mobile
           crt_warp = 0.05  # Reduced curvature
           crt_scanline_intensity = 0.1  # Lighter scanlines
   ```

#### Object Highlighting Problems

**Symptoms:**
- Objects don't highlight on hover
- Highlighting appears in wrong location
- Effects are too subtle or too intense

**Solutions:**

1. **Check Desaturation Settings:**
   ```python
   # Verify object has desaturation configuration
   "desk": {
       "image": "desk.png",
       "position": (100, 200),
       "desaturation_intensity": 0.6,  # Try higher values
       "desaturation_preset": "moderate"  # Or try "explosive_normal"
   }
   ```

2. **Debug Hover Detection:**
   ```python
   def on_object_hover(room_id, obj):
       print(f"[HOVER DEBUG] {room_id}.{obj}")
       # This should print when hovering over objects
   ```

3. **Verify Transform Application:**
   ```python
   # Make sure transforms are being applied
   show desk at object_desaturation_highlight
   ```

### Audio Issues

#### No Sound or Music

**Symptoms:**
- Complete silence during gameplay
- Music doesn't play in rooms
- Sound effects missing

**Diagnostic Steps:**

1. **Check Audio Settings:**
   ```python
   # Verify in game/core/options.rpy
   define config.has_sound = True
   define config.has_music = True
   define config.has_voice = True
   ```

2. **Test Audio Files:**
   ```bash
   # Verify files exist and are accessible
   ls -la game/audio/
   ```

3. **Check File Formats:**
   - Use OGG or MP3 format
   - Avoid WAV files (large and compatibility issues)
   - Keep file paths relative to game/ directory

**Solutions:**

1. **Fix Audio Channel Registration:**
   ```python
   init python:
       renpy.music.register_channel("ambient", mixer="music", loop=True)
       renpy.music.register_channel("sfx", mixer="sfx", loop=False)
   ```

2. **Proper Audio Loading:**
   ```python
   # Use proper audio paths
   renpy.music.play("audio/background.ogg", channel="music")
   renpy.sound.play("audio/click.ogg")
   ```

#### Audio Stuttering or Performance Issues

**Solutions:**

1. **Reduce Audio Quality:**
   - Convert to lower bitrate OGG files
   - Use shorter audio clips where possible

2. **Preload Important Audio:**
   ```python
   # Preload frequently used sounds
   $ renpy.music.queue("audio/common_sound.ogg", clear_queue=False)
   ```

## Development Workflow Issues

### Linting Failures

**Symptoms:**
- `scripts/run-game.sh --lint` reports errors
- Syntax errors prevent game from starting
- Indentation or formatting issues

**Common Lint Errors:**

1. **Indentation Problems:**
   ```python
   # Wrong (mixed tabs and spaces)
   def on_game_start():
   \tstore.test = True  # Tab character
       print("Hello")     # Spaces
   
   # Correct (consistent spaces)
   def on_game_start():
       store.test = True
       print("Hello")
   ```

2. **Missing Colons:**
   ```python
   # Wrong
   if condition
       do_something()
   
   # Correct
   if condition:
       do_something()
   ```

3. **Incorrect String Quotes:**
   ```python
   # Avoid mixing quote types unnecessarily
   renpy.say(None, "This is consistent")
   renpy.say(None, "Don't mix 'quotes' unnecessarily")
   ```

**Lint Fixing Process:**

1. **Run Lint with Details:**
   ```bash
   scripts/run-game.sh --lint
   # Read error messages carefully
   ```

2. **Fix One Error at a Time:**
   - Address the first error reported
   - Re-run lint to see if it fixed subsequent errors

3. **Use Text Editor Features:**
   - Enable "Show Whitespace" to see tabs vs spaces
   - Use auto-indent features
   - Set editor to use spaces instead of tabs

### Build and Distribution Problems

#### Build Failures

**Symptoms:**
- Ren'Py Launcher build fails
- Missing files in distribution
- Distribution crashes on other systems

**Solutions:**

1. **Use Ren'Py Launcher (Not CLI):**
   ```bash
   # Wrong - headless CLI doesn't support distribute
   $RENPY_SDK/renpy.sh . distribute
   
   # Correct - use the GUI launcher
   $RENPY_SDK/renpy.sh launcher
   # Then: Select project → Build & Distribute
   ```

2. **Check Build Configuration:**
   ```python
   # In game/core/options.rpy
   define build.name = "snatchernauts_framework"
   define build.itch_project = "YourUsername/your-game-name"
   
   # Ensure proper file exclusions
   build.classify('**~', None)  # Exclude backup files
   build.classify('**.psd', None)  # Exclude source art
   ```

3. **Verify Required Files:**
   - Check that all referenced images exist
   - Ensure audio files are included
   - Test that fonts are properly bundled

#### Platform-Specific Issues

**Windows Builds:**
- Include necessary Visual C++ redistributables
- Test on systems without development tools installed

**Mac Builds:**
- Handle code signing requirements
- Test on different macOS versions

**Linux Builds:**
- Check library dependencies
- Test on different distributions

### Memory and Performance Issues

#### High Memory Usage

**Symptoms:**
- Game uses excessive RAM
- Slowdowns during gameplay
- System becomes unresponsive

**Solutions:**

1. **Optimize Images:**
   - Use appropriate image sizes (don't use 4K for small objects)
   - Convert large images to WEBP or optimized PNG
   - Use Ren'Py's image optimization features

2. **Manage Audio Resources:**
   - Use streaming for long audio files
   - Unload unused audio channels
   ```python
   renpy.music.stop(channel="ambient", fadeout=1.0)
   ```

3. **Clean Up Objects:**
   ```python
   # Remove objects that are no longer needed
   renpy.hide("large_background")
   # Use renpy.free_memory() sparingly in extreme cases
   ```

#### Low Frame Rate

**Solutions:**

1. **Disable Expensive Effects:**
   ```python
   # Temporarily disable for testing
   crt_enabled = False
   film_grain_enabled = False
   ```

2. **Reduce Shader Complexity:**
   - Lower CRT scanline resolution
   - Reduce number of simultaneous effects
   - Use simpler desaturation presets

3. **Profile Performance:**
   ```python
   # Enable performance monitoring
   define config.profile = True
   define config.profile_init = True
   ```

## Logging and Debug Issues

### Excessive Log Output

**Symptoms:**
- Console floods with debug messages
- Performance impact from logging
- Difficulty finding relevant information

**Solutions:**

1. **Adjust Logging Levels:**
   ```python
   # In game/core/options.rpy
   default sn_log_enabled = True    # Master switch
   default sn_log_color = True      # Colored output
   default sn_log_intercept_prints = False  # Reduce noise
   ```

2. **Use Debug Overlay Controls:**
   - Press `Ctrl+Shift+F12` to cycle debug overlay
   - Use overlay toggles to control specific logging categories

3. **Filter Debug Output:**
   ```python
   # Add category-specific controls
   bloom_debug_enabled = False   # Disable bloom debugging
   shader_debug_enabled = False  # Disable shader debugging
   ```

### Missing Debug Information

**Symptoms:**
- Can't see what's happening during errors
- Need more detailed troubleshooting info

**Solutions:**

1. **Enable Comprehensive Debugging:**
   ```bash
   scripts/run-game.sh --debug
   ```

2. **Activate Specific Debug Systems:**
   ```python
   # Enable various debug systems
   bloom_debug_enabled = True
   bloom_debug_verbose = True
   shader_debug_enabled = True
   ```

3. **Add Custom Debug Output:**
   ```python
   def on_object_interact(room_id, obj, action):
       print(f"[INTERACTION] {room_id}.{obj} → {action}")
       # Your interaction logic here
   ```

## Getting Additional Help

### Before Asking for Help

1. **Gather Information:**
   - Note exact error messages
   - Record steps to reproduce the issue
   - Note your operating system and Ren'Py version
   - Try with debug mode enabled

2. **Check Recent Changes:**
   - What was the last thing you modified?
   - Does the issue occur with a fresh project?
   - Have you updated any system components recently?

3. **Test with Minimal Setup:**
   - Disable all effects and test basic functionality
   - Try with a simple room configuration
   - Test with default framework settings

### Diagnostic Information to Collect

```bash
# System information
echo "OS: $(uname -a)"
echo "Ren'Py SDK: $RENPY_SDK"
ls -la $RENPY_SDK/renpy.sh

# Project information
echo "Project directory: $(pwd)"
ls -la game/

# Check for common files
ls -la game/core/options.rpy
ls -la game/logic/game_logic.rpy

# Test basic functionality
scripts/run-game.sh --lint --debug
```

### Common Error Patterns

#### "Module Not Found" Errors
- Check file paths are correct
- Verify Python import statements
- Ensure files are in the correct directories

#### "Undefined Variable" Errors
- Check variable initialization
- Verify variable scope (store vs local)
- Look for typos in variable names

#### "Transform Not Found" Errors
- Verify transform definitions
- Check for proper initialization order
- Ensure transforms are defined before use

## Emergency Recovery

### Project Won't Start At All

1. **Backup Current State:**
   ```bash
   cp -r game game_backup_$(date +%Y%m%d)
   ```

2. **Reset to Known Good State:**
   - Revert to last working version
   - Or start with a fresh framework copy
   - Gradually add back your changes

3. **Minimal Test Configuration:**
   ```python
   # Create minimal game/script.rpy for testing
   label start:
       "Hello, world!"
       return
   ```

### Corrupted Save Files or Settings

1. **Clear Persistent Data:**
   ```bash
   # Location varies by OS - check Ren'Py documentation
   rm -rf ~/.renpy/snatchernauts_framework-*/
   ```

2. **Reset to Default Settings:**
   - Delete persistent save data
   - Restart game to regenerate clean settings

3. **Verify Project Integrity:**
   ```bash
   # Check for corrupted or missing files
   find game/ -name "*.rpy" -exec python -m py_compile {} \;
   ```

Remember: when in doubt, start with the simplest possible configuration and build complexity back up gradually. Most issues can be resolved by methodically isolating the problem through systematic testing.

