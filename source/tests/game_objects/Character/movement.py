import pygame
from pygame.locals import *
import sys
from source.core.ui.Animation import Animation

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

width = 450
height = 330
DISPLAYSURF = pygame.display.set_mode((width, height), 0, 32)

background = pygame.image.load('../../../../assets/background_test.png')
animation = Animation('../../../../assets/bomberman.gif',
                      '../../../../assets/bomberman.txt')
animation = animation.get_sprite()
sprite = animation['right']

posx = 0
posy = 0
velx = 0
vely = 0

counter = 0
while True:
    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(sprite, (posx, posy))

    if velx == 1:
        if counter < 9:
            sprite = animation['move_right1']
        else:
            sprite = animation['move_right2']
    elif velx == -1:
        if counter < 9:
            sprite = animation['move_left1']
        else:
            sprite = animation['move_left2']
    elif vely == -1:
        if counter < 9:
            sprite = animation['move_up1']
        else:
            sprite = animation['move_up2']
    elif vely == 1:
        if counter < 9:
            sprite = animation['move_down1']
        else:
            sprite = animation['move_down2']

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                velx = -1
                if counter < 9:
                    sprite = animation['move_left1']
                else:
                    sprite = animation['move_left2']
            elif event.key == K_RIGHT:
                velx = 1
                if counter < 9:
                    sprite = animation['move_right1']
                else:
                    sprite = animation['move_right2']
            elif event.key == K_UP:
                vely = -1
                if counter < 9:
                    sprite = animation['move_up1']
                else:
                    sprite = animation['move_up2']
            elif event.key == K_DOWN:
                vely = 1
                if counter < 9:
                    sprite = animation['move_down1']
                else:
                    sprite = animation['move_down2']

        if event.type == KEYUP:
            if event.key == K_LEFT:
                velx = 0
                sprite = animation['left']
            elif event.key == K_RIGHT:
                velx = 0
                sprite = animation['right']
            elif event.key == K_UP:
                vely = 0
                sprite = animation['up']
            elif event.key == K_DOWN:
                vely = 0
                sprite = animation['down']

    posx += velx
    posy += vely

    pygame.display.update()
    fpsClock.tick(FPS)

    if counter == 16:
        counter = 0
    else:
        counter += 1
