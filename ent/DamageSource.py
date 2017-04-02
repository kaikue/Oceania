from Entity import Entity

class DamageSource(Entity):
    
    def __init__(self, pos, imageurl, damage, parent = None, decay = -1):
        #TODO: remove imageurl
        super(DamageSource, self).__init__(pos, imageurl)
        self.damage = damage
        #self.damage_type = damage_type #TODO
        self.parent = parent
        self.decay = decay
    
    def update(self, world):
        super(DamageSource, self).update(world)
        
        if self.parent is not None:
            #TODO: move with parent? right now it does that from the pos reference
            pass
        
        if self.decay > -1:
            if self.decay == 0:
                world.remove_entity(self)
            self.decay -= 1