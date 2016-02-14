import Game
import Entity

class EntityChest(Entity.Entity):
    def interact(self, item):
        print("Nice meme!")
    
    def render(self, screen, pos):
        txt = Game.font.render("this is a chest", 0, Game.WHITE)
        screen.blit(txt, pos)