import pygame
import Game

#Buttons needed: play, quit, options
WIDTH = 150
HEIGHT = 60
COLOR_INACTIVE = (97, 180, 207)
COLOR_HOVER = (58, 170, 207)
COLOR_PRESSED = (9, 121, 159)
FONT_COLOR = (0, 0, 0)

def draw_rounded_rect(surface, rect, color, radius=0.4):
    """
    draw_rounded_rect(surface,rect,color,radius=0.4)
    By josmiley: http://joel-murielle.perso.sfr.fr/AAfilledRoundedRect.py
    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """
    
    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size, pygame.SRCALPHA)
    
    circle       = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)
    
    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)
    
    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))
    
    rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)
    
    return surface.blit(rectangle,pos)

class Button(object):
    
    def __init__(self, pos, text, effect):
        self.pos = pos
        self.text = text
        self.effect = effect
        self.pressed = False
        self.font = pygame.font.SysFont("monospace", 20)
    
    def activate(self):
        if self.effect == "play":
            Game.play()
        elif self.effect == "quit":
            Game.close()
    
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], WIDTH, HEIGHT)
    
    def mouse_hover(self):
        return self.get_rect().collidepoint(pygame.mouse.get_pos())
    
    def render(self, screen):
        if self.mouse_hover():
            if self.pressed:
                color = COLOR_PRESSED
            else:
                color = COLOR_HOVER
        else:
            color = COLOR_INACTIVE
        draw_rounded_rect(screen, self.get_rect(), color)
        text_img = self.font.render(self.text, 0, FONT_COLOR)
        h = text_img.get_height()
        w = text_img.get_width()
        screen.blit(text_img, (self.pos[0] + (WIDTH - w) / 2, self.pos[1] + (HEIGHT - h) / 2))

if __name__ == "__main__":
    Game.main()