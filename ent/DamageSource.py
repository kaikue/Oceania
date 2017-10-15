import Game
from Entity import Entity
from ent.EntityLiving import EntityLiving

DEFAULT_ATTACK = 1
DEFAULT_KNOCKBACK = 0.2 #make sure this is a multiple of KNOCKBACK_FALLOFF
KNOCKBACK_FALLOFF = 0.01
DEFAULT_REACH = 2 * Game.BLOCK_SIZE * Game.SCALE #in pixels

class DamageSource(Entity):
    
    def __init__(self, pos, damage, knockback, imageurl = "", parent = None, move_with_parent = True, decay = -1):
        super().__init__(pos, imageurl)
        self.damage = damage
        self.knockback = knockback
        #self.damage_type = damage_type #TODO: different types of damage e.g. sword, explosion, etc.
        self.parent = parent
        self.move_with_parent = move_with_parent
        self.decay = decay
    
    def update(self, world):
        super().update(world)
        
        if self.parent is not None:
            if self.move_with_parent:
                for i in (0, 1):
                    self.pos[i] += self.parent.vel[i]
        
        if self.decay > -1:
            if self.decay == 0:
                world.remove_entity(self)
            self.decay -= 1
    
    def collide_with(self, entity, world):
        if isinstance(entity, EntityLiving):
            if self.parent != entity:
                entity.damage(self, world)