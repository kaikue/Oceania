from Entity import Entity
from ent.EntityLiving import EntityLiving

DEFAULT_ATTACK = 1
DEFAULT_KNOCKBACK = 0.2 #make sure this is a multiple of KNOCKBACK_FALLOFF
KNOCKBACK_FALLOFF = 0.01

class DamageSource(Entity):
    
    def __init__(self, pos, damage, knockback, imageurl = "", parent = None, decay = -1):
        super(DamageSource, self).__init__(pos, imageurl)
        self.damage = damage
        self.knockback = knockback
        #self.damage_type = damage_type #TODO: different types of damage e.g. sword, explosion, etc.
        self.parent = parent
        self.decay = decay
    
    def update(self, world):
        super(DamageSource, self).update(world)
        
        if self.parent is not None:
            #TODO: move with parent? right now it does that from the pos reference
            # and bullets shouldn't do that anyway
            pass
        
        if self.decay > -1:
            if self.decay == 0:
                world.remove_entity(self)
            self.decay -= 1
    
    def collide_with(self, entity, world):
        if isinstance(entity, EntityLiving):
            if self.parent != entity:
                entity.damage(self, world)