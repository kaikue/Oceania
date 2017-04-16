from ent.EntityLiving import EntityLiving

class EntityEnemy(EntityLiving):
    
    def __init__(self, pos, imageurl, health):
        super(EntityEnemy, self).__init__(pos, imageurl, health)
        self.max_speed = 0.25
        self.acceleration = 0.01
    
    def update(self, world):
        move_dir = self.find_move_dir()
        hspeed = min(abs(self.vel[0] + self.acceleration * move_dir[0]), self.max_speed) * move_dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * move_dir[1]), self.max_speed) * move_dir[1]
        self.vel = [hspeed, vspeed]
        super(EntityEnemy, self).update(world)
    
    def find_move_dir(self):
        move_dir = [0, 0]
        #TODO: a* pathfinding
        return move_dir
    
    def die(self, world):
        super(EntityEnemy, self).die(world)