import World
import Game
from GUI import GUI
import pygame

class InventoryGUI(GUI):
    
    def __init__(self, player):
        self.player = player
    
    def render(self, screen):
        left = (Game.SCREEN_WIDTH - 192) / 2
        top = (Game.SCREEN_HEIGHT - 192) / 2
        pygame.draw.rect(screen, Game.BLACK, pygame.Rect(left, top, 192, 192), 0)
        inventory = self.player.inventory
        for r in range(len(inventory)):
            for c in range(len(inventory[r])):
                inv_item = inventory[r][c]
                if inv_item is not None:
                    #c and r are flipped here so it renders across then down
                    screen.blit(World.block_images[False][World.get_block_id(inv_item.itemtype)], (left + c * 32, top + r * 32))
                    countimg = Game.get_font().render(str(inv_item.count), 0, Game.WHITE)
                    screen.blit(countimg, (left + c * 32, top + r * 32))
                #TODO make it work for items too