#!/usr/bin/python3
'''3dObject.py'''
''' Create a 3D space with a Tetrahedron inside and rotate the
    view around using the mouse.
'''
from math import sin, cos, radians
import pi3d

DISPLAY = pi3d.Display.create(x=50, y=50)
#capture mouse and key presses
INPUTS = pi3d.InputEvents()

def main():
    CAMERA = pi3d.Camera.instance()
    tex = pi3d.Texture("textures/stripwood.jpg")
    flatsh = pi3d.Shader("uv_flat")

    #Define the coordinates for our shape (x,y,z)
    A = (-1.0, -1.0, -1.0)
    B = (1.0, -1.0, 1.0)
    C = (-1.0, -1.0, 1.0)
    D = (-1.0, 1.0, 1.0)
    ids = ["A", "B", "C", "D"]
    coords = [A, B, C, D]
    my_tetra = pi3d.Tetrahedron(x=0.0, y=0.0, z=0.0,
                                corners=(A, B, C, D))
    my_tetra.set_draw_details(flatsh, [tex])
    # Load ttf font and set the font to black
    arial_font = pi3d.Font("fonts/FreeMonoBoldOblique.ttf",
                           "#000000")
    mystring = []
    #Create string objects to show the coordinates
    for i, pos in enumerate(coords):
        mystring.append(pi3d.String(font=arial_font,
                                    string=ids[i]+str(pos),
                                    x=pos[0], y=pos[1], z=pos[2]))
        mystring.append(pi3d.String(font=arial_font,
                                    string=ids[i]+str(pos),
                                    x=pos[0], y=pos[1], z=pos[2], ry=180))
    for string in mystring:
        string.set_shader(flatsh)

    cam_rad = 4.0 # radius of camera position
    rot = 0.0 # rotation of camera
    tilt = 0.0 # tilt of camera

    #Main display loop
    while DISPLAY.loop_running() and not \
                               INPUTS.key_state("KEY_ESC"):
        INPUTS.do_input_events()
        #Note:Some mice devices will be located on
        #get_mouse_movement(1) instead of get_mouse_movement()
        mx, my, mv, mh, md = INPUTS.get_mouse_movement()
        #mx, my, mv, mh, md = inputs.get_mouse_movement(1)
        rot -= (mx)*0.2
        tilt -= (my)*0.2
        CAMERA.reset()
        CAMERA.rotate(-tilt, rot, 0)
        CAMERA.position((cam_rad * sin(radians(rot)) *
                         cos(radians(tilt)),
                         cam_rad * sin(radians(tilt)),
                         -cam_rad * cos(radians(rot)) *
                         cos(radians(tilt))))
        #Draw the Tetrahedron
        my_tetra.draw()
        for string in mystring:
            string.draw()

try:
    main()
finally:
    INPUTS.release()
    DISPLAY.destroy()
    print("Closed Everything. END")
#End
