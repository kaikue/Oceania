import pygame
from ItemStack import ItemStack


class ToolPickaxe(ItemStack):
    
    def __init__(self, itemname, imageurl):
        img = pygame.image.load(imageurl).convert_alpha()
        ItemStack.__init__(self, itemname, img, False, stackable = False, itemdata = None)
    
    def get_break_speed(self):
        return 2
    
    def get_harvest_level(self):
        return 1