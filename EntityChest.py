import Game
import Entity
import Inventory
from gui.ChestGUI import ChestGUI

class EntityChest(Entity.Entity):
    def __init__(self, pos, imageurl, background=False):
        self.inventory = Inventory.Inventory(4, 10)
        super(EntityChest, self).__init__(pos, imageurl, background)
    
    def load_image(self):
        super(EntityChest, self).load_image()
        for row in self.inventory:
            for item in row:
                if item is not None:
                    item.load_image()
    
    def interact(self, player, item):
        Game.set_gui(ChestGUI(self.inventory, player, "img/gui/chest.png"))
        return True
    
    def render(self, screen, pos):
        #this is temporary, until I fix the structure generation
        txt = Game.get_font().render("*", 0, Game.WHITE)
        screen.blit(txt, pos)