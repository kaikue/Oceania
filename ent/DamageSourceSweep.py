import math
import pygame
import Convert
import Images
import Game
from ent.DamageSource import DamageSource

DEFAULT_REACH = Game.BLOCK_SIZE * Game.SCALE * 17 / 8 #in pixels
MIN_SIZE = Game.BLOCK_SIZE / 2 * Game.SCALE #in pixels
FRAME_LENGTH = 3

class DamageSourceSweep(DamageSource):
    
    def __init__(self, pos, damage, knockback, reach, angle, item = None, parent = None, decay = 100):
        self.reach = reach
        self.item = item
        self.max_decay = decay
        self.angle_mid = angle
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
        img = pygame.Surface((Game.BLOCK_SIZE * 3, Game.BLOCK_SIZE * 3), pygame.SRCALPHA, 32).convert_alpha() #not game scale
        center = img.get_rect().center
        #TODO: blit small diagonal arm image on img (after blitting item? but before rotation)
        if self.item is not None:
            #TODO: self.item may be a dummy pickled object that hasn't been loaded- what should we do?
            #does the parent reference also get lost? that would be bad
            #self.item.load_image()
            item_img = self.item.imgs[0]
            item_img = Images.scale(item_img, 1 / Game.SCALE)
            img.blit(item_img, (0, 0))
        start_deg = math.degrees(self.angle_start - 2 * self.angle_mid)
        end_deg = math.degrees(self.angle_end - 2 * self.angle_mid)
        for i in range(0, self.max_decay + 1, FRAME_LENGTH):
            t = (self.max_decay - i) / self.max_decay
            angle = (1 - t) * start_deg + t * end_deg + 225
            rotated_img = Images.rotate(img, angle)
            rotated_img.get_rect().center = center
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
        
        #TODO: if player is swimming, maybe add some to the pos?
        parent_w = self.parent.bounding_box.width / Game.BLOCK_SIZE / Game.SCALE
        parent_h = self.parent.bounding_box.height / Game.BLOCK_SIZE / Game.SCALE
        self.pos = [self.parent.pos[0] + parent_w / 2, self.parent.pos[1] + parent_h / 2]
    
    def render(self, screen, pos):
        #temporary bounding box
        pygame.draw.rect(screen, Game.RED, \
                         pygame.rect.Rect(Convert.pixels_to_viewport(self.bounding_box.topleft, Game.get_viewport()), 
                                          (self.bounding_box.width, self.bounding_box.height)))
     
    def render_actual(self, screen):
        index = int((self.max_decay - self.decay) / FRAME_LENGTH)
        #self.load_image()
        img = self.imgs[index] #TODO: these might all be dead surfaces if loading in
        pos = Convert.world_to_viewport(self.pos, Game.get_viewport())
        center = img.get_rect().center
        screen.blit(img, (pos[0] - center[0], pos[1] - center[1]))
    
    def destroy(self, world):
        super().destroy(world)
        self.parent.attack = None