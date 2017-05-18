try:
    import sys
    import pygame
    import pygame.font
    import helpers
    import textField
    from pygame.locals import *
    from helpers import *
    from textField import *
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)


class Clickable(pygame.sprite.Sprite):
    def __init__(self, function=None):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect((0, 0, 0, 0))
        self.function = function

    def checkClick(self, mousePos, *kwargs):
        if self.rect.collidepoint(mousePos[0], mousePos[1]):
            self.onClick(*kwargs)
            return True
        else:
            return False

    def onClick(self, *kwargs):
        if self.function is not None:
            self.function(*kwargs)

    def getRectCenter(self, rect, xshift=0, yshift=0):
        return (rect[0] + rect[2] / 2 + xshift), (rect[1] + rect[3] / 2 + yshift)


class TextFieldButton(TextField, Clickable):
    def __init__(self, pos, size, textSize, text, innerColor=(250, 250, 250), outerColor=(10, 10, 10), function=None):
        Clickable.__init__(self, function)
        TextField.__init__(self, pos, size, textSize, innerColor, outerColor, text)
        self.rect = self.outer.rect

    def setText(self, text):
        self.string = text
        self.text, self.textRect = create_text(text, self.textSize)
        self.textRect.center = self.getRectCenter(self.outer.rect)

class Button(Clickable):
    def __init__(self, pos, text, size=36, name='button.png', function=None):
        Clickable.__init__(self, function)

        try:
            self.image, self.rect = load_img(name)
        except SystemExit:
            sys.exit(1)

        self.rect[0], self.rect[1] = pos[0], pos[1]
        self.text, self.textRect = create_text(text, size)
        self.textRect.center = self.getRectCenter(self.rect)

    def drawText(self, surface):
        surface.blit(self.text, self.textRect)


class ItemButton(Button):
    def __init__(self, pos, itemName, quantity=1, toWeigh=False, function=None):
        size = min(int(340 / len(itemName)), 70)
        Button.__init__(self, pos, itemName, size, 'item.png', function=function)
        self.textRect[1] = self.rect[1] + self.textRect[3] / 5
        self.toWeigh = toWeigh

        if self.toWeigh:
            self.quantity = round(quantity, 2)
            self.weighed = False
        else:
            self.quantity = int(quantity)
            self.weighed = True

        text = '?.?? kg' if toWeigh else 'x ' + str(self.quantity)
        self.text2, self.textRect2 = create_text(text, 30)
        self.textRect2.center = self.getRectCenter(self.rect, yshift=30)
        self.failure = False

    def drawText(self, surface):
        Button.drawText(self, surface)
        surface.blit(self.text2, self.textRect2)

    def unveilWeigh(self):
        if self.toWeigh:
            text = str(float(self.quantity)) + ' kg'
            self.text2, self.textRect2 = create_text(text, 30)
            self.textRect2.center = self.getRectCenter(self.rect, yshift=30)
            self.weighed = True
        else:
            self.failure = True

    def setQuantity(self, quantity):
        if quantity < 0:
            self.failure = True
        self.quantity = quantity
        self.text2, self.textRect2 = create_text('x ' + str(quantity), 30)
        self.textRect2.center = self.getRectCenter(self.rect, yshift=30)

    def onClick(self, *kwargs):
        if self.toWeigh:
            if not self.weighed or kwargs[0] > 1:
                self.failure = True
        else:
            Button.onClick(self)


class DigitButton(Button):
    def __init__(self, pos, text, value, size=36, function=None):
        Button.__init__(self, pos, text, size, function=function)
        self.value = value

    def onClick(self, *kwargs):
        Button.onClick(self, self.value, *kwargs)


class RenderButton(pygame.sprite.RenderPlain):
    def draw(self, surface):
        pygame.sprite.RenderPlain.draw(self, surface)
        for b in self.sprites():
            b.drawText(surface)
