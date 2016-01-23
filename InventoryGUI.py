import World
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
                    screen.blit(World.block_images[False][World.get_block_id(inv_item.itemtype)], (drawX, drawY))
                    countimg = Game.get_font().render(str(inv_item.count), 0, Game.WHITE)
                    screen.blit(countimg, (drawX, drawY))
                #TODO make it work for items too
        #TODO draw armor