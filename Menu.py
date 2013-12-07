import Game
import Button

BACKGROUND = (64, 64, 255)

class Menu(object):
    
    def __init__(self):
        self.mouse_pressed = False
        self.set("main")
    
    def set(self, mode):
        self.mode = mode
        self.create_buttons()
    
    def create_buttons(self):
        if self.mode == "main":
            play_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 2 // 3), "Start Game", "play")
            self.buttons = [play_button]
        elif self.mode == "options":
            self.buttons = []
        #add code here
    
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

if __name__ == "__main__":
    Game.main()