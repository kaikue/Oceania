from ent.DamageSource import DamageSource

class DamageSourceBullet(DamageSource):
    
    def __init__(self, pos, damage, knockback, vel, imageurl = "", parent = None, decay = -1):
        super().__init__(pos, damage, knockback, imageurl, parent, False, decay)
        self.vel = vel