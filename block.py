import pygame
import game

AIR = 0
WATER = 1
DIRT = 2
STONE = 3

SIZE = 16

class Block(object):
    
    def __init__(self, blockid):
        self.blockid = blockid
    
    def render(self, screen, x, y):
        if self.blockid == AIR:
            #pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y, SIZE, SIZE))
            pass
        elif self.blockid == WATER:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(x, y, SIZE, SIZE))
        elif self.blockid == DIRT:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, SIZE, SIZE))
        if game.DEBUG:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, SIZE, SIZE), 1)