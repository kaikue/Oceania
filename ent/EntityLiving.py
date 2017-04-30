import math
import pygame
import Game
from Entity import Entity
import ent.DamageSource

INVINCIBLE_FRAMES = 30

class EntityLiving(Entity):
    
    def __init__(self, pos, imageurl, health):
        super(EntityLiving, self).__init__(pos, imageurl)
        self.max_health = health
        self.health = health
        self.hurt = False
        self.hurt_time = -1
        self.knockback = [0, 0]
    
    def update(self, world):
        if self.hurt_time > -1:
            if self.hurt_time == 0:
                self.hurt = False
            self.hurt_time -= 1
        if self.knockback[0] != 0:
            self.vel[0] += self.knockback[0]
            self.knockback[0] += math.copysign(ent.DamageSource.KNOCKBACK_FALLOFF, -self.knockback[0])
        if self.knockback[1] != 0:
            self.vel[1] += self.knockback[1]
            self.knockback[1] += math.copysign(ent.DamageSource.KNOCKBACK_FALLOFF, -self.knockback[1])
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
    
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
    
    def damage(self, source, world):
        if not self.hurt:
            self.set_hurt(INVINCIBLE_FRAMES)
            self.health -= source.damage
            self.apply_knockback(source)
            if self.health <= 0:
                self.die(world)
    
    def set_hurt(self, time):
        self.hurt = True
        self.hurt_time = time
    
    def apply_knockback(self, source):
        k = source.knockback
        x1 = source.bounding_box.centerx
        y1 = source.bounding_box.centery
        x2 = self.bounding_box.centerx
        y2 = self.bounding_box.centery
        #normalize vector and multiply by strength of knockback
        b = x2 - x1
        h = y2 - y1
        m = math.sqrt(b ** 2 + h ** 2)
        self.knockback = [k * b / m, k * h / m]
    
    def die(self, world):
        world.remove_entity(self)