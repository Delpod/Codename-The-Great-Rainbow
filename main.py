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

global screensize
screensize = (1280, 720)

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
    def __init__(self, pos, text, size=36, name='button.png'):
        Clickable.__init__(self)
        self.image, self.rect = load_img(name)
        self.rect[0], self.rect[1] = pos[0], pos[1]
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.text, self.textRect = create_text(text, size)
        self.textRect.center = ((self.rect[0] + self.rect[2]/2), (self.rect[1] + self.rect[3]/2))

    def drawText(self):
        self.screen.blit(self.text, self.textRect)

    def onClick(self):
        print('Click')

class DigitButton(Button):
    def __init__(self, pos, text, value, size=36):
        Button.__init__(self, pos, text, size)
        self.value = value

    def onClick(self):
        print(self.value)

def initButtons():
    buttons = []
    start = [848, 360]
    for i in range(3):
        for j in range(3):
            val = 1 + j + 3 * i
            buttons.append(DigitButton((start[0] + 80 * j, start[1] - 80 * i), chr(48 + val), val))
    buttons.append(DigitButton((start[0], start[1] + 80), chr(48), 0))
    buttons.append(Button((start[0] + 1 * 80, start[1] + 80), 'Bcksp', 20))
    buttons.append(Button((start[0] + 2 * 80, start[1] + 80), 'Cls', 30))
    buttons.append(Button((start[0] - 16, start[1] + 2 * 80), 'Weigh', 36, 'longbutton.png'))
    return pygame.sprite.RenderPlain(buttons)


pygame.init()
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption('xd')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

buttons = pygame.sprite.RenderPlain(initButtons())

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

    buttons.draw(screen)
    for b in buttons.sprites():
        b.drawText()
    pygame.display.flip()