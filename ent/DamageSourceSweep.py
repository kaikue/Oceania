import math
import pygame
import Convert
import Images
import Game
from ent.DamageSource import DamageSource

DEFAULT_REACH = 2 * Game.BLOCK_SIZE * Game.SCALE #in pixels
MIN_SIZE = Game.BLOCK_SIZE / 2 * Game.SCALE #in pixels
FRAME_LENGTH = 3

class DamageSourceSweep(DamageSource):
    
    def __init__(self, pos, damage, knockback, reach, angle, item = None, parent = None, decay = 100):
        self.reach = reach
        self.item = item
        self.max_decay = decay
        if -math.pi / 2 < angle < math.pi / 2:
            self.side = Game.LEFT
            self.angle_start = angle - math.pi / 2
            self.angle_end = angle + math.pi / 2
        else:
            self.side = Game.RIGHT
            self.angle_start = angle + math.pi / 2
            self.angle_end = angle - math.pi / 2
        super().__init__(pos, damage, knockback, "", parent, decay)
        if self.parent == None:
            raise AttributeError("DamageSourceSweep must have a parent.")
        self.parent.attack = self
    
    def load_image(self):
        self.img = None
        self.imgs = []
        if self.item is not None:
            img = self.item.imgs[0]
            img = Images.scale(img, 1 / Game.SCALE)
            start_deg = math.degrees(self.angle_start)
            end_deg = math.degrees(self.angle_end)
            for i in range(0, self.max_decay + 1, FRAME_LENGTH):
                t = (self.max_decay - i) / self.max_decay
                angle = (1 - t) * start_deg + t * end_deg + 225
                rotated_img = Images.rotate(img, angle)
                self.imgs.append(Images.scale(rotated_img, Game.SCALE))
    
    def update(self, world):
        super().update(world)
        
        t = (self.max_decay - self.decay) / self.max_decay
        angle = (1 - t) * self.angle_start + t * self.angle_end
        
        #all calculations in pixels
        px = self.parent.bounding_box.centerx + self.reach * math.cos(angle)
        py = self.parent.bounding_box.centery + self.reach * math.sin(angle)
        pw = self.parent.bounding_box.centerx - px
        ph = self.parent.bounding_box.centery - py
        
        #make sure dimensions are positive
        if pw < 0:
            pw *= -1
            px -= pw
        if ph < 0:
            ph *= -1
            py -= ph
        
        #minimum thickness
        if pw < MIN_SIZE:
            px += (MIN_SIZE - pw) / 2
            pw = MIN_SIZE
        if ph < MIN_SIZE:
            py += (MIN_SIZE - ph) / 2
            ph = MIN_SIZE
        
        self.bounding_box.x = px
        self.bounding_box.y = py
        self.bounding_box.width = pw
        self.bounding_box.height = ph
    
    def render(self, screen, pos):
        #temporary bounding box
        pygame.draw.rect(screen, Game.RED, \
                         pygame.rect.Rect(Convert.pixels_to_viewport(self.bounding_box.topleft, Game.viewport), \
                                          (self.bounding_box.width, self.bounding_box.height)))
        
        index = int((self.max_decay - self.decay) / FRAME_LENGTH)
        img = self.imgs[index]
        """offset_pos = [pos[0], pos[1]]
        offset_pos[1] += Game.BLOCK_SIZE * Game.SCALE * -8 / 16
        if self.side == Game.LEFT:
            offset_pos[0] += Game.BLOCK_SIZE * Game.SCALE * -8 / 16
        else:
            offset_pos[1] += Game.BLOCK_SIZE * Game.SCALE * 8 / 16"""
        screen.blit(img, Convert.pixels_to_viewport(self.bounding_box.topleft, Game.viewport)) #it's not that simple...
    
    def destroy(self, world):
        super().destroy(world)
        self.parent.attack = None