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
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.text, self.textRect = create_text(text, size)
        self.textRect.center = ((self.rect[0] + self.rect[2]/2), (self.rect[1] + self.rect[3]/2))

    def drawText(self, surface):
        surface.blit(self.text, self.textRect)

    def onClick(self):
        print('Click')

class DigitButton(Button):
    def __init__(self, pos, text, value, size=36):
        Button.__init__(self, pos, text, size)
        self.value = value

    def onClick(self):
        print(self.value)

class RenderButton(pygame.sprite.RenderPlain):
    def __init__(self, *sprites):
        pygame.sprite.RenderPlain.__init__(self, sprites)

    def draw(self, surface):
        ret = pygame.sprite.RenderPlain.draw(self, surface)
        for b in self.sprites():
            b.drawText(surface)