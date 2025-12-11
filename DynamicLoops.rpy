# The animation will loop continuously in the background.
screen loopingMovie( anim_name ):

    zorder 0
    
    # Timer to update animation frames at 24fps (1/24 ≈ 0.0417 seconds)
    timer 0.0417 repeat True action Function(update_animation, anim_name)
    
    # Display the current frame from the animation state
    python:
        data = _animations.get(anim_name)
        if data and data['frames'] and data['index'] < len(data['frames']):
            current_frame = data['frames'][data['index']]
    
    if current_frame is not None:
        add current_frame

    # The animation runs in the background. Avoid consuming input so
    # dialogue and clicks still reach the screens above (say window).


## dynamically generate animations from frame folders
init python:
    import os
    import re

    # Global animations state. Keys are folder names, values are dicts:
    # {frames: [Displayable,...], frame_duration: float, index: int,
    #  playing: bool, stop_after_loop: bool}
    _animations = {}

    def create_animation_from_folder(anim_name):
        """
        Loads frames (as Image displayables) from a folder and stores them
        in the global `_animations` dict. Frames are sorted naturally and
        will play at 24 FPS.
        """
        folder_path = os.path.join(config.basedir, "game", "images", anim_name)

        if not os.path.exists(folder_path):
            return None

        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]

        def natural_sort_key(filename):
            return [int(text) if text.isdigit() else text.lower()
                    for text in re.split(r'(\d+)', filename)]

        files.sort(key=natural_sort_key)

        if not files:
            return None

        frame_duration = 1.0 / 24.0
        frames = []
        for frame_file in files:
            frame_path = os.path.join("images", anim_name, frame_file)
            frames.append(Image(frame_path))

        # Duplicate last frame to reduce skipping (optional)
        if frames:
            frames.append(frames[-1])

        # Store into _animations
        _animations[anim_name] = {
            'frames': frames,
            'frame_duration': frame_duration,
            'index': 0,
            'playing': False,
        }

        return _animations[anim_name]

    def update_animation(anim_name):
        """
        Called by the screen timer to advance the frame index.
        """
        data = _animations.get(anim_name)
        if not data or not data['playing']:
            return

        data['index'] = (data['index'] + 1) % len(data['frames'])

    def play_animation(anim_name, fade_in=None):
        """
        Start playing an animation in the background. The animation will
        loop until stop_animation() is called.
        
        Args:
            anim_name: Name of the animation folder (e.g., "cube_fast")
            fade_in: Optional transition to fade in the animation 
                (e.g., Dissolve(0.5), Fade(0.3, 0, 0.3))
        
        Usage: 
            play_animation("cube_fast")
            play_animation("cube_fast", fade_in=Dissolve(0.5))
        """
        data = _animations.get(anim_name)
        if not data:
            # Try to load it on demand
            data = create_animation_from_folder(anim_name)
            if not data:
                return

        # If already playing, restart from first frame; otherwise start playing.
        if data.get('playing'):
            data['index'] = 0
        else:
            data['playing'] = True
            data['index'] = 0
        
        renpy.show_screen('loopingMovie', anim_name)
        if fade_in:
            renpy.transition(fade_in)

    def stop_animation(fade_out=None):
        """
        Stop the currently playing animation immediately with optional transition.
        
        Args:
            fade_out: Optional transition to fade out the animation
                (e.g., Dissolve(0.5), Fade(0.3, 0, 0.3))
        
        Usage: 
            stop_animation()
            stop_animation(fade_out=Dissolve(0.5))
        """
        # Find and stop the visible animation
        for name, data in _animations.items():
            if data.get('playing'):
                data['playing'] = False
                break
        
        renpy.hide_screen('loopingMovie')
        if fade_out:
            renpy.transition(fade_out)

    # Load available animation folders at init
    images_dir = os.path.join(config.basedir, 'game', 'images')
    if os.path.exists(images_dir):
        for d in sorted(os.listdir(images_dir)):
            full = os.path.join(images_dir, d)
            if os.path.isdir(full):
                create_animation_from_folder(d)


