import os
import threading
import pickle
import json
import pygame
import Game
import Player
import Convert
import Chunk
import TwoWayList
import Images
import Generate

HEIGHT = 256
SEA_LEVEL = HEIGHT / 4
SEA_FLOOR = HEIGHT * 3 / 4
CHUNKS_TO_SIDE = 2

CTM_POSITIONS = \
    {
        False: {False: 0, True:  1},
        True:  {True:  2, False: 3}
    }

biomes = {}
structures = {}
blocks = {}
block_images = {} #False:{foreground block ids to image}, True:{background block ids to image}
ctm_block_images = {}
item_images = {} #[normal, flipped horizontal, rotated 90 degrees CCW, rotated 90 degrees CCW and flipped horizontal, flipped horizontal and vertical]
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
        if isinstance(item["description"], str):
            item["description"] = [item["description"]]
        img = Images.load_imageurl(item["image"])
        
        img_rotated = Images.rotate(img, 90)
        item_images[itemname] = [img,
                                Images.flip_horizontal(img),
                                img_rotated,
                                Images.flip_horizontal(img_rotated),
                                Images.flip_completely(img)]

def load_blocks():
    blocks_file = open("blocks.json", "r")
    global blocks
    blocks = json.load(blocks_file)["blocks"]
    blocks_file.close()
    
    water_image = pygame.image.load("img/water.png")
    st_water_image = water_image.copy()
    st_water_image.set_alpha(128)
    pygame.display.set_icon(water_image) #TO DO: change the icon to something better
    
    bid = 0
    global block_images
    block_images = {False:{}, True:{}}
    global ctm_block_images
    ctm_block_images = {False:{}, True:{}}
    for block in blocks:
        #set some default attributes
        if "breakable" not in block.keys():
            block["breakable"] = True
        if "connectedTexture" not in block.keys():
            block["connectedTexture"] = None
        if "solid" not in block.keys():
            block["solid"] = True
        if "entity" not in block.keys():
            block["entity"] = ""
        if "item" not in block.keys():
            block["item"] = "ItemStack"
        if "description" not in block.keys():
            block["description"] = [""]
        if "harvestlevel" not in block.keys():
            block["harvestlevel"] = 0
        if "breaktime" not in block.keys():
            block["breaktime"] = 100
        if "image" not in block.keys():
            block["image"] = ""
        #add an id to the block
        block["id"] = bid
        global block_mappings
        block_mappings[block["name"]] = bid
        global id_mappings
        id_mappings[bid] = block["name"]
        
        if isinstance(block["description"], str):
            block["description"] = [block["description"]]
        
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
            item_images[block["name"]] = [Images.make_itemdrop_image(icon)]
            foreground_image = Images.scale(blockimg, Game.SCALE)
            block_images[False][bid] = Images.crop(foreground_image)
            #blit the image onto the water tile so it isn't just empty transparency
            image = blockimg.copy()
            for x in range(image.get_width() // Game.BLOCK_SIZE):
                for y in range(image.get_height() // Game.BLOCK_SIZE):
                    image.blit(water_image, (x * Game.BLOCK_SIZE, y * Game.BLOCK_SIZE))
            image.blit(blockimg, (0, 0))
            for x in range(image.get_width() // Game.BLOCK_SIZE):
                for y in range(image.get_height() // Game.BLOCK_SIZE):
                    image.blit(st_water_image, (x * Game.BLOCK_SIZE, y * Game.BLOCK_SIZE))
            background_image = Images.scale(image, Game.SCALE)
            block_images[True][bid] = background_image
            if block["connectedTexture"]:
                ctm_block_images[False][bid] = {}
                ctm_block_images[True][bid] = {}
                for x in range(4):
                    for y in range(4):
                        foreground_surf = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE)).convert_alpha()
                        foreground_surf.fill((0, 0, 0, 0))
                        background_surf = foreground_surf.copy()
                        foreground_surf.blit(foreground_image, (0, 0),
                            pygame.Rect((x * Game.BLOCK_SIZE * Game.SCALE, y * Game.BLOCK_SIZE * Game.SCALE),
                                 (Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE)))
                        ctm_block_images[False][bid][(x, y)] = foreground_surf
                        background_surf.blit(background_image, (0, 0),
                            pygame.Rect((x * Game.BLOCK_SIZE * Game.SCALE, y * Game.BLOCK_SIZE * Game.SCALE),
                                 (Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE)))
                        ctm_block_images[True][bid][(x, y)] = background_surf
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
    
    def __init__(self, name):
        self.name = name
        self.dir = "dat/" + self.name
        self.breaking_blocks = {True: [], False: []}
    
    def load(self):
        path = self.dir + "/state"
        self.load_state(path)
    
    def generate(self, seed, player_options):
        os.makedirs(self.dir)
        self.player = Player.Player([0, 140], player_options)
        self.seed = seed
        Generate.setup(seed)
        self.generate_spawn()
    
    def update(self):
        for x in range(self.loaded_chunks.first, self.loaded_chunks.end):
            chunk = self.loaded_chunks.get(x)
            for entity in chunk.entities:
                entity.update(self)
                if Convert.world_to_chunk(entity.pos[0])[1] != chunk.x \
                        and self.loaded_chunks.contains_index(Convert.world_to_chunk(entity.pos[0])[1]) \
                        and entity in chunk.entities:
                    chunk.entities.remove(entity)
                    self.create_entity(entity)
        for layer in [True, False]:
            blocks_to_remove = []
            for breaking_block in self.breaking_blocks[layer]:
                breaking_block["progress"] -= 1
                if breaking_block["progress"] <= 0:
                    blocks_to_remove.append(breaking_block)
            for b in blocks_to_remove:
                self.breaking_blocks[layer].remove(b)
    
    def get_block_at(self, world_pos, background):
        chunk = self.loaded_chunks.get(world_pos[0] // Chunk.WIDTH) #Convert.world_to_chunk(world_pos[0])[1]
        x_in_chunk = world_pos[0] % Chunk.WIDTH #Convert.world_to_chunk(world_pos[0])[0]
        return chunk.get_block_at(x_in_chunk, world_pos[1], background)
    
    def get_block_in_chunk(self, world_pos, background, chunk):
        if chunk.x != world_pos[0] // Chunk.WIDTH:
            #wrong chunk
            return self.get_block_at(world_pos, background)
        
        x_in_chunk = world_pos[0] % Chunk.WIDTH
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
            loaded_chunk = None
            for chunk in old_chunks.elements:
                if chunk.x == i:
                    loaded_chunk = chunk
            if loaded_chunk is not None:
                chunk = loaded_chunk
            elif self.chunk_exists(i):
                chunk = self.load_chunk(i)
            else:
                if i < 0:
                    side = Game.RIGHT
                    prev = old_chunks.get(i + 1)
                else:
                    side = Game.LEFT
                    prev = old_chunks.get(i - 1)
                chunk = self.generate_chunk(prev, side)
            self.loaded_chunks.append(chunk)
        self.loaded_chunks.update_start(-leftchunk)
    
    #def load_chunks(self, center):
    #    t = threading.Thread(target=self.load_chunks_in_background, args=[center])
    #    t.start()
    
    def is_loaded_chunk(self, index):
        return self.loaded_chunks.contains_index(index)
    
    def render(self, screen, viewport, background):
        for chunk in self.loaded_chunks.elements:
            chunk.render_blocks(screen, viewport, background)
            if not background:
                chunk.render_entities(screen, viewport, background)
    
    def render_breaks(self, screen, viewport, background):
        for breaking_block in self.breaking_blocks[background]:
            break_index = int(breaking_block["progress"] / breaking_block["breaktime"] * Game.BREAK_LENGTH)
            breakimg = Images.break_images[break_index].copy()
            blockimg = block_images[False][get_block_id(breaking_block["name"])] #TO DO: make this support CTM
            mask = pygame.mask.from_surface(blockimg)
            olist = mask.outline()
            polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
            pygame.draw.polygon(polysurface, Game.WHITE, olist, 0)
            breakimg.blit(polysurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(breakimg, Convert.world_to_viewport(breaking_block["pos"], viewport))
    
    def get_block_render(self, block_id, block_pos, connected, background, chunk, backgroundCTM=False):
        if connected is not None:
            #check adjacent tiles
            if connected == "solid":
                field = "solid"
                val = True
            elif connected == "sametype":
                field = "id"
                val = block_id
            
            left_block = self.block_against(block_pos, -1, 0, background, chunk, field, val)
            right_block = self.block_against(block_pos, 1, 0, background, chunk, field, val)
            top_block = self.block_against(block_pos, 0, -1, background, chunk, field, val)
            bottom_block = self.block_against(block_pos, 0, 1, background, chunk, field, val)
            
            tile = (CTM_POSITIONS[left_block][right_block], CTM_POSITIONS[top_block][bottom_block])
            return ctm_block_images[background and not backgroundCTM][block_id][tile]
        else:
            return block_images[background][block_id] 
    
    def block_against(self, block_pos, x_offset, y_offset, background, chunk, field, val):
        #TO DO: this part is slow
        block = self.get_block_in_chunk((block_pos[0] + x_offset, block_pos[1] + y_offset), background, chunk)
        return get_block(block)[field] == val
    
    def render_block(self, block_id, block_pos, connected, screen, viewport, background, chunk):
        screen.blit(self.get_block_render(block_id, block_pos, connected, background, chunk), Convert.world_to_viewport(block_pos, viewport))
    
    def create_entity(self, entity):
        self.loaded_chunks.get(entity.get_chunk()).entities.append(entity)
    
    def remove_entity(self, entity):
        #TO DO: this may fail
        self.loaded_chunks.get(entity.get_chunk()).entities.remove(entity)
    
    def get_nearby_entities(self, chunk):
        #TO DO: only update once per frame?
        entities = []
        if self.is_loaded_chunk(chunk):
            entities += self.loaded_chunks.get(chunk).entities
        if self.is_loaded_chunk(chunk - 1):
            entities += self.loaded_chunks.get(chunk - 1).entities
        if self.is_loaded_chunk(chunk + 1):
            entities += self.loaded_chunks.get(chunk + 1).entities
        player_chunk = self.player.get_chunk()
        if player_chunk == chunk or player_chunk == chunk - 1 or player_chunk == chunk + 1:
            entities.append(self.player)
        return entities
    
    def save_chunk_in_background(self, chunk):
        chunkfile = open(self.dir + "/chunk" + str(chunk.x) + "data", "wb")
        chunk_data = chunk.save()
        pickle.dump(chunk_data, chunkfile)
        chunkfile.close()
    
    def save_chunk(self, chunk):
        t = threading.Thread(target=self.save_chunk_in_background, args=[chunk])
        t.start()
    
    def save_all(self):
        for chunk in self.loaded_chunks.elements:
            self.save_chunk(chunk)
        self.save_state()
    
    def save_state(self):
        player_data = self.player.save()
        save_data = {"player": player_data, "seed": self.seed}
        #more game state data
        savefile = open(self.dir + "/state", "wb")
        pickle.dump(save_data, savefile)
        savefile.close()
    
    def load_state(self, path):
        savefile = open(path, "rb")
        save_data = pickle.load(savefile)
        savefile.close()
        player_data = save_data["player"]
        self.player = Player.Player([0, 0], (0, 0, 0, 0))
        self.player.load(player_data)
        self.seed = save_data["seed"]
        Generate.setup(self.seed)
        player_chunk = Convert.world_to_chunk(self.player.pos[0])[1]
        self.loaded_chunks = TwoWayList.TwoWayList()
        self.load_chunks(player_chunk)
        self.player.load_image()
        for row in self.player.inventory:
            for item in row:
                if item is not None:
                    item.load_image()
    
    def get_chunk_file(self, index):
        return self.dir + "/chunk" + str(index) + "data"
    
    def chunk_exists(self, index):
        return os.path.isfile(self.get_chunk_file(index))
    
    def load_chunk(self, index):
        chunkfile = open(self.get_chunk_file(index), "rb")
        chunk_data = pickle.load(chunkfile)
        chunk = Chunk.Chunk()
        chunk.load(chunk_data)
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
        r1.generate_from_chunk(spawn, Game.LEFT)
        self.loaded_chunks.append(r1)
        r2 = Chunk.Chunk()
        r2.generate_from_chunk(r1, Game.LEFT)
        self.loaded_chunks.append(r2)
        r1l = Chunk.Chunk()
        r1l.generate_from_chunk(spawn, Game.RIGHT)
        self.loaded_chunks.prepend(r1l)
        r2l = Chunk.Chunk()
        r2l.generate_from_chunk(r1l, Game.RIGHT)
        self.loaded_chunks.prepend(r2l)
        self.save_all()
    
    def generate_chunk(self, basechunk, side):
        chunk = Chunk.Chunk()
        chunk.generate_from_chunk(basechunk, side)
        self.save_chunk(chunk)
        return chunk
    
    def close(self):
        self.save_all()