try:
    import sys
    import pygame
    from pygame.locals import *
except ImportError as err:
    print('couldn\'t load module. %s' % err)
    sys.exit(1)

class DrawRect(pygame.sprite.Sprite):
    def __init__(self, color, pos, size):
        pygame.sprite.Sprite.__init__(self)
        surface = pygame.Surface(size)
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        surface.fill(color, (0, 0, size[0], size[1]))
        self.image = surface.convert()