import importlib
import random
import json
import Game
import Convert
import World

WIDTH = 16
LEFT = False
RIGHT = True

class Chunk(object):
    def __init__(self):
        self.heights = [0] * WIDTH
        self.foreground_blocks = [[0] * WIDTH for _ in range(World.HEIGHT)]
        self.background_blocks = [[0] * WIDTH for _ in range(World.HEIGHT)]
        self.entities = []
    
    def generate_spawn(self):
        self.x = 0
        self.biome = World.biomes["default"] #this works
        self.generate_spawn_heights()
        self.populate()
    
    def generate_spawn_heights(self):
        self.heights = [144] * WIDTH
    
    def generate_from_chunk(self, chunk, sidegenerated):
        if sidegenerated == LEFT:
            self.x = chunk.x + 1
            sideheight = chunk.heights[WIDTH - 1]
        else:
            self.x = chunk.x - 1
            sideheight = chunk.heights[0]
        if random.random() > chunk.biome["size"]:
            biomes_wanted = []
            for biome in World.biomes:
                if World.biomes[biome]["maxelevation"] <= sideheight <= World.biomes[biome]["minelevation"]:
                    biomes_wanted.append(World.biomes[biome])
            self.biome = biomes_wanted[random.randrange(len(biomes_wanted))] #select random from biomes_wanted
        else:
            self.biome = chunk.biome
        self.generate_heights_from_chunk(chunk, sidegenerated)
        self.populate()
    
    def generate_heights_from_chunk(self, chunk, sidegenerated):
        displace = self.biome["displacement"]
        floor = self.biome["maxelevation"]
        ceiling = self.biome["minelevation"]
        tempheights = [0, 0]
        if sidegenerated == LEFT:
            #Pre-existing chunk is on the left side
            lefth = int(chunk.heights[WIDTH - 1])
            righth = random.randint(lefth - self.biome["slope"], lefth + self.biome["slope"])
            righth = min(righth, ceiling)
            righth = max(righth, floor)
        else:
            #Pre-existing chunk is on the right side
            righth = int(chunk.heights[0])
            lefth = random.randint(righth - self.biome["slope"], righth + self.biome["slope"])
            lefth = min(lefth, ceiling)
            lefth = max(lefth, floor)
        tempheights[0] = lefth
        tempheights[1] = righth
        
        #Midpoint Displacement Algorithm
        while len(tempheights) < WIDTH:
            newpoints = []
            for i in range(len(tempheights) - 1):
                midpoint = (tempheights[i] + tempheights[i + 1]) / 2
                midpoint += random.randint(-int(displace), int(displace))
                midpoint = min(midpoint, ceiling)
                midpoint = max(midpoint, floor)
                displace /= 2
                newpoints.append(int(tempheights[i]))
                newpoints.append(int(midpoint))
            newpoints.append(int(tempheights[-1])) #add the last point which wasn't counted
            tempheights = newpoints
        self.heights = tempheights
    
    def midpoint_displace(self, lst):
        displace = self.biome["displacement"]
        floor = self.biome["maxelevation"]
        ceiling = self.biome["minelevation"]
        while len(lst) < WIDTH:
            newpoints = []
            for i in range(len(lst) - 1):
                midpoint = (lst[i] + lst[i + 1]) / 2
                midpoint += random.randint(-int(displace), int(displace))
                midpoint = min(midpoint, ceiling)
                midpoint = max(midpoint, floor)
                displace /= 2
                newpoints.append(int(lst[i]))
                newpoints.append(int(midpoint))
            newpoints.append(int(lst[-1])) #add the last point which wasn't counted
            lst = newpoints
        return lst
    
    def populate(self):
        #Fill in blocks based on heights
        for y in range(len(self.foreground_blocks)):
            for x in range(len(self.foreground_blocks[y])):
                surface_depth = self.heights[x] + 2 + random.randrange(4)
                if y < World.SEA_LEVEL:
                    self.set_blocks_at(x, y, World.get_block("air"))
                elif y < self.heights[x]:
                    self.set_blocks_at(x, y, World.get_block("water"))
                elif y < surface_depth:
                    self.set_blocks_at(x, y, World.get_block(self.biome["surface"]))
                else:
                    self.set_blocks_at(x, y, World.get_block(self.biome["base"]))
        self.decorate()
    
    def decorate(self):
        #TODO caves, ore
        for x in range(WIDTH):
            for structure_name in self.biome["structures"]:
                structure = World.structures[structure_name]
                if random.random() < structure["frequency"]:
                    self.generate_structure(structure, x)
                    break #can only have one structure at a given x
    
    def generate_structure(self, structure, x):
        #TODO add background blocks defined separately
        if structure["type"] == "column":
            height = random.randint(structure["minheight"], structure["maxheight"])
            for y in range(self.heights[x] - height, self.heights[x]):
                self.set_block_at(x, y, World.get_block(structure["block"]), False)
        elif structure["type"] == "json":
            structure_file = open(structure["location"])
            structure_json = json.load(structure_file)
            curr_y = self.heights[x] - len(structure_json["shape"])
            for line in structure_json["shape"]:
                curr_world_x = Convert.chunk_to_world(x, self)
                for char in line:
                    #find the right chunk
                    chunk = self #world.chunks[Convert.world_to_chunk(x)[1]]- can't really do this...
                    curr_chunk_x = Convert.world_to_chunk(curr_world_x)[0]
                    if curr_chunk_x < WIDTH:
                        if char == " ":
                            block_name = "water"
                        else:
                            block_name = structure_json["blocks"][char]
                        block = World.get_block(block_name)
                        #TODO add background
                        chunk.set_block_at(curr_chunk_x, curr_y, block, False)
                        if block["entity"] is not "":
                            EntityClass = getattr(importlib.import_module(block["entity"]), block["entity"])
                            instance = EntityClass([curr_world_x, curr_y], "")
                            chunk.entities.append(instance)
                    curr_world_x += 1
                curr_y += 1
            structure_file.close()
        elif structure["type"] == "singleblock":
            self.set_block_at(x, self.heights[x] - 1, World.get_block(structure["block"]), False)
    
    def get_block_at(self, x, y, background):
        if background:
            return self.background_blocks[y][x]
        else:
            return self.foreground_blocks[y][x]
    
    def set_blocks_at(self, x, y, block):
        self.set_block_at(x, y, block, True)
        self.set_block_at(x, y, block, False)
    
    def set_block_at(self, x, y, block, background):
        if background:
            self.background_blocks[y][x] = block["id"]
        else:
            self.foreground_blocks[y][x] = block["id"]
    
    def render_blocks(self, screen, viewport, background):
        top = max(Convert.pixel_to_world(viewport.y), 0)
        bottom = min(Convert.pixel_to_world(viewport.y + viewport.height) + 1, World.HEIGHT)
        for blocky in range(top, bottom):
            leftData = Convert.pixel_to_chunk(viewport.x)
            rightData = Convert.pixel_to_chunk(viewport.x + viewport.width)
            if leftData[1] == self.x:
                for blockx in range(leftData[0], WIDTH):
                    self.render_block(blockx, blocky, screen, viewport, background)
            elif leftData[1] < self.x < rightData[1]:
                for blockx in range(WIDTH):
                    self.render_block(blockx, blocky, screen, viewport, background)
            elif self.x == rightData[1]:
                for blockx in range(0, rightData[0] + 1):
                    self.render_block(blockx, blocky, screen, viewport, background)
    
    def render_entities(self, screen, viewport, background):
        for entity in self.entities:
            entity.render(screen, Convert.world_to_viewport(entity.pos, viewport))
    
    def render_block(self, x, y, screen, viewport, background):
        #don't render air
        if background:
            block = World.blocks[self.background_blocks[y][x]]
        else:
            block = World.blocks[self.foreground_blocks[y][x]]
        if block["name"] != "air":
            Game.get_world().render_block(block["id"], [Convert.chunk_to_world(x, self), y], block["connectedTexture"], screen, viewport, background)
        #if Game.DEBUG:
            #draw bounding box- this is really slow for some reason
        #    pygame.draw.rect(screen, Game.BLACK, pygame.Rect(Convert.chunk_to_viewport(pos, self, viewport), (Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE)), 1)
    
    def __str__(self):
        return "Chunk at x=" + str(self.x) + " contains entities " + str(self.entities)

if __name__ == "__main__":
    Game.main()