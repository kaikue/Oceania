import math
import World
from ent.EntityLiving import EntityLiving

MAX_SEARCH_DISTANCE = 50

class EntityEnemy(EntityLiving):
    
    def __init__(self, pos, imageurl, health):
        super(EntityEnemy, self).__init__(pos, imageurl, health)
        self.max_speed = 0.1
        self.acceleration = 0.001
    
    def update(self, world):
        move_dir = self.find_move_dir(world)
        hspeed = min(abs(self.vel[0] + self.acceleration * move_dir[0]), self.max_speed) * move_dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * move_dir[1]), self.max_speed) * move_dir[1]
        self.vel = [hspeed, vspeed]
        super(EntityEnemy, self).update(world)
    
    def find_move_dir(self, world):
        self.is_clear(world, self.pos)
        move_dir = [0, 0]
        goal = (int(world.player.pos[0]), int(world.player.pos[1]))
        current = (round(self.pos[0]), round(self.pos[1]))
        
        #TODO cache for performance
        path = self.pathfind(world, current, goal)
        if len(path) == 0:
            return move_dir
        dest = path[0]
        
        if self.pos[0] < dest[0]:
            move_dir[0] = 1
        elif self.pos[0] > dest[0]:
            move_dir[0] = -1
        if self.pos[1] < dest[1]:
            move_dir[1] = 1
        elif self.pos[1] > dest[1]:
            move_dir[1] = -1
        return move_dir
    
    def pathfind(self, world, start, goal):
        visited = []
        discovered = [start]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        iterations = 0
        while len(discovered) > 0:
            current = self.pick_lowest(discovered, f_score)
            if current == goal:
                return self.reconstruct_path(came_from, current)
            discovered.remove(current)
            visited.append(current)
            for neighbor in self.find_neighbors(current):
                if not self.is_clear(world, neighbor):
                    continue
                if neighbor in visited:
                    continue
                tentative_g_score = g_score[current] + 1
                if neighbor not in discovered:
                    discovered.append(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
            iterations += 1
            if iterations > MAX_SEARCH_DISTANCE:
                break
        return []
    
    def heuristic(self, p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    
    def pick_lowest(self, discovered, f_score):
        min_node = discovered[0]
        min_score = f_score[min_node]
        for node in discovered:
            cur_score = f_score[node]
            if cur_score < min_score:
                min_score = cur_score
                min_node = node
        return min_node
    
    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from.keys():
            path.insert(0, current)
            current = came_from[current]
        return path
    
    def find_neighbors(self, point):
        neighbors =  [(point[0] - 1, point[1]),
                      (point[0] + 1, point[1])]
        if point[1] > 0:
            neighbors.append((point[0], point[1] - 1))
        if point[1] < World.HEIGHT - 1:
            neighbors.append((point[0], point[1] + 1))
        return neighbors
    
    def is_clear(self, world, pos):
        for x in range(int(pos[0]), int(pos[0] + self.width)):
            for y in range(int(pos[1]), int(pos[1] + self.height)):
                block = World.get_block(world.get_block_at((x, y), False))
                if block["solid"]:
                    return False
        return True
    
    def die(self, world):
        #TODO spawn drops
        super(EntityEnemy, self).die(world)