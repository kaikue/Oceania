import Game
from mnu.Menu import Menu, Label
from mnu.WorldNameMenu import WorldNameMenu
import Button

LIST_SEPARATION = 4 * Game.SCALE
NUM_WORLDS = 4

class WorldSelectMenu(Menu):
    
    def __init__(self, main_menu):
        self.worlds = Game.get_worlds()
        self.worlds_index = 0
        
        scroll_up_button = Button.Button((Game.SCREEN_WIDTH * 7 // 10 - Button.SMALL_WIDTH / 2, self.get_button_y(1)), "/\\", "scroll_worlds", True)
        scroll_up_button.scroll_amount = -1
        scroll_up_button.world_menu = self
        
        scroll_down_button = Button.Button((Game.SCREEN_WIDTH * 7 // 10 - Button.SMALL_WIDTH / 2, self.get_button_y(2)), "\\/", "scroll_worlds", True)
        scroll_down_button.scroll_amount = 1
        scroll_down_button.world_menu = self
        
        create_world_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "New World", "menu")
        create_world_button.next_menu = WorldNameMenu(self)
        
        back_button = Button.Button((Game.SCREEN_WIDTH / 4 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Back", "menu")
        back_button.next_menu = main_menu
        
        title_label = Label("Select World", (Game.SCREEN_WIDTH / 2 - Label.WIDTH / 2, Game.SCREEN_HEIGHT // 15))
        
        super().__init__([scroll_up_button, scroll_down_button, create_world_button, back_button], [title_label], True)
        
        self.world_buttons = []
        self.display_worlds()
    
    def get_button_y(self, i):
        return Game.SCREEN_HEIGHT // 4 + i * (Button.HEIGHT + LIST_SEPARATION)
    
    def display_worlds(self):
        for old_button in self.world_buttons:
            self.buttons.remove(old_button)
        
        self.world_buttons = []
        for i in range(min(NUM_WORLDS, len(self.worlds) - self.worlds_index)):
            world_i = self.worlds[self.worlds_index + i]
            world_message = world_i
            world_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, self.get_button_y(i)), world_message, "load_world")
            world_button.world_to_load = world_i
            self.world_buttons.append(world_button)
            self.buttons.append(world_button)
    
    def scroll_by(self, amount):
        worlds_end = max(0, len(self.worlds) - NUM_WORLDS)
        self.worlds_index = min(worlds_end, max(0, self.worlds_index + amount))