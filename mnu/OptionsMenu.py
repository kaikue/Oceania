import Game
from mnu.Menu import Menu
import Button

class OptionsMenu(Menu):
    def __init__(self, prev_menu):
        music_message = Button.music_message(Game.is_music_enabled())
        self.music_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 1 // 2), music_message, "music")
        back_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Back", "back")
        back_button.prev_menu = prev_menu
        super(OptionsMenu, self).__init__([self.music_button, back_button])