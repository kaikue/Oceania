import random
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
        #g = self.midpoint_displace([0, 0])
        #print(g, len(g))
        self.generate_spawn_heights()
        self.generate_blocks()
    
    def generate_spawn_heights(self):
        self.heights = [196] * WIDTH
    
    def generate_from_chunk(self, chunk, sidegenerated):
        if sidegenerated == LEFT:
            self.x = chunk.x + 1
        else:
            self.x = chunk.x - 1
        self.generate_heights_from_chunk(chunk, sidegenerated)
        self.generate_blocks()
    
    def generate_heights_from_chunk(self, chunk, sidegenerated):
        #tempheights = [0] * WIDTH
        tempheights = [0, 0]
        if sidegenerated == LEFT:
            #generate with left start
            leftx = int(chunk.heights[WIDTH - 1])
            tempheights[0] = leftx
            tempheights[1] = random.randint(leftx - MAX_SLOPE, leftx + MAX_SLOPE) #WIDTH - 1
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
    
    def generate_blocks(self):
        for y in range(len(self.blocks)):
            for x in range(len(self.blocks[y])):
                if y < World.SEA_LEVEL:
                    self.blocks[y][x] = Block.Block(Block.AIR)
                elif y < self.heights[x]:
                    self.blocks[y][x] = Block.Block(Block.WATER)
                else:
                    self.blocks[y][x] = Block.Block(Block.DIRT)
    
    def render(self, screen, viewport):
        viewport_y1 = Convert.pixel_to_world(viewport.y)
        viewport_y2 = Convert.pixel_to_world(viewport.y + viewport.width)
        for blocky in range(viewport_y1, viewport_y2):
            if blocky < 0 or blocky > World.HEIGHT:
                continue
            for blockx in range(WIDTH):
                self.blocks[blocky][blockx].render(screen, Convert.world_to_viewport([Convert.chunk_to_world(blockx, self), blocky], viewport))
        for entity in self.entities:
            entity.render(screen, Convert.world_to_viewport([Convert.chunk_to_world(entity.pos[0], self), entity.pos[1]], viewport))
