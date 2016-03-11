import pygame
from ItemStack import ItemStack


class ToolMagicStaff(ItemStack):
    
    def __init__(self, itemname, imageurl):
        img = pygame.image.load(imageurl).convert_alpha()
        ItemStack.__init__(self, itemname, img, False, stackable = False, itemdata = None)
    
    def use(self, mouse_pos):
        #create a bolt of energy facing towards direction
        print("using the staff")