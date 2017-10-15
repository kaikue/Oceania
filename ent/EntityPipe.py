import Game
import Entity

class EntityPipe(Entity.Entity):
    def __init__(self, pos, chunk, background=False):
        super().__init__(pos, "", background)
    
    def render(self, screen, pos):
        #this is temporary, until I fix the structure generation
        txt = Game.get_font().render("*", 0, Game.WHITE)
        screen.blit(txt, pos)
    
    #TODO: update, hold item and transfer it- how?