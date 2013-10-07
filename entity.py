import pygame

class Entity(object):
    
    def __init__(self, pos, imageurl):
        self.pos = pos
        self.img = pygame.image.load(imageurl).convert_alpha()
        self.dir = [0, 0] #direction: -1, 0, 1
        self.vel = [0, 0] #speeds: any numbers
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    
    def render(self, screen, pos):
        screen.blit(self.img, pos)