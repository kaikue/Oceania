import os
import math
import pickle
import Convert
import Chunk
import TwoWayList
import Block

HEIGHT = 256
SEA_LEVEL = HEIGHT / 4
SEA_FLOOR = HEIGHT * 3 / 4
CHUNKS_TO_SIDE = 2

class World(object):
    
    def __init__(self, name, player):
        self.name = name
        self.dir = "dat/" + self.name
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        spawn = Chunk.Chunk()
        spawn.generate_spawn()
        self.loaded_chunks = TwoWayList.TwoWayList()
        self.loaded_chunks.append(spawn)
        r1 = Chunk.Chunk()
        r1.generate_from_chunk(spawn, Chunk.LEFT)
        self.loaded_chunks.append(r1)
        r2 = Chunk.Chunk()
        r2.generate_from_chunk(r1, Chunk.LEFT)
        self.loaded_chunks.append(r2)
        r1l = Chunk.Chunk()
        r1l.generate_from_chunk(spawn, Chunk.RIGHT)
        self.loaded_chunks.prepend(r1l)
        r2l = Chunk.Chunk()
        r2l.generate_from_chunk(r1l, Chunk.RIGHT)
        self.loaded_chunks.prepend(r2l)
        self.save_all()
        self.player = player
    
    def update(self):
        for x in range(self.loaded_chunks.first, self.loaded_chunks.end):
            chunk = self.loaded_chunks.get(x)
            for entity in chunk.entities:
                entity.update(self)
                if entity.pos[0] / Chunk.WIDTH != chunk.x: 
                    chunk.entities.remove(entity)
                    self.loaded_chunks.get(entity.pos[0] / Chunk.WIDTH).entities.append(entity)
    
    def find_angle(self, player, mouse_pos, viewport):
        #find nearest breakable block based on angle from player pos to mouse pos (raycasting?)
        #begin breaking it
        x_diff = Convert.viewport_to_pixel(mouse_pos[0], viewport, 0) - player.bounding_box.x
        y_diff = Convert.viewport_to_pixel(mouse_pos[1], viewport, 1) - player.bounding_box.y
        angle = math.atan2(y_diff, x_diff)
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
        self.loaded_chunks.get(chunk).blocks[block_pos[1]][x_in_chunk] = Block.Block(Block.WATER)
    
    def load_chunks(self, center):
        #unload and serialize unneeded chunks
        self.old_chunks = self.loaded_chunks.clone()
        
        self.loaded_chunks = TwoWayList.TwoWayList()
        #if the needed chunks do not all exist, generate some more
        leftchunk = center - CHUNKS_TO_SIDE
        print("Start:", leftchunk)
        rightchunk = center + CHUNKS_TO_SIDE + 1
        print("End:", rightchunk)
        
        for i in range(leftchunk, rightchunk):
            if self.chunk_exists(i):
                chunk = self.load_chunk(i)
            else:
                if i < 0:
                    side = Chunk.RIGHT
                    prev = self.old_chunks.get(i + 1)
                else:
                    side = Chunk.LEFT
                    prev = self.old_chunks.get(i - 1)
                chunk = self.generate_chunk(i, prev, side)
            self.loaded_chunks.append(chunk)
        self.loaded_chunks.update_start(-leftchunk)
        
        """negstart = min(-1, rightchunk) - 1
        for i in range(negstart, leftchunk, -1):
            #print(i, self.old_chunks)
            self.loaded_chunks.prepend(self.load_chunk(i))
        #print(lastchunk, self.old_chunks)
        self.loaded_chunks.prepend(self.generate_chunk(leftchunk, self.old_chunks.get(leftchunk + 1), Chunk.RIGHT))
        
        posstart = max(0, leftchunk)
        for i in range(posstart, rightchunk):
            #print("", i, self.old_chunks)
            self.loaded_chunks.append(self.load_chunk(i))
        #print(lastchunk, self.old_chunks)
        self.loaded_chunks.append(self.generate_chunk(rightchunk, self.old_chunks.get(rightchunk - 1), Chunk.LEFT))
        #self.loaded_chunks.update_start(-(center - CHUNKS_TO_SIDE))
        """
        
        #save all unloaded chunks
        print(self.loaded_chunks)
        for old in self.old_chunks.elements:
            save = True
            #if chunk not in self.loaded_chunks.elements:
            for new in self.loaded_chunks.elements:
                if old.x == new.x:
                    save = False
            if save:
                print("Unloaded", old.x)
                self.save_chunk(old)
        print()
    
    def render(self, screen, viewport):
        for chunk in self.loaded_chunks.elements:
            chunk.render(screen, viewport)
    
    def save_chunk(self, chunk):
        chunkfile = open(self.dir + "/chunk" + str(chunk.x) + "data", "wb")
        pickle.dump(chunk, chunkfile)
        chunkfile.close()
        #print("Saved chunk", chunk.x)
    
    def save_all(self):
        for chunk in self.loaded_chunks.elements:
            self.save_chunk(chunk)
    
    def get_chunk_file(self, index):
        return self.dir + "/chunk" + str(index) + "data"
    
    def chunk_exists(self, index):
        return os.path.isfile(self.get_chunk_file(index))
    
    def load_chunk(self, index):
        chunkfile = open(self.get_chunk_file(index), "rb")
        chunk = pickle.load(chunkfile)
        chunkfile.close()
        return chunk
    
    def generate_chunk(self, index, basechunk, side):
        #print("Generating", index, "from", basechunk.x)
        chunk = Chunk.Chunk()
        chunk.generate_from_chunk(basechunk, side)
        self.save_chunk(chunk)
        return chunk
    
    def close(self):
        self.save_all()