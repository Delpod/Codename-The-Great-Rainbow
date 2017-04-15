try:
    import sys
    import random
    import math
    import os
    import pygame
    import helpers
    import buttons
    import textField
    import drawRect
    from pygame.locals import *
    from helpers import *
    from buttons import Button, DigitButton, ItemButton, RenderButton
    from textField import TextField
    from drawRect import DrawRect
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)

global screensize
screensize = (1280, 720)

def setValue(value, textfield):
    textfield.setText(str(int(textfield.getString()) * 10 + value))

def backspace(textfield):
    textfield.setText(str(int(int(textfield.getString()) / 10)))

def clear(textfield):
    textfield.setText('0')

def unveilWeigh(itemButton):
    itemButton.sprites()[0].unveilWeigh()

def initButtons(textfield, itembutton):
    buttons = []
    buttonArgs = []
    start = [848, 360]

    for i in range(3):
        for j in range(3):
            val = 1 + j + 3 * i
            buttons.append(DigitButton((start[0] + 80 * j, start[1] - 80 * i), chr(48 + val), val, function=setValue))
            buttonArgs.append(textfield)

    buttons.append(Button((start[0], start[1] + 80), 'Cls', 30, function=clear))
    buttonArgs.append(textfield)
    buttons.append(DigitButton((start[0] + 1 * 80, start[1] + 80), chr(48), 0, function=setValue))
    buttonArgs.append(textfield)
    buttons.append(Button((start[0] + 2 * 80, start[1] + 80), 'Bcksp', 20, function=backspace))
    buttonArgs.append(textfield)
    buttons.append(Button((start[0], start[1] + 2 * 80), 'Weigh', 40, 'longbutton.png', function=unveilWeigh))
    buttonArgs.append(itembutton)

    return pygame.sprite.RenderPlain(buttons), buttonArgs

def generateItem(itembutton):
    x = random.randint(0, screensize[0] / 2 - 150)
    y = random.randint(0, screensize[1] - 100)
    quantity = 1
    weigh = random.randint(0, 100) > 50
    if (weigh):
        quantity = random.randint(5, 200) / 100
    else:
        many = random.randint(0, 100) > 50
        if (many):
            quantity = random.randint(2, 50)

    itembutton.add((ItemButton((x, y), 'Pen', quantity, weigh)))


pygame.init()
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption('The Great Rainbow')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

otherUi = pygame.sprite.RenderPlain((DrawRect((0, 0, 0), (screensize[0] / 2 - 1, 0), (2, screensize[1]))))
textField = TextField((848, 120), (224, 64), 64, (190, 220, 165), (60, 85, 35))
itembutton = RenderButton(())
buttons, buttonArgs = initButtons(textField, itembutton)
buttons = RenderButton(buttons)

screen.blit(background, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if(event.type == QUIT):
            sys.exit(2)
        elif(event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
            for i in range(len(buttons.sprites())):
                if(buttons.sprites()[i].checkClick(pygame.mouse.get_pos(), buttonArgs[i])):
                    break
            else:
                item = itembutton.sprites()[0]
                if(item.toWeigh and item.weighed and item.checkClick(pygame.mouse.get_pos())):
                    screen.blit(background, item.rect)
                    itembutton.empty()

    if(len(itembutton.sprites()) == 0):
        generateItem(itembutton)

    buttons.draw(screen)
    textField.draw(screen)
    itembutton.draw(screen)
    otherUi.draw(screen)
    pygame.display.flip()