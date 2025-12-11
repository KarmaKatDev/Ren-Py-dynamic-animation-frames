# The script of the game goes in this file.

label start:
    scene bg room
    $ play_animation("cube_slow")
    "this is a slow cube"
    "this is still a slow cube"
    "this is now going to switch to a fast cube"
    #$ stop_animation()
    $ play_animation("cube_fast", fade_in=Dissolve(0.3))
    "this is a fast cube"
    $ stop_animation(fade_out=Dissolve(0.3))

    "this is the end of the demo."
    
    
    # This ends the game.

    return
