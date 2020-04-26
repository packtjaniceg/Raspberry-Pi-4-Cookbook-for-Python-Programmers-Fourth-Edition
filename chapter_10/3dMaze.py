#!/usr/bin/python3
'''3dMaze.py'''
'''Small maze game, try to find the exit
'''
from math import sin, cos, radians
import pi3d
from pi3d.shape.Building import SolidObject, Size, Position

# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create()
#Load shader
shader = pi3d.Shader("uv_reflect")
flatsh = pi3d.Shader("uv_flat")
# Load textures
ceilingimg = pi3d.Texture("textures/squareblocks4.png")
wallimg = pi3d.Texture("textures/squareblocksred.png")
floorimg = pi3d.Texture("textures/dunes3_512.jpg")
bumpimg = pi3d.Texture("textures/mudnormal.jpg")
startimg = pi3d.Texture("textures/rock1.jpg")
endimg = pi3d.Texture("textures/water.jpg")
# Create elevation map
mapwidth = 1000.0
mapdepth = 1000.0
#We shall assume we are using a flat floor in this example
mapheight = 0.0
mymap = pi3d.ElevationMap(mapfile="textures/floor.png",
                          width=mapwidth, depth=mapdepth,
                          height=mapheight, divx=64, divy=64)
mymap.set_draw_details(shader, [floorimg, bumpimg], 128.0, 0.0)
level_list = ["textures/inside_map0.png",
              "textures/inside_map1.png",
              "textures/inside_map2.png"]
avhgt = 5.0
aveyelevel = 4.0
MAP_BLOCK = 15.0
aveyeleveladjust = aveyelevel - avhgt/2
PLAYERHEIGHT = (mymap.calcHeight(5, 5) + avhgt/2)
#Start the player in the top-left corner
startpos = [(8*MAP_BLOCK), PLAYERHEIGHT, (8*MAP_BLOCK)]
endpos = [0, PLAYERHEIGHT, 0] #Set the end pos in the centre
person = SolidObject("person", Size(1, avhgt, 1),
                     Position(startpos[0], startpos[1],
                              startpos[2]), 1)
#Add spheres for start and end, end must also have a solid object
#so we can detect when we hit it
start_object = pi3d.Sphere(name="start", x=startpos[0],
                           y=startpos[1]+avhgt, z=startpos[2])
start_object.set_draw_details(shader, [startimg, bumpimg],
                              32.0, 0.3)
end_object = pi3d.Sphere(name="end", x=endpos[0],
                         y=endpos[1], z=endpos[2])
end_object.set_draw_details(shader, [endimg, bumpimg], 32.0, 0.3)
end_solid = SolidObject("end", Size(1, avhgt, 1),
                        Position(endpos[0], endpos[1],
                                 endpos[2]), 1)

maze_scheme = {
    "#models": 3,
    (1, None): [["C", 2]],      #white cell : Ceiling
    (0, 1, "edge"): [["W", 1]], #white cell on edge next
                                #   black cell : Wall
    (1, 0, "edge"): [["W", 1]], #black cell on edge next
                                #   to white cell : Wall
    (0, 1): [["W", 0]]          #white cell next
    }                           #   to black cell : Wall

details = [[shader, [wallimg], 1.0, 0.0, 4.0, 16.0],
           [shader, [wallimg], 1.0, 0.0, 4.0, 8.0],
           [shader, [ceilingimg], 1.0, 0.0, 4.0, 4.0]]

arial_font = pi3d.Font("fonts/FreeMonoBoldOblique.ttf",
                       "#ffffff", font_size=10)
INPUTS = pi3d.InputEvents()

def load_level(next_level):
    ''' Load a level '''
    print(">>> Please wait while maze is constructed...")
    next_level = next_level%len(level_list)
    building = pi3d.Building(level_list[next_level], 0, 0, mymap,
                             width=MAP_BLOCK, depth=MAP_BLOCK,
                             height=30.0, name="",
                             draw_details=details, yoff=-15,
                             scheme=maze_scheme)
    return building

def show_message(text, rot=0):
    ''' Display message on screen '''
    message = pi3d.String(font=arial_font, string=text,
                          x=endpos[0], y=endpos[1]+(avhgt/4),
                          z=endpos[2], sx=0.05, sy=0.05, ry=-rot)
    message.set_shader(flatsh)
    message.draw()

def main():
    ''' Main function '''
    #Load a level
    level = 0
    building = load_level(level)
    lights = pi3d.Light(lightpos=(10, -10, 20),
                        lightcol=(0.7, 0.7, 0.7),
                        lightamb=(0.7, 0.7, 0.7))
    rot = 0.0
    tilt = 0.0
    CAMERA = pi3d.Camera.instance()
    while DISPLAY.loop_running() and not \
                                 INPUTS.key_state("KEY_ESC"):
        CAMERA.reset()
        CAMERA.rotate(tilt, rot, 0)
        CAMERA.position((person.x(), person.y(),
                         person.z() - aveyeleveladjust))
        #Draw objects
        person.drawall()
        building.drawAll()
        mymap.draw()
        start_object.draw()
        end_object.draw()
        #Apply the light to all the objects in the building
        for b in building.model:
            b.set_light(lights, 0)
        mymap.set_light(lights, 0)

        INPUTS.do_input_events()
        #Note:Some mice devices will be located on
        #get_mouse_movement(1) instead of get_mouse_movement()
        mx, my, mv, mh, md = INPUTS.get_mouse_movement()
        #mx, my, mv, mh, md = INPUTS.get_mouse_movement(1)
        rot -= (mx)*0.2
        tilt -= (my)*0.2
        xm = person.x()
        ym = person.y()
        zm = person.z()

        #Handle keyboard keys
        if INPUTS.key_state("KEY_APOSTROPHE"):  #key '
            tilt -= 2.0
        if INPUTS.key_state("KEY_SLASH"):  #key /
            tilt += 2.0
        if INPUTS.key_state("KEY_A"):
            rot += 2
        if INPUTS.key_state("KEY_D"):
            rot -= 2
        if INPUTS.key_state("KEY_H"):
            #Use point_at as help - will turn the player to face
            #  the direction of the end point
            tilt, rot = CAMERA.point_at([end_object.x(),
                                         end_object.y(),
                                         end_object.z()])
        if INPUTS.key_state("KEY_W"):
            xm -= sin(radians(rot))
            zm += cos(radians(rot))
        if INPUTS.key_state("KEY_S"):
            xm += sin(radians(rot))
            zm -= cos(radians(rot))
    
        new_pos = Position(xm, ym, zm)
        collisions = person.CollisionList(new_pos)
        if collisions:
            #If we reach end, reset to start position!
            for obj in collisions:
                if obj.name == "end":
                    INPUTS.do_input_events() #clear any pending inputs
                    #Required to remove the building walls from the
                    #  solidobject list
                    building.remove_walls()
                    show_message("Loading Level", rot)
                    DISPLAY.loop_running()
                    level += 1
                    building = load_level(level)
                    show_message("")
                    person.move(Position(startpos[0], startpos[1],
                                         startpos[2]))
        else:
            person.move(new_pos)

try:
    main()
finally:
    INPUTS.release()
    DISPLAY.destroy()
    print("Closed Everything. END")
#End
