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
        for button in self.buttons:
            button.render(screen)