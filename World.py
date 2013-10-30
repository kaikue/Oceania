import math
import pickle
import Convert
import Chunk
import TwoWayList
import Block

HEIGHT = 256
SEA_LEVEL = HEIGHT / 4
SEA_FLOOR = HEIGHT * 3 / 4
CHUNKS_TO_SIDE = 1

class World(object):
    
    def __init__(self, player):
        spawn = Chunk.Chunk()
        spawn.generate_spawn()
        self.chunks = TwoWayList.TwoWayList()
        self.chunks.append(spawn)
        r1 = Chunk.Chunk()
        r1.generate_from_chunk(spawn, Chunk.LEFT)
        self.chunks.append(r1)
        r2 = Chunk.Chunk()
        r2.generate_from_chunk(r1, Chunk.LEFT)
        self.chunks.append(r2)
        r1l = Chunk.Chunk()
        r1l.generate_from_chunk(spawn, Chunk.RIGHT)
        self.chunks.prepend(r1l)
        r2l = Chunk.Chunk()
        r2l.generate_from_chunk(r1l, Chunk.RIGHT)
        self.chunks.prepend(r2l)
        #for chunk in self.chunks.elements:
        #    chunkfile = open("chunk" + str(chunk.x) + "data", "wb")
        #    pickle.dump(chunk, chunkfile)
        #    chunkfile.close()
        self.load_chunks(0)
        self.player = player
    
    def update(self):
        for x in range(self.loaded_chunks.first, self.loaded_chunks.end):
            chunk = self.loaded_chunks.get(x)
            for entity in chunk.entities:
                entity.update(self)
                if entity.pos[0] / Chunk.WIDTH != chunk.x: 
                    chunk.entities.remove(entity)
                    self.chunks.get(entity.pos[0] / Chunk.WIDTH).entities.append(entity)
    
    def find_angle(self, player, mouse_pos, viewport):
        #find nearest breakable block based on angle from player pos to mouse pos (raycasting?)
        #begin breaking it
        x_diff = Convert.viewport_to_pixel(mouse_pos[0], viewport, 0) - player.bounding_box.x
        y_diff = Convert.viewport_to_pixel(mouse_pos[1], viewport, 1) - player.bounding_box.y
        angle = math.atan2(y_diff, x_diff) #not sure if y should be negative
        return angle
    
    def find_pos(self, angle, offset):
        #in pixels
        MAX_DIST = 64
        dist = MAX_DIST
        return [offset[0] + dist * math.cos(angle), offset[1] + dist * math.sin(angle)]
    
    def break_block(self, player, mouse_pos, viewport):
        angle = self.find_angle(player, mouse_pos, viewport)
        block_pos = Convert.pixels_to_world(self.find_pos(angle, player.pixel_pos()))
        chunk = Convert.world_to_chunk(block_pos[0])[1]
        x_in_chunk = Convert.world_to_chunk(block_pos[0])[0]
        self.chunks.get(chunk).blocks[block_pos[1]][x_in_chunk] = Block.Block(Block.WATER)
    
    def load_chunks(self, center):
        #unload and serialize unneeded chunks
        self.loaded_chunks = self.chunks.get_range(center - CHUNKS_TO_SIDE, center + CHUNKS_TO_SIDE + 1)
    
    def render(self, screen, viewport):
        for chunk in self.loaded_chunks.elements:
            chunk.render(screen, viewport)
    
    def load(self):
        self.chunks = TwoWayList.TwoWayList()
        for i in range(-1, -3, -1):
            chunkfile = open("dat/chunk" + str(i) + "data", "rb")
            self.chunks.prepend(pickle.load(chunkfile))
            chunkfile.close()
        for i in range(0, 3):
            chunkfile = open("dat/chunk" + str(i) + "data", "rb")
            self.chunks.append(pickle.load(chunkfile))
            chunkfile.close()
        self.load_chunks(Convert.world_to_chunk(self.player.pos[0])[1])
    
    def close(self):
        for chunk in self.chunks.elements:
            chunkfile = open("dat/chunk" + str(chunk.x) + "data", "wb")
            pickle.dump(chunk, chunkfile)
            chunkfile.close()