#import random
#import layer
#import block
import chunk
from twowaylist import TwoWayList

HEIGHT = 256
SEA_LEVEL = HEIGHT / 4
SEA_FLOOR = HEIGHT * 3 / 4

class World(object):
    
    def __init__(self):
        spawn = chunk.Chunk()
        spawn.generate_spawn()
        #self.chunks = {spawn.x: spawn}
        self.chunks = TwoWayList()
        self.chunks.append(spawn)
        r1 = chunk.Chunk()
        r1.generate_from_chunk(spawn, chunk.LEFT)
        #self.chunks[r1.x] = r1
        self.chunks.append(r1)
        r2 = chunk.Chunk()
        r2.generate_from_chunk(r1, chunk.LEFT)
        #self.chunks[r2.x] = r2
        self.chunks.append(r2)
        r1l = chunk.Chunk()
        r1l.generate_from_chunk(spawn, chunk.RIGHT)
        #self.chunks[r1l.x] = r1l
        self.chunks.prepend(r1l)
        r2l = chunk.Chunk()
        r2l.generate_from_chunk(r1l, chunk.RIGHT)
        #self.chunks[r2l.x] = r2l
        self.chunks.prepend(r2l)
        self.loaded_chunks = self.chunks #improve
    
    def update(self):
        #for x in range(min(self.loaded_chunks.keys), max(self.loaded_chunks.keys), chunk.WIDTH):
        for x in range(self.loaded_chunks.first, self.loaded_chunks.last):
            chunk = self.loaded_chunks.get(x)
            for entity in chunk.entities:
                entity.update()
                chunkmove = 0
                while entity.x < 0:
                    chunkmove -= 1
                    entity.x += 16
                while entity.x >= 16:
                    chunkmove = 1
                    entity.x -= 16
                chunk.entities.remove(entity)
                #self.chunks[x + chunk.WIDTH * chunkmove].entities.append(entity)
                self.chunks.get(x - chunkmove).entities.append(entity)
    
    def render(self, screen, viewport):
        #for i in range(viewport.x // chunk.WIDTH * chunk.WIDTH, viewport.right + viewport.right % chunk.WIDTH, chunk.WIDTH):
        #    self.loaded_chunks.get(i).render(screen, viewport)
        
        #change this to render only chunks on screen, not just all loaded chunks
        #for chunk in self.loaded_chunks.elements:
        #    chunk.render(screen, viewport)
        for i in range(viewport.x // chunk.WIDTH, viewport.right // chunk.WIDTH + 1):
            self.loaded_chunks.get(i).render(screen, viewport)
    
    """
    def generate(self):
        heights = self.midpoint_displace()
        for y in range(len(self.blocks)):
            for x in range(len(self.blocks[y])):
                if y < SEA_LEVEL:
                    self.blocks[y][x] = block.Block(block.AIR)
                elif y < heights[x]:
                    self.blocks[y][x] = block.Block(block.WATER)
                else:
                    self.blocks[y][x] = block.Block(block.DIRT)
    """
    """
    def midpoint_displace(self):
        iters = 7
        points = [SEA_LEVEL, SEA_FLOOR, SEA_LEVEL]
        displace = 100
        for _ in range(iters):
            newpoints = []
            for i in range(len(points) - 1):
                midpoint = (points[i] + points[i + 1]) / 2
                midpoint += random.random() * displace * 2 - displace
                displace /= 2
                newpoints.append(points[i])
                newpoints.append(midpoint)
            newpoints.append(points[-1]) #add the last point which wasn't counted
            points = newpoints
        return points
    """