import entity

class Player(entity.Entity):
    
    def __init__(self, pos, imageurl, max_speed):
        super(Player, self).__init__(pos, imageurl)
        self.max_speed = max_speed
        self.acceleration = 0.5 #fiddle with this until it seems good
    
    def update(self):
        #UH OH
        hspeed = min(abs(self.vel[0] + self.acceleration * self.dir[0]), self.max_speed) * self.dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * self.dir[1]), self.max_speed) * self.dir[1]
        self.vel = [hspeed, vspeed]
        super(Player, self).update()