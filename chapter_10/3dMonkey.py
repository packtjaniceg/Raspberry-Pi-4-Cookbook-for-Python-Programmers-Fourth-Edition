#!/usr/bin/python3
'''3dModel.py'''
''' Wavefront obj model loading. Material properties set in
    mtl file. Uses the import pi3d method to load *everything*
'''

import pi3d


# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create()
# Fetch key presses
INPUTS = pi3d.InputEvents()

def main():
    #Model textures and shaders
    shader = pi3d.Shader("uv_reflect")
    bumptex = pi3d.Texture("textures/floor_nm.jpg")
    shinetex = pi3d.Texture("textures/stars.jpg")
    #Load model
    my_model = pi3d.Model(file_string='models/monkey.obj',
                          name='monkey', z=4)
    my_model.set_shader(shader)
    my_model.set_normal_shine(bumptex, 4.0, shinetex, 0.5)


    #Create environment box
    flatsh = pi3d.Shader("uv_flat")
    ectex = pi3d.loadECfiles("textures/ecubes", "sbox")
    my_ecube = pi3d.EnvironmentCube(size=900.0, maptype="FACES",
                                    name="cube")
    my_ecube.set_draw_details(flatsh, ectex)

    CAMERA = pi3d.Camera.instance()
    rot = 0.0 # rotation of camera
    tilt = 0.0 # tilt of camera

    #Main display loop
    while DISPLAY.loop_running() and not \
                                 INPUTS.key_state("KEY_ESC"):
        #Rotate camera
        INPUTS.do_input_events()
        #Camera steered by mouse
        #Note:Some mice devices will be located on
        #get_mouse_movement(1) instead of get_mouse_movement()
        mx, my, mv, mh, md = INPUTS.get_mouse_movement()
        #mx, my, mv, mh, md = INPUTS.get_mouse_movement(1)
        rot -= (mx)*0.2
        tilt -= (my)*0.2
        CAMERA.reset()
        CAMERA.rotate(tilt, rot, 0)
        #Rotate object
        my_model.rotateIncY(2.0)
        my_model.rotateIncZ(0.1)
        my_model.rotateIncX(0.3)
        #Draw objects
        my_model.draw()
        my_ecube.draw()

try:
    main()
finally:
    INPUTS.release()
    DISPLAY.destroy()
    print("Closed Everything. END")
#End
