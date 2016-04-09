import pygame
import Game

MAX_STACK_SIZE = 100

class ItemStack(object):
    
    def __init__(self, itemname, imageurl, can_place, stackable = True, itemdata = None):
        self.itemname = itemname
        img = pygame.image.load(imageurl).convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * Game.SCALE, img.get_height() * Game.SCALE))
        self.img = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA, 32).convert_alpha()
        self.img.blit(img, (0, 0))
        self.can_place = can_place
        self.count = 1
        self.stackable = stackable
        self.itemdata = itemdata
    
    def can_stack(self, itemstack):
        return self.count < MAX_STACK_SIZE and \
            itemstack.itemtype == self.itemname and \
            self.stackable and \
            itemstack.itemdata == self.itemdata
    
    def get_break_speed(self):
        return 1
    
    def get_harvest_level(self):
        return 0
    
    def use_continuous(self, world, player, mouse_pos, viewport):
        pass
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        pass
    
    def __str__(self):
        return str(self.count) + "x " + self.itemname