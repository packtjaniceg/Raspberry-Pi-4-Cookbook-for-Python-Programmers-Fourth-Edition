#!/usr/bin/python3
'''jump.py'''
import random
import pgzrun

SPEED = 6
WIDTH = 800
HEIGHT = 300
PLAYER_XPOS, PLAYER_YPOS = 75, HEIGHT-60
ANI_SPEED = 4
JUMP = 18
GRAVITY = 1.0
GAP = 200
GAP_MULTI = 2
PLAYER_IMG = 'bot'
HAZARD_IMG = 'hazard'

bg = []
bg.append(Actor('ground', anchor=('left', 'bottom')))
bg.append(Actor('ground', anchor=('left', 'bottom')))
player = Actor(f'{PLAYER_IMG}0', anchor=('left', 'bottom'))
hazards = []
for i in range(0, 4):
    hazards.append(Actor(f'{HAZARD_IMG}0'))
player.vy = 0
player.stop = True
player.frame = 0

bg[1].x = WIDTH
bg[0].y = HEIGHT
bg[1].y = HEIGHT

def get_gap():
    ''' create a suitable gap between our hazards '''
    return GAP + random.randint(0, GAP_MULTI*GAP)

def reset():
    ''' set starting positions '''
    player.x = PLAYER_XPOS
    player.vy = 0
    player.y = PLAYER_YPOS
    gap = 0
    for hazard in hazards:
        hazard.x = WIDTH+gap
        hazard.y = HEIGHT-100
        gap += get_gap()

def update_bg():
    ''' scroll the background images '''
    bg[0].left -= SPEED
    bg[1].left -= SPEED
    if bg[0].x < -WIDTH:
        bg[0].x = WIDTH
    if bg[1].x < -WIDTH:
        bg[1].x = WIDTH

def update_hazards():
    ''' scroll and position hazards '''
    for hazard in hazards:
        hazard.left -= SPEED
        hazard.image = f'{HAZARD_IMG}{random.randint(0,6)}'
        if hazard.right < 0:
            nearest = WIDTH 
            for haz in hazards:
                nearest = max(nearest, haz.right)
            hazard.left = nearest + get_gap()

def update_player():
    ''' handle animation and score player '''
    uy = player.vy
    player.vy += GRAVITY
    player.y += (uy + player.vy) / 2
    if player.y > PLAYER_YPOS:
        player.image = f'{PLAYER_IMG}{player.frame // ANI_SPEED}'
        player.y = PLAYER_YPOS
        player.vy = 0
    else:
        player.image = f'{PLAYER_IMG}up{player.frame // ANI_SPEED}'
    player.frame = (player.frame + 1) % (3*ANI_SPEED)
    for hazard in hazards:
        if player.colliderect(hazard):
            player.stop = True

def tap():
    ''' react to taps '''
    if not player.stop:
        if player.vy == 0:
            player.vy -= JUMP
    else:
        player.stop = False
        reset()

def on_key_down():
    ''' react to key presses '''
    tap()

def on_mouse_down():
    ''' react to mouse clicks '''
    tap()

def update():
    ''' pgzero function to update game objects '''
    if not player.stop:
        update_bg()
        update_hazards()
        update_player()

def draw():
    ''' pgzero function to establish objects '''
    bg[1].draw()
    bg[0].draw()
    player.draw()
    for hazard in hazards:
        hazard.draw()

reset()
pgzrun.go()
#End
