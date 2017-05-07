import Game
from mnu.Menu import Menu
from mnu.CharacterMenu import CharacterMenu
import Button

class WorldNameMenu(Menu):
    
    def __init__(self, prev_menu):
        
        #TODO: text fields for name and seed
        #name field should be validated- folder characters only, not the same as any existing world
        #don't let the next button work until it is valid
        self.name = "menuworld"
        self.seed = "asdfghjkl"
        
        back_button = Button.Button((Game.SCREEN_WIDTH / 4 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Cancel", "menu")
        back_button.next_menu = prev_menu
        
        next_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Next", "menu")
        next_button.next_menu = CharacterMenu(self)
        
        super(WorldNameMenu, self).__init__([back_button, next_button])