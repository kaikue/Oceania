import pygame
import Game

AIR = 0
WATER = 1
DIRT = 2
STONE = 3

SOLID_BLOCKS = (DIRT, STONE)

SIZE = 32

def load_images():
    global images
    images = {}
    #could probably be improved
    images[WATER] = pygame.image.load("img/water.png").convert_alpha()
    images[WATER] = pygame.transform.scale(images[WATER], (SIZE, SIZE))
    images[DIRT] = pygame.image.load("img/dirt.png").convert_alpha()
    images[DIRT] = pygame.transform.scale(images[DIRT], (SIZE, SIZE))

class Block(object):
    
    def __init__(self, blockid):
        self.blockid = blockid
    
    def is_solid(self):
        return self.blockid in SOLID_BLOCKS
    
    def render(self, screen, pos):
        if self.blockid == AIR:
            #pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x, y, SIZE, SIZE))
            pass
        #elif self.blockid == WATER:
        #    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(pos[0], pos[1], SIZE, SIZE))
        #elif self.blockid == DIRT:
        #    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(pos[0], pos[1], SIZE, SIZE))
        else:
            global images
            screen.blit(images[self.blockid], pos)
        #draw bounding boxes
        if Game.DEBUG:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pos[0], pos[1], SIZE, SIZE), 1)
