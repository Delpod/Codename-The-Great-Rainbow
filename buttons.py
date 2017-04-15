try:
    import sys
    import pygame
    import pygame.font
    import helpers
    from pygame.locals import *
    from helpers import *
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)

class Clickable(pygame.sprite.Sprite):
    def __init__(self, function=None):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect((0, 0, 0, 0))
        self.function = function

    def checkClick(self, mousePos, *kwargs):
        if(self.rect.collidepoint(mousePos[0], mousePos[1])):
            return True, self.onClick(*kwargs)
        else:
            return False

    def onClick(self, *kwargs):
        if(self.function != None):
            self.function(*kwargs)

class Button(Clickable):
    def __init__(self, pos, text, size=36, name='button.png', function=None):
        Clickable.__init__(self, function)
        self.image, self.rect = load_img(name)
        self.rect[0], self.rect[1] = pos[0], pos[1]
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.text, self.textRect = create_text(text, size)
        self.textRect.center = ((self.rect[0] + self.rect[2]/2), (self.rect[1] + self.rect[3]/2))

    def drawText(self, surface):
        surface.blit(self.text, self.textRect)

class DigitButton(Button):
    def __init__(self, pos, text, value, size=36, function=None):
        Button.__init__(self, pos, text, size, function=function)
        self.value = value

    def onClick(self, *kwargs):
        Button.onClick(self, self.value, *kwargs)

class RenderButton(pygame.sprite.RenderPlain):
    def __init__(self, *sprites):
        pygame.sprite.RenderPlain.__init__(self, sprites)

    def draw(self, surface):
        pygame.sprite.RenderPlain.draw(self, surface)
        for b in self.sprites():
            b.drawText(surface)