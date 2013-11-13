import random
import pygame
import Game
import Convert
import World

WIDTH = 16
LEFT = False
RIGHT = True
MAX_SLOPE = 32

class Chunk(object):
    def __init__(self):
        self.heights = [0] * WIDTH
        self.blocks = [[0] * WIDTH for _ in range(World.HEIGHT)]
        self.entities = []
    
    def generate_spawn(self):
        self.x = 0
        self.biome = World.biomes["default"] #this works
        self.generate_spawn_heights()
        self.populate()
    
    def generate_spawn_heights(self):
        self.heights = [196] * WIDTH
    
    def generate_from_chunk(self, chunk, sidegenerated):
        if sidegenerated == LEFT:
            self.x = chunk.x + 1
        else:
            self.x = chunk.x - 1
        self.biome = chunk.biome
        self.generate_heights_from_chunk(chunk, sidegenerated)
        self.populate()
    
    def generate_heights_from_chunk(self, chunk, sidegenerated):
        tempheights = [0, 0]
        if sidegenerated == LEFT:
            #generate with left start
            leftx = int(chunk.heights[WIDTH - 1])
            tempheights[0] = leftx
            tempheights[1] = random.randint(leftx - MAX_SLOPE, leftx + MAX_SLOPE)
        else:
            #generate with right start
            rightx = int(chunk.heights[0])
            tempheights[1] = rightx
            tempheights[0] = random.randint(rightx - MAX_SLOPE, rightx + MAX_SLOPE)
        tempheights = self.midpoint_displace(tempheights)
        self.heights = tempheights
    
    def midpoint_displace(self, lst):
        displace = 8
        #for _ in range(iters):
        while len(lst) < WIDTH:
            newpoints = []
            for i in range(len(lst) - 1):
                midpoint = (lst[i] + lst[i + 1]) / 2
                midpoint += random.randint(-int(displace), int(displace))
                displace /= 2
                newpoints.append(int(lst[i]))
                newpoints.append(int(midpoint))
            newpoints.append(int(lst[-1])) #add the last point which wasn't counted
            lst = newpoints
        return lst
    
    def populate(self):
        for y in range(len(self.blocks)):
            for x in range(len(self.blocks[y])):
                if y < World.SEA_LEVEL:
                    self.blocks[y][x] = World.blocks["air"]
                elif y < self.heights[x]:
                    self.blocks[y][x] = World.blocks["water"]
                else:
                    self.blocks[y][x] = World.blocks["dirt"]
        self.decorate()
    
    def decorate(self):
        for x in range(WIDTH):
            for structure_name in self.biome["structures"]:
                structure = World.structures[structure_name]
                if random.random() < structure["frequency"]:
                    #create that structure at x
                    self.generate_structure(structure, x)
                    break
    
    def generate_structure(self, structure, x):
        if structure["type"] == "column":
            height = random.randint(structure["minheight"], structure["maxheight"])
            for y in range(self.heights[x] - height, self.heights[x]):
                self.blocks[y][x] = World.blocks[structure["block"]]
        elif structure["type"] == "other":
            pass
    
    def render(self, screen, viewport):
        top = max(Convert.pixel_to_world(viewport.y), 0)
        bottom = min(Convert.pixel_to_world(viewport.y + viewport.height) + 1, World.HEIGHT)
        for blocky in range(top, bottom):
            for blockx in range(WIDTH):
                self.render_block(self.blocks[blocky][blockx], screen, Convert.world_to_viewport([Convert.chunk_to_world(blockx, self), blocky], viewport))
        for entity in self.entities:
            entity.render(screen, Convert.world_to_viewport([Convert.chunk_to_world(entity.pos[0], self), entity.pos[1]], viewport))
    
    def render_block(self, block, screen, pos):
        if block["id"] != 0:
            screen.blit(World.block_images[block["id"]], pos)
        if Game.DEBUG:
            #draw bounding box
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pos[0], pos[1], Game.BLOCK_SIZE, Game.BLOCK_SIZE), 1)
    
    def __str__(self):
        return "Chunk at x=" + str(self.x) + " contains entities " + str(self.entities)

if __name__ == "__main__":
    Game.main()