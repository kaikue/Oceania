import pygame
import Game
import Images

WIDTH = 96 * Game.SCALE
HEIGHT = 32 * Game.SCALE

class Button(object):
    
    def __init__(self, pos, text, effect):
        self.pos = pos
        self.text = text
        self.effect = effect
        self.pressed = False
        self.font = Game.get_font()
        self.unpressed_image = Images.load_imageurl("img/gui/button_up.png")
        self.hovered_image = Images.load_imageurl("img/gui/button_hover.png")
        self.pressed_image = Images.load_imageurl("img/gui/button_down.png")
    
    def activate(self):
        if self.effect == "play":
            Game.play()
        elif self.effect == "resume":
            Game.unpause()
        elif self.effect == "quit":
            Game.close()
    
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], WIDTH, HEIGHT)
    
    def mouse_hover(self):
        return self.get_rect().collidepoint(pygame.mouse.get_pos())
    
    def render(self, screen):
        color = Game.LIGHT_GRAY
        if self.mouse_hover():
            if self.pressed:
                img = self.pressed_image
                color = Game.MEDIUM_GRAY
            else:
                img = self.hovered_image
        else:
            img = self.unpressed_image
        screen.blit(img, self.pos)
        text_img = self.font.render(self.text, 0, color)
        h = text_img.get_height() - (2 * Game.SCALE)
        w = text_img.get_width()
        screen.blit(text_img, (self.pos[0] + (WIDTH - w) / 2, self.pos[1] + (HEIGHT - h) / 2))