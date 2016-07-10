import Game
import GUI

class InventoryGUI(GUI.GUI):
    
    def __init__(self, player, imageurl):
        super(InventoryGUI, self).__init__(imageurl)
        self.player = player
    
    def render(self, screen):
        super(InventoryGUI, self).render(screen)
        
        left = (Game.SCREEN_WIDTH - self.width) // 2
        top = (Game.SCREEN_HEIGHT - self.height) // 2
        
        self.player.inventory.render(left, top, screen, True)