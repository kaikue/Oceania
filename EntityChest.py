import Game
import Entity
import Inventory

class EntityChest(Entity.Entity):
    def __init__(self, pos, imageurl, background=False):
        super(EntityChest, self).__init__(pos, imageurl, background)
        self.inventory = Inventory.Inventory(4, 10)
    
    def interact(self, item):
        #TODO open a chest gui
        pass
    
    def render(self, screen, pos):
        #this is temporary, until I fix the structure generation
        txt = Game.get_font().render("*", 0, Game.WHITE)
        screen.blit(txt, pos)