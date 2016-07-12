import pygame
import Game
import World
import gui.GUI as GUI
import Images
import importlib


MAX_STACK_SIZE = 10

def itemstack_from_name(itemname):
    item = World.items[itemname]
    item_class = getattr(importlib.import_module(item["class"]), item["class"])
    return item_class(itemname)

class ItemStack(object):
    
    def __init__(self, name, stackable = True, data = None, count = 1):
        self.name = name
        self.imageurl = World.items[name]["image"]
        self.load_image()
        self.can_place = World.items[name]["can_place"]
        self.count = count
        self.stackable = stackable
        self.data = data
    
    def load_image(self):
        img = Images.load_imageurl(self.imageurl)
        self.img = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA, 32).convert_alpha()
        self.img.blit(img, (0, 0))
    
    def can_stack(self, itemstack):
        return itemstack is not None and \
            itemstack.count + self.count <= MAX_STACK_SIZE and \
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
    
    def render(self, pos, screen):
        screen.blit(self.img, (pos[0] + GUI.SCALING / 6, pos[1] + GUI.SCALING / 6))
        if self.stackable:
            countimg = Game.get_font().render(str(self.count), 0, Game.WHITE)
            screen.blit(countimg, (pos[0] + 3 * Game.SCALE, pos[1] + 3 * Game.SCALE))
    
    def __str__(self):
        return str(self.count) + "x " + self.name