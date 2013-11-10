import random
import Game
import Convert
import World
import Block

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
                newpoints.append(lst[i])
                newpoints.append(midpoint)
            newpoints.append(lst[-1]) #add the last point which wasn't counted
            lst = newpoints
        return lst
    
    def populate(self):
        for y in range(len(self.blocks)):
            for x in range(len(self.blocks[y])):
                if y < World.SEA_LEVEL:
                    self.blocks[y][x] = Block.Block(Block.AIR)
                elif y < self.heights[x]:
                    self.blocks[y][x] = Block.Block(Block.WATER)
                else:
                    self.blocks[y][x] = Block.Block(Block.DIRT)
        self.decorate()
    
    def decorate(self):
        for x in range(WIDTH):
            for structure in self.biome["structures"]:
                if random.random() < structure["frequency"]:
                    #create that structure at x
                    break
        
    def render(self, screen, viewport):
        top = max(Convert.pixel_to_world(viewport.y), 0)
        bottom = min(Convert.pixel_to_world(viewport.y + viewport.height) + 1, World.HEIGHT)
        for blocky in range(top, bottom):
            for blockx in range(WIDTH):
                self.blocks[blocky][blockx].render(screen, Convert.world_to_viewport([Convert.chunk_to_world(blockx, self), blocky], viewport))
        for entity in self.entities:
            entity.render(screen, Convert.world_to_viewport([Convert.chunk_to_world(entity.pos[0], self), entity.pos[1]], viewport))
    
    def __str__(self):
        return "Chunk at x=" + str(self.x) + " contains entities " + str(self.entities)

if __name__ == "__main__":
    Game.main()