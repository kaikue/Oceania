import os
import threading
import random
import pickle
import json
import pygame
import Game
import Convert
import Chunk
import TwoWayList
import Images

HEIGHT = 256
SEA_LEVEL = HEIGHT / 4
SEA_FLOOR = HEIGHT * 3 / 4
CHUNKS_TO_SIDE = 2

biomes = {}
structures = {}
blocks = {}
block_images = {}
block_icons = {}
block_mappings = {}
id_mappings = {}
items = {}

def load_data():
    load_biomes()
    load_structures()
    load_items()
    load_blocks()
    Images.load_images()

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

def load_items():
    items_file = open("items.json", "r")
    global items
    items = json.load(items_file)
    items_file.close()
    for itemname in items.keys():
        item = items[itemname]
        item["can_place"] = False
        if "class" not in item.keys():
            item["class"] = "ItemStack"

def load_blocks():
    blocks_file = open("blocks.json", "r")
    global blocks
    blocks = json.load(blocks_file)["blocks"]
    blocks_file.close()
    
    water_image = pygame.image.load("img/water.png")
    st_water_image = water_image.copy()
    st_water_image.set_alpha(128)
    pygame.display.set_icon(water_image) #TODO change the icon to something better
    
    bid = 0
    global block_images
    block_images = {False:{}, True:{}}
    global block_icons
    block_icons = {False:{}, True:{}}
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
        if "item" not in block.keys():
            block["item"] = "ItemStack"
        if "description" not in block.keys():
            block["description"] = ""
        if "harvestlevel" not in block.keys():
            block["harvestlevel"] = 0
        if "breaktime" not in block.keys():
            block["breaktime"] = 100
        #add an id to the block
        block["id"] = bid
        global block_mappings
        block_mappings[block["name"]] = bid
        global id_mappings
        id_mappings[bid] = block["name"]
        
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
            surf = pygame.transform.scale(blockimg, (blockimg.get_width() * Game.SCALE, blockimg.get_height() * Game.SCALE))
            block_images[False][bid] = surf
            #blit the image onto the water tile so it isn't just empty transparency
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
        #make the corresponding item
        items[block["name"]] = {"displayName": block["displayName"],
                                "image": block["image"],
                                "class": block["item"],
                                "description": block["description"],
                                "can_place": True}
        bid += 1
    block_images[False][get_block_id("water")] = pygame.Surface((Game.BLOCK_SIZE, Game.BLOCK_SIZE), pygame.SRCALPHA, 32)

def get_block_id(blockname):
    return block_mappings[blockname]

def get_id_name(blockid):
    return id_mappings[blockid]

def get_block(blockname):
    return blocks[get_block_id(blockname)]

def get_block_from_id(blockid):
    return blocks[blockid]

class World(object):
    
    def __init__(self, name, player):
        self.name = name
        self.dir = "dat/" + self.name
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.player = player
        path = self.dir + "/state"
        if os.path.isfile(path):
            self.load_state(path)
        else:
            random.seed(self.name)
            self.generate_spawn()
        self.breaking_blocks = {True: [], False: []}
    
    def update(self):
        for x in range(self.loaded_chunks.first, self.loaded_chunks.end):
            chunk = self.loaded_chunks.get(x)
            for entity in chunk.entities:
                entity.update(self)
                if Convert.world_to_chunk(entity.pos[0])[1] != chunk.x and self.loaded_chunks.contains_index(Convert.world_to_chunk(entity.pos[0])[1]):
                    print("Moving", entity, entity.pos, "from", chunk)
                    chunk.entities.remove(entity)
                    self.loaded_chunks.get(Convert.world_to_chunk(entity.pos[0])[1]).entities.append(entity)
        for layer in [True, False]:
            blocks_to_remove = []
            for breaking_block in self.breaking_blocks[layer]:
                breaking_block["progress"] -= 1
                if breaking_block["progress"] <= 0:
                    blocks_to_remove.append(breaking_block)
            for b in blocks_to_remove:
                self.breaking_blocks[layer].remove(b)
    
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
    
    #def load_chunks(self, center):
    #    t = threading.Thread(target=self.load_chunks_in_background, args=[center])
    #    t.start()
    
    def render(self, screen, viewport, background):
        for chunk in self.loaded_chunks.elements:
            chunk.render_blocks(screen, viewport, background)
            if not background:
                chunk.render_entities(screen, viewport, background)
    
    def render_breaks(self, screen, viewport, background):
        for breaking_block in self.breaking_blocks[background]:
            break_index = int(breaking_block["progress"] / breaking_block["breaktime"] * Game.BREAK_LENGTH)
            breakimg = Images.break_images[break_index].copy()
            blockimg = block_images[False][get_block_id(breaking_block["name"])] #TODO make this support CTM
            mask = pygame.mask.from_surface(blockimg)
            olist = mask.outline()
            polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
            pygame.draw.polygon(polysurface, Game.WHITE, olist, 0)
            breakimg.blit(polysurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(breakimg, Convert.world_to_viewport(breaking_block["pos"], viewport))
    
    def get_block_render(self, block_id, block_pos, connected, background, backgroundCTM=False):
        if connected:
            #check adjacent tiles
            left_block = get_block(self.get_block_at((block_pos[0] - 1, block_pos[1]), background))["solid"]
            right_block = get_block(self.get_block_at((block_pos[0] + 1, block_pos[1]), background))["solid"]
            top_block = get_block(self.get_block_at((block_pos[0], block_pos[1] - 1), background))["solid"]
            bottom_block = get_block(self.get_block_at((block_pos[0], block_pos[1] + 1), background))["solid"]
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
            surf = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE)).convert_alpha()
            surf.fill((0, 0, 0, 0))
            surf.blit(block_images[background and not backgroundCTM][block_id], (0, 0),
                        pygame.Rect((tile[0] * Game.BLOCK_SIZE * Game.SCALE, tile[1] * Game.BLOCK_SIZE * Game.SCALE),
                                    (Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE)))
            return surf
        else:
            return block_images[background][block_id] 
    
    def render_block(self, block_id, block_pos, connected, screen, viewport, background):
        screen.blit(self.get_block_render(block_id, block_pos, connected, background), Convert.world_to_viewport(block_pos, viewport))
    
    def save_chunk_in_background(self, chunk):
        chunkfile = open(self.dir + "/chunk" + str(chunk.x) + "data", "wb")
        pickle.dump(chunk, chunkfile)
        chunkfile.close()
    
    def save_chunk(self, chunk):
        t = threading.Thread(target=self.save_chunk_in_background, args=[chunk])
        t.start()
    
    def save_all(self):
        for chunk in self.loaded_chunks.elements:
            self.save_chunk(chunk)
        self.save_state()
    
    def save_state(self):
        save_data = {"player_pos": self.player.pos, 
                     "player_inventory": self.player.inventory,
                     "hotbar_slot": self.player.selected_slot}
        #more game state data
        savefile = open(self.dir + "/state", "wb")
        pickle.dump(save_data, savefile)
        savefile.close()
    
    def load_state(self, path):
        savefile = open(path, "rb")
        save_data = pickle.load(savefile)
        savefile.close()
        self.player.set_pos(save_data["player_pos"])
        player_chunk = Convert.world_to_chunk(self.player.pos[0])[1]
        self.loaded_chunks = TwoWayList.TwoWayList()
        self.load_chunks(player_chunk)
        self.player.inventory = save_data["player_inventory"]
        for row in self.player.inventory:
            for item in row:
                if item is not None:
                    item.load_image()
        self.player.selected_slot = save_data["hotbar_slot"]
    
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