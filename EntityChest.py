import Game
import Entity

class EntityChest(Entity.Entity):
    def interact(self, item):
        #TODO open a chest gui
        pass
    
    def render(self, screen, pos):
        #this is temporary, until I fix the structure generation
        txt = Game.get_font().render("*", 0, Game.WHITE)
        screen.blit(txt, pos)