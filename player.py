import entity

class Player(entity.Entity):
    
    def __init__(self, pos, imageurl):
        super(Player, self).__init__(pos, imageurl)
        self.max_speed = 0.25
        self.acceleration = 0.025 #fiddle with this until it seems good
    
    def update(self, world):
        hspeed = min(abs(self.vel[0] + self.acceleration * self.dir[0]), self.max_speed) * self.dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * self.dir[1]), self.max_speed) * self.dir[1]
        self.vel = [hspeed, vspeed]
        super(Player, self).update(world)