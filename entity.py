import pygame

class Entity(object):
    
    def __init__(self, x, y, imageurl):
        self.x = x
        self.y = y
        self.img = pygame.image.load(imageurl).convert_alpha()
        self.dir = [0, 0] #direction: -1, 0, 1
        self.vel = [0, 0] #speeds: any numbers
    
    def update(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
    
    def render(self, screen, x, y):
        screen.blit(self.img, (x, y))