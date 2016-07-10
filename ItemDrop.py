import pygame
import Game
from Entity import Entity

class ItemDrop(Entity):
    
    def __init__(self, pos, name, imageurl, data = None):
        #center the position in the block
        pos = [pos[0] + 0.25, pos[1] + 0.25]
        super(ItemDrop, self).__init__(pos, imageurl)
        self.name = name
        self.data = data
    
    def load_image(self):
        blockimg = pygame.image.load(self.imageurl).convert_alpha()
        #make the image pixelated to fit in better
        img = pygame.Surface((Game.BLOCK_SIZE, Game.BLOCK_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        img.blit(blockimg, (0, 0))
        img = pygame.transform.scale(img, (Game.BLOCK_SIZE // Game.SCALE, Game.BLOCK_SIZE // Game.SCALE))
        self.img = pygame.transform.scale(img, (Game.BLOCK_SIZE, Game.BLOCK_SIZE))