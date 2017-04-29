import Game
import Button

BACKGROUND = (64, 64, 255)

class Menu(object):
    
    def __init__(self, buttons):
        self.mouse_pressed = False
        self.buttons = buttons
    
    def mouse_press(self):
        for button in self.buttons:
            if button.mouse_hover():
                button.pressed = True
        self.mouse_pressed = True
    
    def mouse_hold(self):
        for button in self.buttons:
            if button.pressed and not button.mouse_hover():
                button.pressed = False
    
    def mouse_release(self):
        for button in self.buttons:
            if button.pressed and button.mouse_hover():
                button.activate()
        self.mouse_pressed = False
    
    def update(self):
        if self.mouse_pressed:
            self.mouse_hold()
    
    def render(self, screen):
        screen.fill(BACKGROUND)
        for button in self.buttons:
            button.render(screen)

def main_menu():
    play_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 2 // 3), "Start Game", "play")
    return Menu([play_button])

def pause_menu():
    resume_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 1 // 3), "Resume", "resume")
    quit_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 2 // 3), "Quit", "quit")
    return Menu([resume_button, quit_button])