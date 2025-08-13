# Simple Working Shaders for Testing
# Basic shader effects that work without complex animation
#
# This file provides working shader transforms that can be applied
# to test the shader system integration

# For now, use basic visual transforms that work without shaders
# until we can properly integrate with the shader system

# Simple visual effects using built-in Ren'Py transforms
transform simple_grain:
    # Simulate grain with slight alpha and tint variation
    alpha 0.95
    matrixcolor TintMatrix("#f8f8f0")

transform simple_fog:
    # Simulate fog with desaturation and tint
    matrixcolor SaturationMatrix(0.7) * TintMatrix("#d0d0e0")
    alpha 0.9

transform simple_lighting:
    # Simulate different lighting with color adjustment
    matrixcolor BrightnessMatrix(-0.1) * ContrastMatrix(1.1) * TintMatrix("#fff8e0")

transform test_grain:
    # More pronounced grain effect
    alpha 0.92
    matrixcolor TintMatrix("#f0f0e8") * ContrastMatrix(1.15)

transform test_fog:
    # Heavier fog effect
    matrixcolor SaturationMatrix(0.5) * TintMatrix("#c8c8d8") * BrightnessMatrix(-0.05)
    alpha 0.85

# Test that the basic system works
transform shader_test:
    # Simple color tint to verify shader application is working
    matrixcolor TintMatrix("#ffe0e0")
    alpha 0.95
