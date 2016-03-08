import os
import random
import pickle
import json
import pygame
import Game
import Convert
import Chunk
import TwoWayList

HEIGHT = 256
SEA_LEVEL = HEIGHT / 4
SEA_FLOOR = HEIGHT * 3 / 4
CHUNKS_TO_SIDE = 2

biomes = {}
structures = {}
blocks = {}
block_images = {}
block_icons = {}

def load_data():
    load_biomes()
    load_structures()
    load_blocks()

def load_biomes():
    biomes_file = open("biomes.json", "r")
    global biomes
    biomes = json.load(biomes_file)
    biomes_file.close()

def load_structures():
    structures_file = open("structures.json", "r")
    global structures
    structures = json.load(structures_file)
    structures_file.close()

def load_blocks():
    blocks_file = open("blocks.json", "r")
    global blocks
    blocks = json.load(blocks_file)["blocks"]
    blocks_file.close()
    
    bid = 0
    global block_images
    block_images = {False:{}, True:{}}
    global block_icons
    block_icons = {False:{}, True:{}}
    global block_mappings
    block_mappings = {}
    water_id = 1
    water_image = pygame.image.load(blocks[water_id]["image"]) #have to make water the second one in the file...
    st_water_image = water_image.copy()
    st_water_image.set_alpha(128)
    #st_water_image = pygame.transform.scale(st_water_image, (st_water_image.get_width() * Game.SCALE, st_water_image.get_height() * Game.SCALE))
    
    for block in blocks:
        #set some default attributes
        if "breakable" not in block.keys():
            block["breakable"] = True
        if "connectedTexture" not in block.keys():
            block["connectedTexture"] = False
        if "solid" not in block.keys():
            block["solid"] = True
        if "entity" not in block.keys():
            block["entity"] = ""
        #add an id to the block
        block["id"] = bid
        block_mappings[block["name"]] = bid
        #load the block image
        path = block["image"]
        if path != "":
            blockimg = pygame.image.load(path).convert_alpha()
            if block["connectedTexture"]:
                icon = pygame.Surface((Game.BLOCK_SIZE, Game.BLOCK_SIZE), pygame.SRCALPHA, 32)
                icon = icon.convert_alpha()
                icon.blit(blockimg, (0, 0))
            else:
                icon = blockimg.copy()
            #blockicons[False] is the unscaled version for blockdrops, [True] is scaled up for inventory rendering
            block_icons[False][bid] = icon
            block_icons[True][bid] = pygame.transform.scale(icon, (Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE))
            #blit the image onto the water tile so it isn't just empty transparency
            image = blockimg.copy()
            #for x in range(image.get_width() // Game.BLOCK_SIZE):
            #    for y in range(image.get_height() // Game.BLOCK_SIZE):
            #        image.blit(st_water_image, (x * Game.BLOCK_SIZE, y * Game.BLOCK_SIZE))
            image.blit(blockimg, (0, 0))
            surf = pygame.transform.scale(image, (image.get_width() * Game.SCALE, image.get_height() * Game.SCALE))
            block_images[False][bid] = surf
            
            #background- opaque water image
            image = blockimg.copy()
            for x in range(image.get_width() // Game.BLOCK_SIZE):
                for y in range(image.get_height() // Game.BLOCK_SIZE):
                    image.blit(water_image, (x * Game.BLOCK_SIZE, y * Game.BLOCK_SIZE))
            image.blit(blockimg, (0, 0))
            for x in range(image.get_width() // Game.BLOCK_SIZE):
                for y in range(image.get_height() // Game.BLOCK_SIZE):
                    image.blit(st_water_image, (x * Game.BLOCK_SIZE, y * Game.BLOCK_SIZE))
            surf = pygame.transform.scale(image, (image.get_width() * Game.SCALE, image.get_height() * Game.SCALE))
            block_images[True][bid] = surf
        bid += 1
    block_images[False][water_id] = pygame.Surface((Game.BLOCK_SIZE, Game.BLOCK_SIZE), pygame.SRCALPHA, 32)

def get_block_id(blockname):
    return block_mappings[blockname]

def get_block(blockname):
    return blocks[get_block_id(blockname)]

class World(object):
    
    def __init__(self, name, player):
        self.name = name
        self.dir = "dat/" + self.name
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        random.seed(self.name)
        self.generate_spawn()
        self.player = player
    
    def update(self):
        for x in range(self.loaded_chunks.first, self.loaded_chunks.end):
            chunk = self.loaded_chunks.get(x)
            for entity in chunk.entities:
                entity.update(self)
                if Convert.world_to_chunk(entity.pos[0])[1] != chunk.x:
                    print("Moving", entity, entity.pos, "from", chunk)
                    chunk.entities.remove(entity)
                    self.loaded_chunks.get(Convert.world_to_chunk(entity.pos[0])[1]).entities.append(entity)
    
    def get_block_at(self, world_pos, background):
        chunk = self.loaded_chunks.get(Convert.world_to_chunk(world_pos[0])[1])
        x_in_chunk = Convert.world_to_chunk(world_pos[0])[0]
        return chunk.get_block_at(x_in_chunk, world_pos[1], background)
    
    def set_block_at(self, world_pos, block, background):
        chunk = self.loaded_chunks.get(Convert.world_to_chunk(world_pos[0])[1])
        x_in_chunk = Convert.world_to_chunk(world_pos[0])[0]
        chunk.set_block_at(x_in_chunk, world_pos[1], block, background)
    
    def load_chunks(self, center):
        #unload and serialize unneeded chunks
        old_chunks = self.loaded_chunks.clone()
        for chunk in old_chunks.elements:
            self.save_chunk(chunk)
        
        self.loaded_chunks = TwoWayList.TwoWayList()
        leftchunk = center - CHUNKS_TO_SIDE
        rightchunk = center + CHUNKS_TO_SIDE + 1
        
        for i in range(leftchunk, rightchunk):
            if self.chunk_exists(i):
                chunk = self.load_chunk(i)
            else:
                if i < 0:
                    side = Chunk.RIGHT
                    prev = old_chunks.get(i + 1)
                else:
                    side = Chunk.LEFT
                    prev = old_chunks.get(i - 1)
                chunk = self.generate_chunk(i, prev, side)
            self.loaded_chunks.append(chunk)
        self.loaded_chunks.update_start(-leftchunk)
    
    def render(self, screen, viewport):
        for chunk in self.loaded_chunks.elements:
            chunk.render(screen, viewport)
    
    def render_block(self, block_id, block_pos, connected, screen, viewport, background):
        if connected:
            #check adjacent tiles
            left_block = blocks[self.get_block_at((block_pos[0] - 1, block_pos[1]), background)]["solid"]
            right_block = blocks[self.get_block_at((block_pos[0] + 1, block_pos[1]), background)]["solid"]
            top_block = blocks[self.get_block_at((block_pos[0], block_pos[1] - 1), background)]["solid"]
            bottom_block = blocks[self.get_block_at((block_pos[0], block_pos[1] + 1), background)]["solid"]
            tile = ()
            #there must be some better way to do this
            if not left_block and not right_block and not top_block and not bottom_block:
                tile = (0, 0)
            if not left_block and not right_block and not top_block and bottom_block:
                tile = (0, 1)
            if not left_block and not right_block and top_block and bottom_block:
                tile = (0, 2)
            if not left_block and not right_block and top_block and not bottom_block:
                tile = (0, 3)
            if not left_block and right_block and not top_block and not bottom_block:
                tile = (1, 0)
            if not left_block and right_block and not top_block and bottom_block:
                tile = (1, 1)
            if not left_block and right_block and top_block and bottom_block:
                tile = (1, 2)
            if not left_block and right_block and top_block and not bottom_block:
                tile = (1, 3)
            if left_block and right_block and not top_block and not bottom_block:
                tile = (2, 0)
            if left_block and right_block and not top_block and bottom_block:
                tile = (2, 1)
            if left_block and right_block and top_block and bottom_block:
                tile = (2, 2)
            if left_block and right_block and top_block and not bottom_block:
                tile = (2, 3)
            if left_block and not right_block and not top_block and not bottom_block:
                tile = (3, 0)
            if left_block and not right_block and not top_block and bottom_block:
                tile = (3, 1)
            if left_block and not right_block and top_block and bottom_block:
                tile = (3, 2)
            if left_block and not right_block and top_block and not bottom_block:
                tile = (3, 3)
            screen.blit(block_images[background][block_id],
                        Convert.world_to_viewport(block_pos, viewport),
                        pygame.Rect((tile[0] * Game.BLOCK_SIZE * Game.SCALE, tile[1] * Game.BLOCK_SIZE * Game.SCALE),
                                    (Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE)))
        else:
            #just render it normally
            screen.blit(block_images[background][block_id], Convert.world_to_viewport(block_pos, viewport))
    
    def save_chunk(self, chunk):
        chunkfile = open(self.dir + "/chunk" + str(chunk.x) + "data", "wb")
        pickle.dump(chunk, chunkfile)
        chunkfile.close()
    
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
        for entity in chunk.entities:
            entity.load_image()
        return chunk
    
    def generate_spawn(self):
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
    
    def generate_chunk(self, index, basechunk, side):
        chunk = Chunk.Chunk()
        chunk.generate_from_chunk(basechunk, side)
        self.save_chunk(chunk)
        return chunk
    
    def close(self):
        self.save_all()

if __name__ == "__main__":
    Game.main()