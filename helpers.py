try:
    import sys
    import pygame
    import pygame.font
    import os
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)

def load_img(name):
    '''Load image and return image object'''
    fullname = os.path.join('data\images', name)
    try:
        image = pygame.image.load(fullname)
        if(image.get_alpha is None):
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image: ', message)
        raise SystemExit
    return image, image.get_rect()

def create_text(text, size):
    font = pygame.font.Font(None, size)
    textSurface = font.render(text, True, (10, 10, 10))
    return textSurface, textSurface.get_rect()
