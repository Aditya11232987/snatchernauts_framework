# Screens \u0026 UI

- Exploration screen orchestrates hover/selection, description box, and action menu
- Info overlay appears at startup and can be toggled later
- Debug overlay cycles through hidden → compact → verbose

Customization
- Tweak styles and sizes in `game/ui/` and `game/overlays/`
- Add transforms/transitions to taste

Example composition (simplified)
```renpy
screen room_exploration():
    default hover_obj = current_hover_object()
    use description_box(hover_obj)
    use object_list()
    if hover_obj:
        use object_actions(hover_obj)
```

