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
        self.text, self.textRect = create_text(text, size)
        self.textRect.center = ((self.rect[0] + self.rect[2]/2), (self.rect[1] + self.rect[3]/2))

    def drawText(self, surface):
        surface.blit(self.text, self.textRect)


class ItemButton(Button):
    def __init__(self, pos, itemName, quantity=1, toWeigh=False, function=None):
        size = min(int(325 / len(itemName)), 75)
        Button.__init__(self, pos, itemName, size, 'item.png', function=function)
        self.textRect[1] -= 10
        self.toWeigh = toWeigh
        self.quantity = round(quantity, 2) if toWeigh else int(quantity)
        text = '??.?? kg' if toWeigh else 'x ' + str(self.quantity)
        self.text2, self.textRect2 = create_text(text, 30)
        self.textRect2.center = ((self.rect[0] + self.rect[2] / 2), (self.rect[1] + self.rect[3] / 2) + 30)
        self.unveilWeigh()

    def drawText(self, surface):
        Button.drawText(self, surface)
        surface.blit(self.text2, self.textRect2)

    def unveilWeigh(self):
        if(self.toWeigh):
            text = str(float(self.quantity)) + ' kg'
            self.text2, self.textRect2 = create_text(text, 30)
            self.textRect2.center = ((self.rect[0] + self.rect[2] / 2), (self.rect[1] + self.rect[3] / 2) + 30)

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