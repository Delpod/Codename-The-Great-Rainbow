try:
    import sys
    import random
    import math
    import os
    import pygame
    import pygame.font
    import helpers
    from pygame.locals import *
    from helpers import *
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)

class Clickable(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect((0,0,0,0))

    def checkClick(self, mousePos):
        if(self.rect.collidepoint(mousePos[0], mousePos[1])):
            return True, self.onClick()
        else:
            return False, None

    def onClick(self):
        pass

class Button(Clickable):
    def __init__(self, text):
        Clickable.__init__(self)
        self.image, self.rect = load_img('button.png')
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.text, self.textRect = create_text(text)
        self.textRect.center = ((self.rect[0] + self.rect[2]/2), (self.rect[1] + self.rect[3]/2))

    def drawText(self):
        self.screen.blit(self.text, self.textRect)


pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('xd')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

global button
global text
button = Button('0')

buttons = pygame.sprite.RenderPlain((button))

screen.blit(background, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if(event.type == QUIT):
            sys.exit(2)
        elif(event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
            for b in buttons.sprites():
                b.checkClick(pygame.mouse.get_pos())

    screen.blit(background, button.rect, button.rect)
    buttons.draw(screen)
    for b in buttons.sprites():
        b.drawText()
    pygame.display.flip()