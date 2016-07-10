import pygame
import Game

SCALING = 48

def render_string_array(strings, font, antialias, color):
    str_images = []
    h = 0
    w = 0
    for string in strings:
        if string is "":
            continue
        str_image = font.render(string, antialias, color)
        str_images.append(str_image)
        w = max(w, str_image.get_width())
        h = h + str_image.get_height()
    surf = pygame.Surface((w, h), pygame.SRCALPHA, 32)
    h = 0
    for str_image in str_images:
        surf.blit(str_image, (0, h))
        h = h + str_image.get_height()
    return surf

class GUI(object):
    
    def __init__(self, imageurl):
        self.imageurl = imageurl
        self.img = self.load_imageurl(imageurl)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.highlightimg = self.load_imageurl("img/gui/highlight.png")
    
    def load_imageurl(self, imageurl):
        if imageurl is "":
            return None
        img = pygame.image.load(imageurl).convert_alpha()
        return pygame.transform.scale(img, (Game.SCALE * img.get_width(), Game.SCALE * img.get_height()))
    
    def render(self, screen):
        left = (Game.SCREEN_WIDTH - self.width) // 2
        top = (Game.SCREEN_HEIGHT - self.height) // 2
        screen.blit(self.img, (left, top))