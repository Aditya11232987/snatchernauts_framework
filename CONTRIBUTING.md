# Contributing to Snatchernauts Framework

Thank you for your interest in contributing to the Snatchernauts Framework! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the [GitLab Issues](../../issues) to report bugs or request features
- Search existing issues before creating a new one
- Provide clear reproduction steps for bugs
- Include system information (OS, Ren'Py version, etc.)

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitLab, then clone your fork
   git clone https://gitlab.com/yourusername/snatchernauts_framework.git
   cd snatchernauts_framework
   ```

2. **Set up Development Environment**
   ```bash
   # Ensure you have Ren'Py 8.3.7+ installed
   # Add your Ren'Py SDK to PATH or use full path
   /path/to/renpy/renpy.sh .
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number
   ```

## 📝 Coding Standards

### Python/Ren'Py Code Style
- Follow PEP 8 Python style guidelines where applicable
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable and function names
- Add docstrings to all functions and classes

Example:
```python
def calculate_bloom_intensity(base_intensity, hover_state, time_offset):
    \"\"\"Calculate the current bloom intensity based on animation state.
    
    Args:
        base_intensity (float): Base glow intensity (0.0-1.0)
        hover_state (bool): Whether object is currently hovered
        time_offset (float): Time offset for pulsing animation
        
    Returns:
        float: Calculated intensity value
    \"\"\"
    if hover_state:
        return base_intensity * (1.0 + 0.2 * math.sin(time_offset))
    return base_intensity
```

### File Organization
- Keep related functionality in separate modules
- Use descriptive file names (e.g., `bloom_effects.rpy`, `gamepad_input.rpy`)
- Place utility functions in appropriate utility modules
- Follow the existing directory structure

### Ren'Py Specific Guidelines
- Use `init python:` blocks for Python code that needs early initialization  
- Use `default` statements for variables that should persist
- Prefer `store.` prefix for global variables in functions
- Use appropriate priority levels for init blocks

## 🎨 Asset Guidelines

### Images
- **Format**: PNG with transparency support
- **Room Backgrounds**: 1280x720 resolution
- **Objects**: Any size, but consider memory usage
- **UI Elements**: Use consistent styling
- **Pixel Art**: Use multiples of 8 pixels for crisp rendering

### Naming Conventions
- Use lowercase with underscores: `detective_idle.png`
- Be descriptive: `room1_background.png` vs `bg1.png`
- Group related assets in subdirectories

## 🧪 Testing

### Manual Testing
- Test on multiple platforms if possible (Windows, Mac, Linux)
- Test both mouse and gamepad input
- Verify all editor mode functions work correctly
- Check visual effects on different graphics settings
- Test room transitions and object interactions

### Test Cases to Cover
- [ ] Room loading and object positioning
- [ ] Gamepad navigation between objects
- [ ] Description box positioning in all corners
- [ ] Bloom effects rendering correctly
- [ ] Editor mode object manipulation
- [ ] Persistent state saving/loading
- [ ] Font rendering at different sizes

## 📋 Submitting Changes

### Commit Guidelines
- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Keep commits focused on a single change

Examples:
```bash
git commit -m "Add bloom intensity animation system"
git commit -m "Fix gamepad navigation wrapping (#123)"
git commit -m "Update README with installation instructions"
```

### Merge Request Process
1. Ensure your code follows the style guidelines
2. Update documentation if needed
3. Add yourself to the contributors list if it's your first contribution
4. Create a merge request with:
   - Clear title and description
   - Reference to related issues
   - Screenshots/GIFs for visual changes
   - Test results summary

### Merge Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] Manual testing completed
- [ ] Works on multiple platforms
- [ ] No regression in existing features

## Screenshots (if applicable)
[Include screenshots or GIFs of visual changes]

## Related Issues
Fixes #[issue number]
```

## 🔧 Development Areas

We welcome contributions in these areas:

### High Priority
- **Mobile/Touch Support** - Touch controls for Android/iOS
- **Audio Integration** - Sound effects and music system
- **Performance Optimization** - Memory and rendering improvements
- **Accessibility** - Screen reader support, colorblind-friendly options

### Medium Priority  
- **Animation System** - Timeline-based animations
- **Particle Effects** - Visual enhancement system
- **Save/Load Integration** - Game state management
- **Dialogue Integration** - Character conversation system

### Documentation
- **Wiki Pages** - Detailed tutorials and guides
- **Code Examples** - More usage examples
- **Video Tutorials** - Visual learning resources
- **API Documentation** - Comprehensive function reference

## 🎯 Feature Request Guidelines

When requesting new features:

1. **Check Existing Issues** - Avoid duplicates
2. **Describe the Use Case** - Why is this needed?
3. **Provide Examples** - Show how it would be used
4. **Consider Implementation** - Any technical constraints?
5. **Discuss Impact** - How does it affect existing features?

## 📞 Getting Help

- **GitLab Issues** - For bugs and feature requests
- **GitLab Discussions** - For questions and general discussion
- **Wiki** - For documentation and tutorials
- **Code Comments** - Check inline documentation

## 🏆 Recognition

Contributors are recognized in:
- README.md contributors section
- CHANGELOG.md for specific contributions
- Git commit history
- Release notes for significant contributions

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make Snatchernauts Framework better!** 🎮✨
