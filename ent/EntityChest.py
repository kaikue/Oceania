import Game
import Entity
import Inventory
from gui.ChestGUI import ChestGUI

class EntityChest(Entity.Entity):
    def __init__(self, pos, background=False):
        self.inventory = Inventory.Inventory(4, 10)
        super().__init__(pos, "", background)
    
    def load_image(self):
        super().load_image()
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
    
    def save(self):
        save_data = super().save()
        inventory_data = self.inventory.save()
        save_data["inventory"] = inventory_data
        return save_data
    
    def load(self, save_data):
        super().load(save_data)
        inventory_data = save_data["inventory"]
        inventory = Inventory.Inventory(0, 0)
        inventory.load(inventory_data)

    #breaks entity pickup
    """def __eq__(self, other):
        if type(other) is type(self):
            return self.items == other.items
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)"""