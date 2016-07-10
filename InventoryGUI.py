import pygame
import Game
import GUI

class InventoryGUI(GUI.GUI):
    
    def __init__(self, player, imageurl):
        super(InventoryGUI, self).__init__(imageurl)
        self.player = player
        self.left = (Game.SCREEN_WIDTH - self.width) // 2
        self.top = (Game.SCREEN_HEIGHT - self.height) // 2
        self.moving_item = None
    
    def render(self, screen):
        super(InventoryGUI, self).render(screen)
        self.player.inventory.render(self.left, self.top, screen, True, self.moving_item)
        
        if self.moving_item is not None:
            #screen.blit(self.moving_item.img, )
            self.moving_item.render(pygame.mouse.get_pos(), screen)
    
    def click(self, pos):
        slot = self.player.inventory.slot_at(pos, self.left, self.top, True)
        if slot is not None:
            self.player.inventory[slot[0]][slot[1]], self.moving_item = self.moving_item, self.player.inventory[slot[0]][slot[1]]
    
    def close(self):
        self.moving_item = None