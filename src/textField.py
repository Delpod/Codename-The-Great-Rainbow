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
    def __init__(self, pos, size, textSize, innerColor=(250, 250, 250), outerColor=(10, 10, 10), text='1', maxLength=-1):
        if maxLength == -1:
            self.maxLength = int(size[0] / 30)
        else:
            self.maxLength = maxLength

        self.outer = DrawRect(outerColor, pos, size)
        self.inner = DrawRect(innerColor, [x + 2 for x in pos], [x - 4 for x in size])
        self.textSize = textSize
        self.setText(text)
        pygame.sprite.RenderPlain.__init__(self, (self.outer, self.inner))

    def drawText(self, surface):
        surface.blit(self.text, self.textRect)

    def draw(self, surface):
        pygame.sprite.RenderPlain.draw(self, surface)
        self.drawText(surface)

    def setText(self, text):
        if len(text) <= self.maxLength:
            self.string = text
            self.text, self.textRect = create_text(text, self.textSize)
            self.textRect[0] = self.outer.rect[0] + self.outer.rect[2] - self.textRect[2] - 10
            self.textRect[1] = self.outer.rect[1] + (self.outer.rect[3] - self.textRect[3] * 0.8) / 2
            self.firstclick = True

    def addText(self, text):
        if self.firstclick:
            self.setText(text)
            self.firstclick = False
        elif len(text) + len(self.string) <= self.maxLength:
            self.setText(self.string + text)
            self.firstclick = False
