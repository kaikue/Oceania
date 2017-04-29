import Game
from mnu.Menu import Menu
import Button

class PauseMenu(Menu):
    def __init__(self):
        resume_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 1 // 3), "Resume", "resume")
        options_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 1 // 2), "Options", "options")
        quit_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 2 // 3), "Quit", "quit")
        super(PauseMenu, self).__init__([resume_button, options_button, quit_button])