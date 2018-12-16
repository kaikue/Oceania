import math
import pygame
import Game
from Entity import Entity
import ent.DamageSource

INVINCIBLE_FRAMES = 30

class EntityLiving(Entity):
    
    def __init__(self, pos, imageurl, health):
        super().__init__(pos, imageurl)
        self.max_health = health
        self.health = health
        self.hurt = False
        self.hurt_time = -1
        self.knockback = [0, 0]
        self.attack = None
    
    def update(self, world):
        if self.hurt_time > -1:
            if self.hurt_time == 0:
                self.hurt = False
            self.hurt_time -= 1
        self.knockback[0] = Game.cutoff(self.knockback[0], ent.DamageSource.KNOCKBACK_FALLOFF)
        self.knockback[1] = Game.cutoff(self.knockback[1], ent.DamageSource.KNOCKBACK_FALLOFF)
        if self.knockback[0] != 0:
            self.vel[0] += self.knockback[0]
            self.knockback[0] += math.copysign(ent.DamageSource.KNOCKBACK_FALLOFF, -self.knockback[0])
        if self.knockback[1] != 0:
            self.vel[1] += self.knockback[1]
            self.knockback[1] += math.copysign(ent.DamageSource.KNOCKBACK_FALLOFF, -self.knockback[1])
        super().update(world)
    
    def render(self, screen, pos):
        super().render(screen, pos)
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
        if self.attack is not None:
            self.attack.destroy(world)

    def save(self):
        save_data = super().save()
        save_data["max_health"] = self.max_health
        save_data["health"] = self.health
        save_data["hurt"] = self.hurt
        save_data["hurt_time"] = self.hurt_time
        save_data["knockback"] = self.knockback
        save_data["attack"] = self.attack
        return save_data

    def load(self, save_data):
        super().load(save_data)
        self.max_health = save_data["max_health"]
        self.health = save_data["health"]
        self.hurt = save_data["hurt"]
        self.hurt_time = save_data["hurt_time"]
        self.knockback = save_data["knockback"]
        self.attack = save_data["attack"]