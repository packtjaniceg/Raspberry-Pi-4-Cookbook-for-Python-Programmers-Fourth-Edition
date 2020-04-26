#!/usr/bin/python3
'''animate.py'''
import pgzrun

IMG = 'hazard'
sprite = Actor(f'{IMG}0', leftbottom=(0, 0))

WIDTH = sprite.width
HEIGHT = sprite.height
sprite.frame = 0
FRAMES = 6
SPD = 10

def update():
    ''' pgzero function to update game objects '''
    sprite.frame = (sprite.frame+1)%(SPD*FRAMES)
    sprite.image = f'{IMG}{sprite.frame // SPD}'

def draw():
    ''' pgzero function to establish objects '''
    screen.clear()
    sprite.draw()

pgzrun.go()
#End
