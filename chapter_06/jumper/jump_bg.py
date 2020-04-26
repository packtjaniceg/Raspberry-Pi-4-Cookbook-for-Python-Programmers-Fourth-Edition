#!/usr/bin/python3
'''jump_bg.py'''
import pgzrun

SPEED = 6
WIDTH = 800
HEIGHT = 300

bg=[]
bg.append(Actor('ground', anchor=('left', 'bottom')))
bg.append(Actor('ground', anchor=('left', 'bottom')))

bg[1].x = WIDTH
bg[0].y = HEIGHT
bg[1].y = HEIGHT

def update_bg():
    ''' scroll the background images '''
    bg[0].left -= SPEED
    bg[1].left -= SPEED
    if bg[0].x < -WIDTH:
        bg[0].x = WIDTH
    if bg[1].x < -WIDTH:
        bg[1].x = WIDTH

def update():
    ''' pgzero function to update game objects '''
    update_bg()

def draw():
    ''' pgzero function to establish objects '''
    bg[1].draw()
    bg[0].draw()

pgzrun.go()
#End
