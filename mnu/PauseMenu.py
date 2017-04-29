import Game
from mnu.Menu import Menu
import Button

class PauseMenu(Menu):
    def __init__(self):
        resume_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 1 // 3), "Resume", "resume")
        quit_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 2 // 3), "Quit", "quit")
        super(PauseMenu, self).__init__([resume_button, quit_button])