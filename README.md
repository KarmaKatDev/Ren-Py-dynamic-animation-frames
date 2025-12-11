# Dynamic Animation System for Ren'Py

A flexible, frame-based animation system for Ren'Py that dynamically loads animation frames from folder structures and plays them at 24fps. Animations loop in the background while dialogue and other visual elements play on top.

## Features

- **Dynamic Folder Loading**: Automatically discovers and loads animation folders from `game/images/`
- **24fps Playback**: All animations play at a consistent 24 frames per second
- **Natural Frame Sorting**: Frames are sorted numerically (handles `f1.png`, `f2.png`, etc. correctly)
- **Background Looping**: Animations loop continuously in the background without blocking dialogue
- **Smooth Transitions**: Optional fade-in and fade-out transitions using Ren'Py's built-in transition effects
- **Easy API**: Simple Python function calls from your script.rpy

## File Structure

```
game/
├── DynamicLoops.rpy        # Animation system (screen + Python code)
├── script.rpy              # Your main script (uses animations)
└── images/
    ├── animation 1/          # Animation folder (can be any name)
    │   ├── f1.png            # does not literally have to be f1, f2, etc. it reads the frames in alphabetical order
    │   ├── f2.png
    │   └── ...
    └── animation 2/          # Another animation folder
        ├── f1.png
        ├── f2.png
        └── ...
```

## Setup

1. **Copy `DynamicLoops.rpy`** into your `game/` directory
2. **Create animation folders** in `game/images/`:
   - Each folder name becomes an animation name (e.g., `cube_fast`)
   - Add PNG frames sorted numerically (e.g., `f1.png`, `f2.png`, `f3.png`, etc.)
3. **Use in your script** with simple function calls (see examples below)

## API Reference

### `play_animation(anim_name, fade_in=None)`

Starts playing an animation in the background. The animation will loop continuously until `stop_animation()` is called.

**Parameters:**
- `anim_name` (str): Name of the animation folder (e.g., `"cube_fast"`)
- `fade_in` (Transition, optional): Optional Ren'Py transition to fade in the animation

**Returns:** None

**Examples:**

```renpy
# Basic usage
$ play_animation("cube_fast")

# With fade-in transition
$ play_animation("cube_slow", fade_in=Dissolve(0.5))

# Then display dialogue while animation plays
e "This dialogue appears while the animation loops in the background."

# Switch animations
$ stop_animation(fade_out=Dissolve(0.3))
$ play_animation("cube_fast", fade_in=Dissolve(0.3))
```

### `stop_animation(fade_out=None)`

Stops the currently playing animation immediately and hides it.

**Parameters:**
- `fade_out` (Transition, optional): Optional Ren'Py transition to fade out the animation

**Returns:** None

**Examples:**

```renpy
# Stop without transition
$ stop_animation()

# Stop with fade-out
$ stop_animation(fade_out=Dissolve(0.5))
```

## Built-in Transitions

Ren'Py provides many transition effects you can use:

| Transition | Description |
|-----------|-------------|
| `Dissolve(duration)` | Smooth fade transition (e.g., `Dissolve(0.5)`) |
| `Fade(in_time, stay_time, out_time)` | Fade to black then back (e.g., `Fade(0.3, 0, 0.3)`) |
| `Pixelate(duration)` | Pixelation effect |
| `ZoomInOut(duration)` | Zoom effect |
| `Wipe(duration, direction)` | Wipe across screen |

## Internal Functions

### `create_animation_from_folder(anim_name)`

Loads all PNG frames from a folder in `game/images/<anim_name>/`. Automatically sorts frames numerically and stores them in the global animation state.

**Called automatically at init time for all discovered animation folders.**

### `update_animation(anim_name)`

Advances the frame index for the specified animation. Called by the screen's timer every 0.0417 seconds (24fps).

**You should not call this directly** — it's used internally by the `loopingMovie` screen.

## Global State

The system maintains a global `_animations` dictionary:

```python
_animations = {
    "cube_fast": {
        'frames': [Image(...), Image(...), ...],
        'frame_duration': 0.0417,  # 24fps
        'index': 0,                # Current frame index
        'playing': False,          # Is animation playing
    },
    ...
}
```

## Screen: `loopingMovie`

The `loopingMovie` screen displays the current animation frame and manages the timer that updates frames at 24fps. It's displayed at `zorder 0` so it renders behind dialogue and UI elements.

**Called automatically by `play_animation()`** — you should not call this directly.

## Complete Example

```renpy
label start:
    scene bg room
    show eileen happy
    
    e "Let me show you an animation..."
    
    # Start animation with fade-in
    $ play_animation("cube_fast", fade_in=Dissolve(0.5))
    
    e "This animation loops in the background."
    e "I can speak multiple lines while it plays."
    e "Dialogue and clicks work normally on top of the animation."
    
    # Transition to a different animation
    $ stop_animation(fade_out=Dissolve(0.3))
    $ play_animation("cube_slow", fade_in=Dissolve(0.3))
    
    e "Now we're showing a slower animation."
    
    # Stop the animation
    $ stop_animation(fade_out=Dissolve(0.5))
    
    e "The animation is now hidden."
    
    return
```

## Troubleshooting

### Animation not found
- Check that your animation folder exists in `game/images/`
- Verify the folder name matches the `anim_name` parameter exactly
- Ensure PNG files are in that folder

### Animation not playing
- Confirm `play_animation()` is called with the correct animation name
- Check that `DynamicLoops.rpy` is in your `game/` directory
- Verify frame files are named with numbers (e.g., `f1.png`, `f2.png`)

### Animation stutters or skips frames
- Ensure your frames are PNG format (compressed lossless)
- Check disk I/O performance
- The last frame is duplicated in the animation to reduce skipping

### Rollback behavior
- Rollback will naturally restore animation state (frame index, playing flag)
- Calling `play_animation()` on the same line multiple times will restart the animation from frame 0

## Performance Notes

- Animations load all frames into memory at startup
- 24fps = ~42ms per frame (standard for smooth animation)
- Each frame is an `Image` displayable (lazy-loaded by Ren'Py)
- Background looping has minimal performance impact

## License

This system builds on concepts from the Ren'Py community. Feel free to use and modify for your projects.

## Support

For issues with Ren'Py itself, see the [official Ren'Py documentation](https://www.renpy.org/doc/html/).
