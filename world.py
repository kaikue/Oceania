#import random
#import layer
import convert
import block
import chunk
from twowaylist import TwoWayList

HEIGHT = 256
SEA_LEVEL = HEIGHT / 4
SEA_FLOOR = HEIGHT * 3 / 4

class World(object):
    
    def __init__(self):
        spawn = chunk.Chunk()
        spawn.generate_spawn()
        self.chunks = TwoWayList()
        self.chunks.append(spawn)
        r1 = chunk.Chunk()
        r1.generate_from_chunk(spawn, chunk.LEFT)
        self.chunks.append(r1)
        r2 = chunk.Chunk()
        r2.generate_from_chunk(r1, chunk.LEFT)
        self.chunks.append(r2)
        r1l = chunk.Chunk()
        r1l.generate_from_chunk(spawn, chunk.RIGHT)
        self.chunks.prepend(r1l)
        r2l = chunk.Chunk()
        r2l.generate_from_chunk(r1l, chunk.RIGHT)
        self.chunks.prepend(r2l)
        self.loaded_chunks = self.chunks #improve
    
    def update(self):
        for x in range(self.loaded_chunks.first, self.loaded_chunks.last):
            check_chunk = self.loaded_chunks.get(x)
            for entity in check_chunk.entities:
                entity.update(self)
                if entity.pos[0] / chunk.WIDTH != check_chunk.x: 
                    check_chunk.entities.remove(entity)
                    self.chunks.get(entity.pos[0] / chunk.WIDTH).entities.append(entity)
        """
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
                if chunkmove != 0:
                    chunk.entities.remove(entity)
                    #entity.x = convert.world_to_chunk(convert.chunk_to_world(entity.x))[0]
                    self.chunks.get(x - chunkmove).entities.append(entity)
        """
    
    def render(self, screen, viewport):
        left_chunk = convert.world_to_chunk(convert.pixel_to_world(viewport.x))[1]
        right_chunk = left_chunk + convert.world_to_chunk(convert.pixel_to_world(viewport.width))[1] + 2
        #print(left_chunk, right_chunk)
        for i in range(left_chunk, right_chunk):
            try:
                self.loaded_chunks.get(i).render(screen, viewport)
            except IndexError:
                pass