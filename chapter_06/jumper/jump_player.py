#!/usr/bin/python3
'''jump_player.py'''
import pgzrun

SPEED = 6
WIDTH = 800
HEIGHT = 300
PLAYER_XPOS, PLAYER_YPOS = 75, HEIGHT-60
ANI_SPEED = 4
JUMP = 18
GRAVITY = 1.0
PLAYER_IMG = 'bot'
bg = []
bg.append(Actor('ground', anchor=('left', 'bottom')))
bg.append(Actor('ground', anchor=('left', 'bottom')))
player = Actor(f'{PLAYER_IMG}0', anchor=('left', 'bottom'))
player.vy = 0
player.frame = 0

bg[1].x = WIDTH
bg[0].y = HEIGHT
bg[1].y = HEIGHT

def reset():
    ''' set starting positions '''
    player.x = PLAYER_XPOS
    player.vy = 0
    player.y = PLAYER_YPOS

def update_bg():
    ''' scroll the background images '''
    bg[0].left -= SPEED
    bg[1].left -= SPEED
    if bg[0].x < -WIDTH:
        bg[0].x = WIDTH
    if bg[1].x < -WIDTH:
        bg[1].x = WIDTH

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

def tap():
    ''' react to taps '''
    if player.vy == 0:
        player.vy -= JUMP

def on_key_down():
    ''' react to key presses '''
    tap()

def on_mouse_down():
    ''' react to mouse clicks '''
    tap()

def update():
    ''' pgzero function to update game objects '''
    update_bg()
    update_player()

def draw():
    ''' pgzero function to establish objects '''
    bg[1].draw()
    bg[0].draw()
    player.draw()

reset()
pgzrun.go()
#End
