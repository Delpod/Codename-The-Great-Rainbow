try:
    import sys
    import random
    import math
    import os
    import pygame
    import helpers
    import button
    import textField
    import drawRect
    import items
    from pygame.locals import *
    from helpers import *
    from items import *
    from button import Button, DigitButton, ItemButton, TextFieldButton, RenderButton
    from textField import TextField
    from drawRect import DrawRect
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)

global screensize
screensize = (1280, 720)

def setValue(value, textfield):
    textfield.setText(str(int(textfield.string) * 10 + value))

def backspace(textfield):
    textfield.setText(str(int(int(textfield.string) / 10)))

def clear(textfield):
    textfield.setText('0')

def unveilWeigh(itemButton):
    itemButton.sprites()[0].unveilWeigh()

def initButtons(textfield, itembutton):
    buttonList = []
    buttonArgs = []
    start = [848, 360]

    nextClientButton = TextFieldButton((50, screensize[1] - 150), (screensize[0] / 2 - 100, 100), 100, 'Next Client')

    gameOverAlert = TextFieldButton((200, screensize[1] / 2 - 200), (screensize[0] - 400, 400), 200, 'Game Over')
    gameOverButton = TextFieldButton((screensize[0] / 2 - 300, screensize[1] / 2 + 100), (200, 64), 50, 'Try again')
    gameOverExit = TextFieldButton((screensize[0] / 2 + 100, screensize[1] / 2 + 100), (200, 64), 50, 'Exit')

    for i in range(3):
        for j in range(3):
            val = 1 + j + 3 * i
            buttonList.append(DigitButton((start[0] + 80 * j, start[1] - 80 * i), chr(48 + val), val, function=setValue))
            buttonArgs.append(textfield)

    buttonList.append(Button((start[0], start[1] + 80), 'Cls', 30, function=clear))
    buttonArgs.append(textfield)
    buttonList.append(DigitButton((start[0] + 1 * 80, start[1] + 80), chr(48), 0, function=setValue))
    buttonArgs.append(textfield)
    buttonList.append(Button((start[0] + 2 * 80, start[1] + 80), 'Bcksp', 20, function=backspace))
    buttonArgs.append(textfield)
    buttonList.append(Button((start[0], start[1] + 2 * 80), 'Weigh', 40, 'longbutton.png', function=unveilWeigh))
    buttonArgs.append(itembutton)

    return nextClientButton, (gameOverAlert, gameOverButton, gameOverExit), RenderButton(buttonList), buttonArgs

def generateItem(itembutton):
    x = random.randint(0, screensize[0] / 2 - 150)
    y = random.randint(0, screensize[1] - 100)
    quantity = 1
    weigh = random.randint(0, 100) > 50
    itemName = weighItems[random.randint(0, len(weighItems) - 1)] if weigh else pieceItems[random.randint(0, len(pieceItems) - 1)]

    if (weigh):
        quantity = random.randint(5, 200) / 100
    else:
        many = random.randint(0, 100) > 50
        if(many):
            quantity = random.triangular(2, 50, 2)

    itembutton.add((ItemButton((x, y), itemName, quantity, weigh)))

pygame.init()
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption('The Great Rainbow')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

otherUi = pygame.sprite.RenderPlain((DrawRect((0, 0, 0), (screensize[0] / 2, 0), (2, screensize[1]))))
textfield = TextField((848, 120), (224, 64), 64, (190, 220, 165), (60, 85, 35))
itembutton = RenderButton(())
nextClientButton, gameOverScreen, buttons, buttonArgs = initButtons(textfield, itembutton)

screen.blit(background, (0, 0))
pygame.display.flip()

numberOfItems = 0
numberOfItemsDone = 0
numberOfGoods = 0

clock = pygame.time.Clock()

state = 'START'
endticks = 0
startticks = pygame.time.get_ticks()
print(startticks)
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if(event.type == QUIT):
            sys.exit(2)
        elif(event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
            if(state == 'GAME'):
                for i in range(len(buttons.sprites())):
                    if(buttons.sprites()[i].checkClick(pygame.mouse.get_pos(), buttonArgs[i])):
                        break
                else:
                    item = itembutton.sprites()[0]
                    if(item.weighed and item.checkClick(pygame.mouse.get_pos())):
                        if(item.toWeigh):
                            screen.blit(background, item.rect)
                            numberOfGoods += 1
                            numberOfItemsDone += 1
                            itembutton.empty()
                        else:
                            q = int(textfield.string)
                            item.setQuantity(item.quantity - q)
                            clear(textfield)
                            if(item.quantity <= 0):
                                screen.blit(background, item.rect)
                                numberOfGoods += q
                                numberOfItemsDone += 1
                                itembutton.empty()
                                if(item.quantity < 0):
                                    endticks = pygame.time.get_ticks()
                                    state = 'GAMEOVER'
                                    print((endticks-startticks)/1000)
            elif(state == 'START'):
                if(nextClientButton.checkClick(pygame.mouse.get_pos())):
                    numberOfItems = random.randint(1, 5)
                    screen.blit(background, nextClientButton.rect)
                    state = 'GAME'
            elif(state == 'GAMEOVER'):
                for i in range(1, len(gameOverScreen)):
                    if(gameOverScreen[i].checkClick(pygame.mouse.get_pos())):
                        if(i == 1):
                            screen.blit(background, gameOverScreen[0].rect)
                            state = 'START'
                        elif(i == 2):
                            sys.exit(0)

    buttons.draw(screen)
    textfield.draw(screen)
    otherUi.draw(screen)

    if (state == 'GAME'):
        if (len(itembutton.sprites()) == 0 and numberOfItemsDone < numberOfItems):
            generateItem(itembutton)
        elif (numberOfItemsDone >= numberOfItems):
            state = 'START'
            numberOfItems = 0
            numberOfItemsDone = 0
            numberOfGoods = 0
        itembutton.draw(screen)
    elif(state == 'START'):
        nextClientButton.draw(screen)
    elif(state == 'GAMEOVER'):
        for g in gameOverScreen:
            g.draw(screen)

    pygame.display.flip()