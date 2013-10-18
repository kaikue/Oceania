import pygame
import Convert
import Chunk

class Entity(object):
    
    def __init__(self, pos, imageurl):
        self.pos = pos
        self.img = pygame.image.load(imageurl).convert_alpha()
        #bounding box is in pixels because it can only have ints
        self.bounding_box = pygame.Rect(Convert.world_to_pixel(pos[0]), Convert.world_to_pixel(pos[1]), self.img.get_width(), self.img.get_height())
        self.width = Convert.pixel_to_world(self.img.get_width()) + 1
        self.height = Convert.pixel_to_world(self.img.get_height()) + 1
        self.dir = [0, 0] #direction: -1, 0, 1
        self.vel = [0, 0] #speeds: any numbers
    
    def collides(self, block_pos):
        return self.bounding_box.colliderect(pygame.Rect(Convert.world_to_pixel(block_pos[0]), Convert.world_to_pixel(block_pos[1]), Convert.world_to_pixel(1), Convert.world_to_pixel(1)))
    
    def check_collision(self, chunk, left, right, top, bottom, old_pos, index):
        for block_x in range(left, right):
            for block_y in range(top, bottom):
                check_block = chunk.blocks[block_y][block_x]
                if check_block.is_solid() and self.collides([Convert.chunk_to_world(block_x, chunk), block_y]):
                    #found a collision! 
                    self.pos[index] = old_pos[index]
                    return
    
    def update(self, world):
        old_pos = [self.pos[0], self.pos[1]]
        self.pos[0] += self.vel[0]
        self.bounding_box.x = Convert.world_to_pixel(self.pos[0])
        block_left = int(Convert.world_to_chunk(self.pos[0])[0])
        chunk_left = Convert.world_to_chunk(self.pos[0])[1]
        block_right = int(Convert.world_to_chunk(self.pos[0] + self.width)[0]) + 1
        chunk_right = Convert.world_to_chunk(self.pos[0] + self.width)[1]
        block_top = int(self.pos[1])
        block_bottom = int(self.pos[1] + self.height) + 1
        if chunk_left == chunk_right:
            chunk = world.chunks.get(chunk_left)
            self.check_collision(chunk, block_left, block_right, block_top, block_bottom, old_pos, 0)
        else:
            chunk = world.chunks.get(chunk_left)
            self.check_collision(chunk, block_left, Chunk.WIDTH, block_top, block_bottom, old_pos, 0)
            for c in range(chunk_left + 1, chunk_right):
                chunk = world.chunks.get(c)
                self.check_collision(chunk, 0, Chunk.WIDTH, block_top, block_bottom, old_pos, 0)
            chunk = world.chunks.get(chunk_right)
            self.check_collision(chunk, 0, block_right, block_top, block_bottom, old_pos, 0)
        self.bounding_box.x = Convert.world_to_pixel(self.pos[0])
        
        self.pos[1] += self.vel[1]
        self.bounding_box.y = Convert.world_to_pixel(self.pos[1])
        block_left = int(Convert.world_to_chunk(self.pos[0])[0])
        chunk_left = Convert.world_to_chunk(self.pos[0])[1]
        block_right = int(Convert.world_to_chunk(self.pos[0] + self.width)[0]) + 1
        chunk_right = Convert.world_to_chunk(self.pos[0] + self.width)[1]
        block_top = int(self.pos[1])
        block_bottom = int(self.pos[1] + self.height) + 1
        if chunk_left == chunk_right:
            chunk = world.chunks.get(chunk_left)
            self.check_collision(chunk, block_left, block_right, block_top, block_bottom, old_pos, 1)
        else:
            chunk = world.chunks.get(chunk_left)
            self.check_collision(chunk, block_left, Chunk.WIDTH, block_top, block_bottom, old_pos, 1)
            for c in range(chunk_left + 1, chunk_right):
                chunk = world.chunks.get(c)
                self.check_collision(chunk, 0, Chunk.WIDTH, block_top, block_bottom, old_pos, 1)
            chunk = world.chunks.get(chunk_right)
            self.check_collision(chunk, 0, block_right, block_top, block_bottom, old_pos, 1)
        self.bounding_box.y = Convert.world_to_pixel(self.pos[1])
    
    def render(self, screen, pos):
        screen.blit(self.img, pos)