import pygame
import Game
from mnu.Menu import Menu
import Button
import Images

BG_COLOR = (62, 121, 221)

class MainMenu(Menu):
    def __init__(self):
        play_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 2 // 3), "Start Game", "play")
        self.back_image = Images.load_imageurl("img/title/back.png")
        self.back_width = self.back_image.get_width()
        self.bg_y = Game.SCREEN_HEIGHT - self.back_image.get_height()
        self.mid_image = Images.load_imageurl("img/title/mid.png")
        self.mid_width = self.mid_image.get_width()
        self.front_image = Images.load_imageurl("img/title/front.png")
        self.front_width = self.front_image.get_width()
        
        self.back_xs = [-self.back_width, 0, self.back_width]
        self.mid_xs = [-self.mid_width, 0, self.mid_width]
        self.front_xs = [-self.front_width, 0, self.front_width]
        
        super(MainMenu, self).__init__([play_button])
    
    def update_x(self, xs, i, increment, width):
        xs[i] += increment
        if xs[i] > Game.SCREEN_WIDTH:
            xs[i] = xs[(i + 1) % 3] - width + increment
    
    def update(self):
        for i in range(3):
            self.update_x(self.back_xs, i, 0.25, self.back_width)
            self.update_x(self.mid_xs, i, 0.5, self.mid_width)
            self.update_x(self.front_xs, i, 0.75, self.front_width)
        Menu.update(self)
    
    def calculate_x(self, multiplier):
        return (self.time * multiplier) % Game.SCREEN_WIDTH
    
    def render(self, screen):
        screen.fill(Game.BLACK)
        pygame.draw.rect(screen, BG_COLOR, pygame.rect.Rect(0, 0, Game.SCREEN_WIDTH, self.bg_y))
        for back_x in self.back_xs:
            screen.blit(self.back_image, (back_x, self.bg_y))
        for mid_x in self.mid_xs:
            screen.blit(self.mid_image, (mid_x, self.bg_y))
        for front_x in self.front_xs:
            screen.blit(self.front_image, (front_x, self.bg_y))
        Menu.render(self, screen)