import pygame
import Game
import World
import importlib


MAX_STACK_SIZE = 100

def itemstack_from_name(itemname):
    item = World.items[itemname]
    item_class = getattr(importlib.import_module(item["class"]), item["class"])
    return item_class(itemname)

class ItemStack(object):
    
    def __init__(self, name, stackable = True, data = None):
        self.name = name
        imageurl = World.items[name]["image"]
        img = pygame.image.load(imageurl).convert_alpha()
        img = pygame.transform.scale(img, (img.get_width() * Game.SCALE, img.get_height() * Game.SCALE))
        self.img = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA, 32).convert_alpha()
        self.img.blit(img, (0, 0))
        self.can_place = World.items[name]["can_place"]
        self.count = 1
        self.stackable = stackable
        self.data = data
    
    def can_stack(self, itemstack):
        return self.count < MAX_STACK_SIZE and \
            itemstack.name == self.name and \
            self.stackable and \
            itemstack.data == self.data
    
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