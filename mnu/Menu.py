import pygame
import Game
import Images

class Menu(object):
    
    def __init__(self, buttons, labels = [], background = False):
        self.mouse_pressed = False
        self.buttons = buttons
        self.labels = labels
        self.background = background
        if background:
            self.background_img = Images.load_imageurl("img/gui/menu_background.png")
    
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
    
    def render_background(self, screen):
        screen.fill(Game.BLUE)
    
    def render(self, screen):
        if self.background:
            screen.blit(self.background_img, (0, 0))
        for button in self.buttons:
            button.render(screen)
        for label in self.labels:
            label.render(screen)
    
    def type(self, char):
        pass
    
    def delete(self):
        pass

class Label(object):
    
    WIDTH = 128 * Game.SCALE
    SMALL_WIDTH = 72 * Game.SCALE
    HEIGHT = 32 * Game.SCALE
    Y_OFFSET = 2 * Game.SCALE
    
    def __init__(self, text, pos, small = False):
        self.text = text
        self.pos = pos
        if small:
            imgurl = "img/gui/label_small.png"
        else:
            imgurl = "img/gui/label.png"
        self.img = Images.load_imageurl(imgurl)
        self.font = Game.get_font()
    
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.img.get_width(), Label.HEIGHT)
    
    def render(self, screen):
        screen.blit(self.img, self.pos)
        color = Game.LIGHT_GRAY
        
        text_img = self.font.render(self.text, 0, color)
        x = self.get_rect().centerx - text_img.get_width() / 2
        y = self.get_rect().centery - text_img.get_height() / 2 + Label.Y_OFFSET
        screen.blit(text_img, (x, y))