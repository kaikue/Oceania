import random
import convert
import world
import block

WIDTH = 16
LEFT = False
RIGHT = True
MAX_SLOPE = 32

class Chunk(object):
    def __init__(self):
        self.heights = [0] * WIDTH
        self.blocks = [[0] * WIDTH for _ in range(world.HEIGHT)]
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
                if y < world.SEA_LEVEL:
                    self.blocks[y][x] = block.Block(block.AIR)
                elif y < self.heights[x]:
                    self.blocks[y][x] = block.Block(block.WATER)
                else:
                    self.blocks[y][x] = block.Block(block.DIRT)
    
    def render(self, screen, viewport):
        #print("P:", viewport.x, viewport.y)
        viewport_y1 = convert.y_pixels_to_world(viewport.y)
        viewport_y2 = convert.y_pixels_to_world(viewport.y + viewport.width)
        #print("W:", viewport_y1, viewport_y2)
        print("Rendering chunk " + str(self.x) + " to " + str(convert.world_to_viewport([convert.chunk_to_world(0, self), 0], viewport)))
        for blocky in range(viewport_y1, viewport_y2):
            for blockx in range(WIDTH):
                self.blocks[blocky][blockx].render(screen, convert.world_to_viewport([convert.chunk_to_world(blockx, self), blocky], viewport))
        for entity in self.entities:
            entity.render(screen, convert.world_to_viewport([convert.chunk_to_world(entity.pos[0], self), entity.pos[1]], viewport))
            #entity.render(screen, (self.x * entity.x - viewport.x, self.x * entity.y - viewport.y))
        
        """
        print(viewport.x, viewport.y)
        viewport_blocks = convert.pixels_to_world([viewport.x, viewport.y])
        blocky = viewport.y // block.SIZE
        for drawy in range(0, viewport.height, block.SIZE):
            drawx = self.x * block.SIZE - viewport.x
            for blockx in range(WIDTH):
                self.blocks[blocky][blockx].render(screen, (drawx, drawy))
                #pos = font.render(str(blockx) + " " + str(blocky), 0, (0, 0, 0))
                #if blockx % 8 == 0 and blocky % 8 == 0:
                #    screen.blit(pos, (drawx, drawy))
                drawx += block.SIZE
            blocky += 1
        """