import pygame
import Game
from Entity import Entity
from ent.DamageSource import DamageSource

INVINCIBLE_FRAMES = 30

class EntityLiving(Entity):
    
    def __init__(self, pos, imageurl, health):
        super(EntityLiving, self).__init__(pos, imageurl)
        self.max_health = health
        self.health = health
        self.hurt = False
        self.hurt_time = -1
    
    def update(self, world):
        if self.hurt_time > -1:
            if self.hurt_time == 0:
                self.hurt = False
            self.hurt_time -= 1
            
        super(EntityLiving, self).update(world)
    
    def render(self, screen, pos):
        super(EntityLiving, self).render(screen, pos)
        if self.hurt:
            mask = pygame.mask.from_surface(self.img)
            olist = mask.outline()
            polysurface = pygame.Surface((self.img.get_width() * Game.SCALE, self.img.get_height() * Game.SCALE), pygame.SRCALPHA)
            color = (128, 0, 0, 128)
            pygame.draw.polygon(polysurface, color, olist, 0)
            screen.blit(polysurface, pos)
    
    def collide_with(self, entity, world):
        if isinstance(entity, DamageSource):
            if entity.parent != self:
                self.damage(entity, world)
    
    def damage(self, source, world):
        if not self.hurt:
            self.set_hurt(INVINCIBLE_FRAMES)
            self.health -= source.damage
            if self.health <= 0:
                self.die(world)
    
    def set_hurt(self, time):
        self.hurt = True
        self.hurt_time = time
    
    def die(self, world):
        world.remove_entity(self)
        #TODO: spawn drops