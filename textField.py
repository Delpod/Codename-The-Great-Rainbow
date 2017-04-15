try:
    import sys
    import pygame
    import helpers
    import drawRect
    from pygame.locals import *
    from drawRect import DrawRect
    from helpers import create_text
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)


class TextField(pygame.sprite.RenderPlain):
    def __init__(self, pos, size, innerColor=(255, 255, 255), outerColor=(0, 0, 0)):
        self.outer = DrawRect(outerColor, pos, size)
        self.inner = DrawRect(innerColor, [x + 2 for x in pos], [x - 4 for x in size])
        self.setText('0')
        pygame.sprite.RenderPlain.__init__(self, (self.outer, self.inner))

    def drawText(self, surface):
        surface.blit(self.text, self.textRect)

    def draw(self, surface):
        pygame.sprite.RenderPlain.draw(self, surface)
        self.drawText(surface)

    def setText(self, text):
        self.text, self.textRect = create_text(text, 60)
        self.textRect[0] = self.outer.rect[0] + 10
        self.textRect[1] = self.outer.rect[1] + (self.outer.rect[3] - self.textRect[3] * 0.8) / 2