import math
import pygame
import Convert
import Game
from ent.DamageSource import DamageSource

class DamageSourceSweep(DamageSource):
    
    def __init__(self, pos, damage, knockback, reach, angle, imageurl = "", parent = None, decay = 100):
        super().__init__(pos, damage, knockback, imageurl, parent, True, decay)
        if self.parent == None:
            raise AttributeError("DamageSourceSweep must have a parent.")
        self.reach = reach
        self.max_decay = decay
        if -math.pi / 2 < angle < math.pi / 2:
            self.angle_start = angle - math.pi / 2
            self.angle_end = angle + math.pi / 2
        else:
            #go backwards
            self.angle_start = angle + math.pi / 2
            self.angle_end = angle - math.pi / 2
    
    def update(self, world):
        super().update(world)
        
        t = (self.max_decay - self.decay) / self.max_decay
        angle = (1 - t) * self.angle_start + t * self.angle_end #TODO: swing downward if on left
        
        #all calculations in pixels
        px = self.parent.bounding_box.centerx + self.reach * math.cos(angle)
        py = self.parent.bounding_box.centery + self.reach * math.sin(angle)
        self.bounding_box.x = px
        self.bounding_box.y = py
        self.bounding_box.width = px - self.parent.bounding_box.centerx
        self.bounding_box.height = py - self.parent.bounding_box.centery
        
        #TODO: make it more thicc, centered on px and py
        #TODO: make work properly for other quadrants (no negative widths and stuff)
        
    
    def render(self, screen, pos):
        #TODO: animate held item swinging
        pygame.draw.rect(screen, Game.RED, \
                         pygame.rect.Rect(Convert.pixels_to_viewport(self.bounding_box.topleft, Game.viewport), \
                                          (self.bounding_box.width, self.bounding_box.height)))