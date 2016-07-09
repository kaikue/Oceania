import pygame
import Game

class GUI(object):
    SCALING = 48
    
    def __init__(self, imageurl):
        self.imageurl = imageurl
        self.img = self.load_imageurl(imageurl)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
    
    def load_imageurl(self, imageurl):
        if imageurl is "":
            return None
        img = pygame.image.load(imageurl).convert_alpha()
        return pygame.transform.scale(img, (Game.SCALE * img.get_width(), Game.SCALE * img.get_height()))
    
    def render(self, screen):
        left = (Game.SCREEN_WIDTH - self.width) // 2
        top = (Game.SCREEN_HEIGHT - self.height) // 2
        screen.blit(self.img, (left, top))
    
    def load_extra_image(self, imageurl):
        extra_img = pygame.image.load(imageurl).convert_alpha()
        return pygame.transform.scale(extra_img, (Game.SCALE * extra_img.get_width(), Game.SCALE * extra_img.get_height()))