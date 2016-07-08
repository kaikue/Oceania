import pygame
import Game
from GUI import GUI

class InventoryGUI(GUI):
    
    def __init__(self, player, imageurl):
        self.player = player
        super(InventoryGUI, self).__init__(imageurl)
    
    def render(self, screen):
        super(InventoryGUI, self).render(screen)
        
        left = (Game.SCREEN_WIDTH - self.width) // 2
        top = (Game.SCREEN_HEIGHT - self.height) // 2
        
        tooltip_item = None
        inventory = self.player.inventory
        for r in range(len(inventory)):
            for c in range(len(inventory[r])):
                inv_item = inventory[r][c]
                if inv_item is not None:
                    #c and r are flipped here so it renders across then down
                    drawX = GUI.SCALING * 2 / 3 + left + c * GUI.SCALING
                    drawY = GUI.SCALING * 2 / 3 + top + r * GUI.SCALING
                    if r > 0:
                        drawY += GUI.SCALING / 8
                    screen.blit(inv_item.img, (drawX, drawY))
                    if inv_item.stackable:
                        countimg = Game.get_font().render(str(inv_item.count), 0, Game.WHITE)
                        screen.blit(countimg, (drawX, drawY))
                    rect = inv_item.img.get_rect().move(drawX, drawY)
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        tooltip_item = inv_item
        #TODO draw armor
        
        if tooltip_item is not None:
            print(tooltip_item.itemname)