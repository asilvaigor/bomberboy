import pygame
from pygame.locals import *
import sys
from source.core.ui.Sprite import Sprite

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

width = 450
height = 330
display = pygame.display.set_mode((width, height), 0, 32)

background = pygame.image.load('../../../../assets/background_test.png')
icon = Sprite('../../../../assets/bomberman.gif',
              '../../../../assets/bomberman.txt')
sprite = icon.get_dict()
icon = sprite['right']

posx = 0
posy = 0
velx = 0
vely = 0

counter = 0
while True:
    display.blit(background, (0, 0))
    display.blit(icon, (posx, posy))

    if velx == 1:
        if counter < 9:
            icon = sprite['move_right1']
        else:
            icon = sprite['move_right2']
    elif velx == -1:
        if counter < 9:
            icon = sprite['move_left1']
        else:
            icon = sprite['move_left2']
    elif vely == -1:
        if counter < 9:
            icon = sprite['move_up1']
        else:
            icon = sprite['move_up2']
    elif vely == 1:
        if counter < 9:
            icon = sprite['move_down1']
        else:
            icon = sprite['move_down2']

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                velx = -1
                if counter < 9:
                    icon = sprite['move_left1']
                else:
                    icon = sprite['move_left2']
            elif event.key == K_RIGHT:
                velx = 1
                if counter < 9:
                    icon = sprite['move_right1']
                else:
                    icon = sprite['move_right2']
            elif event.key == K_UP:
                vely = -1
                if counter < 9:
                    icon = sprite['move_up1']
                else:
                    icon = sprite['move_up2']
            elif event.key == K_DOWN:
                vely = 1
                if counter < 9:
                    icon = sprite['move_down1']
                else:
                    icon = sprite['move_down2']

        if event.type == KEYUP:
            if event.key == K_LEFT:
                velx = 0
                icon = sprite['left']
            elif event.key == K_RIGHT:
                velx = 0
                icon = sprite['right']
            elif event.key == K_UP:
                vely = 0
                icon = sprite['up']
            elif event.key == K_DOWN:
                vely = 0
                icon = sprite['down']

    posx += velx * 3
    posy += vely * 3

    pygame.display.update()
    fpsClock.tick(FPS)

    if counter == 16:
        counter = 0
    else:
        counter += 1
