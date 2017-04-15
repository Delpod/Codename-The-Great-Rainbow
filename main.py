try:
    import sys
    import random
    import math
    import os
    import pygame
    import helpers
    from pygame.locals import *
    from helpers import *
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)

class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('button.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('xd')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((127, 127, 127))

global button
button = Button()

buttons = pygame.sprite.RenderPlain((button))

screen.blit(background, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if(event.type == QUIT):
            sys.exit(2)
    screen.blit(background, button.rect, button.rect)
    buttons.draw(screen)
    pygame.display.flip()