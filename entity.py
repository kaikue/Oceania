import pygame
import convert
import chunk

class Entity(object):
    
    def __init__(self, pos, imageurl):
        self.pos = pos
        self.img = pygame.image.load(imageurl).convert_alpha()
        #bounding box is in pixels because it can only have ints
        self.bounding_box = pygame.Rect(convert.world_to_pixel(pos[0]), convert.world_to_pixel(pos[1]), self.img.get_width(), self.img.get_height())
        self.width = convert.pixel_to_world(self.img.get_width()) + 1
        self.height = convert.pixel_to_world(self.img.get_height()) + 1
        #print(self.img.get_width(), convert.pixel_to_world(self.img.get_width()))
        self.dir = [0, 0] #direction: -1, 0, 1
        self.vel = [0, 0] #speeds: any numbers
    
    def collides(self, block_pos):
        return self.bounding_box.colliderect(pygame.Rect(convert.world_to_pixel(block_pos[0]), convert.world_to_pixel(block_pos[1]), convert.world_to_pixel(1), convert.world_to_pixel(1)))
    
    def check_collision(self, check_chunk, left, right, top, bottom, old_pos, index):
        for block_x in range(left, right):
            for block_y in range(top, bottom):
                check_block = check_chunk.blocks[block_y][block_x]
                #print("Checking", block_x, block_y, check_block.is_solid())
                if check_block.is_solid() and self.collides([convert.chunk_to_world(block_x, check_chunk), block_y]): 
                    self.pos[index] = old_pos[index]
                    #print("3a) Found collision while checking", left, right, top, bottom)
                    #print("3b) Resetting", index, "with block", block_x, block_y, "to pos", old_pos)
                    #sys.exit(0)
                    return
    
    def update(self, world):
        old_pos = [self.pos[0], self.pos[1]]
        self.pos[0] += self.vel[0]
        self.bounding_box.x = convert.world_to_pixel(self.pos[0])
        block_left = int(convert.world_to_chunk(self.pos[0])[0])
        chunk_left = convert.world_to_chunk(self.pos[0])[1]
        block_right = int(convert.world_to_chunk(self.pos[0] + self.width)[0]) + 1
        chunk_right = convert.world_to_chunk(self.pos[0] + self.width)[1]
        block_top = int(self.pos[1])
        block_bottom = int(self.pos[1] + self.height) + 1
        if chunk_left == chunk_right:
            print("[x] One chunk:", chunk_left)
            check_chunk = world.chunks.get(chunk_left)
            self.check_collision(check_chunk, block_left, block_right, block_top, block_bottom, old_pos, 0)
        else:
            print("[x] Multiple chunks:", chunk_left, "to", chunk_right)
            check_chunk = world.chunks.get(chunk_left)
            self.check_collision(check_chunk, block_left, chunk.WIDTH, block_top, block_bottom, old_pos, 0)
            for c in range(chunk_left + 1, chunk_right):
                check_chunk = world.chunks.get(c)
                self.check_collision(check_chunk, 0, chunk.WIDTH, block_top, block_bottom, old_pos, 0)
            check_chunk = world.chunks.get(chunk_right)
            self.check_collision(check_chunk, 0, block_right, block_top, block_bottom, old_pos, 0)
        
        self.pos[1] += self.vel[1]
        self.bounding_box.y = convert.world_to_pixel(self.pos[1])
        #print("1) OLD POS:", old_pos, "NEW POS:", self.pos)
        block_left = int(convert.world_to_chunk(self.pos[0])[0])
        chunk_left = convert.world_to_chunk(self.pos[0])[1]
        block_right = int(convert.world_to_chunk(self.pos[0] + self.width)[0]) + 1
        chunk_right = convert.world_to_chunk(self.pos[0] + self.width)[1]
        block_top = int(self.pos[1])
        block_bottom = int(self.pos[1] + self.height) + 1
        if chunk_left == chunk_right:
            #print("2) [y] One chunk:", chunk_left)
            check_chunk = world.chunks.get(chunk_left)
            self.check_collision(check_chunk, block_left, block_right, block_top, block_bottom, old_pos, 1)
        else:
            #print("2) [y] Multiple chunks:", chunk_left, "to", chunk_right)
            check_chunk = world.chunks.get(chunk_left)
            self.check_collision(check_chunk, block_left, chunk.WIDTH, block_top, block_bottom, old_pos, 1)
            for c in range(chunk_left + 1, chunk_right):
                check_chunk = world.chunks.get(c)
                self.check_collision(check_chunk, 0, chunk.WIDTH, block_top, block_bottom, old_pos, 1)
            check_chunk = world.chunks.get(chunk_right)
            self.check_collision(check_chunk, 0, block_right, block_top, block_bottom, old_pos, 1)
        #print("4) Moved from", old_pos, "to", self.pos)
        self.bounding_box.x = convert.world_to_pixel(self.pos[0])
        self.bounding_box.y = convert.world_to_pixel(self.pos[1])
        #print("5) Bounding box", self.bounding_box)
    
    def render(self, screen, pos):
        screen.blit(self.img, pos)