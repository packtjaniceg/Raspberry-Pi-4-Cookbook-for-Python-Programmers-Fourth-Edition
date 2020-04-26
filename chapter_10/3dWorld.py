#!/usr/bin/python3
'''3dWorld.py'''
''' An example of generating a 3D environment using an elevation map
'''
from math import sin, cos, radians
import pi3d

DISPLAY = pi3d.Display.create(x=50, y=50)
#Capture mouse and key presses
INPUTS = pi3d.InputEvents()

def limit(value, min_value, max_value):
    if value < min_value:
        value = min_value
    elif value > max_value:
        value = max_value
    return value

def main():
    CAMERA = pi3d.Camera.instance()
    tex = pi3d.Texture("textures/grass.jpg")
    flatsh = pi3d.Shader("uv_flat")
    # Create elevation map
    mapwidth, mapdepth, mapheight = 200.0, 200.0, 50.0
    mymap = pi3d.ElevationMap("textures/Map.png",
                  width=mapwidth, depth=mapdepth, height=mapheight,
                  divx=128, divy=128, ntiles=20)
    mymap.set_draw_details(flatsh, [tex], 1.0, 1.0)

    rot = 0.0 # rotation of camera
    tilt = 0.0 # tilt of camera
    height = 20
    viewhight = 4
    sky = 200
    xm, ym, zm = 0.0, height, 0.0
    on_ground = False
    # Main display loop
    while DISPLAY.loop_running() and not INPUTS.key_state("KEY_ESC"):
        INPUTS.do_input_events()
        #Camera steered by mouse
        #Note:Some mice devices will be located on
        #get_mouse_movement(1) instead of get_mouse_movement()
        mx, my, mv, mh, md = INPUTS.get_mouse_movement()
        #mx, my, mv, mh, md = INPUTS.get_mouse_movement(1)
        rot -= (mx)*0.2
        tilt -= (my)*0.2
        CAMERA.reset()
        CAMERA.rotate(-tilt, rot, 0)
        CAMERA.position((xm, ym, zm))
        mymap.draw()
        if INPUTS.key_state("KEY_W"):
            xm -= sin(radians(rot))
            zm += cos(radians(rot))
        elif INPUTS.key_state("KEY_S"):
            xm += sin(radians(rot))
            zm -= cos(radians(rot))
        elif INPUTS.key_state("KEY_R"):
            ym += 2
            on_ground = False
        elif INPUTS.key_state("KEY_T"):
            ym -= 2
        ym -= 0.1 #Float down!
        #Limit the movement
        xm = limit(xm, -(mapwidth/2), mapwidth/2)
        zm = limit(zm, -(mapdepth/2), mapdepth/2)
        if ym >= sky:
            ym = sky
        #Check on_ground
        ground = mymap.calcHeight(xm, zm) + viewhight
        if on_ground or (ym <= ground):
            ym = mymap.calcHeight(xm, zm) + viewhight
            on_ground = True

try:
    main()
finally:
    INPUTS.release()
    DISPLAY.destroy()
    print("Closed Everything. END")
#End
