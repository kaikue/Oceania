import Game
from ent.EntityLiving import EntityLiving

class EntityEnemy(EntityLiving):
    
    def __init__(self, pos, imageurl, health):
        super(EntityEnemy, self).__init__(pos, imageurl, health)
        self.max_speed = 0.1
        self.acceleration = 0.001
    
    def update(self, world):
        move_dir = self.find_move_dir()
        hspeed = min(abs(self.vel[0] + self.acceleration * move_dir[0]), self.max_speed) * move_dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * move_dir[1]), self.max_speed) * move_dir[1]
        self.vel = [hspeed, vspeed]
        super(EntityEnemy, self).update(world)
    
    def find_move_dir(self):
        move_dir = [0, 0]
        #TODO: a* pathfinding
        goal = Game.get_world().player.pos
        current = self.pos
        if current[0] < goal[0]:
            move_dir[0] = 1
        elif current[0] > goal[0]:
            move_dir[0] = -1
        if current[1] < goal[1]:
            move_dir[1] = 1
        elif current[1] > goal[1]:
            move_dir[1] = -1
        return move_dir
    
    def die(self, world):
        super(EntityEnemy, self).die(world)