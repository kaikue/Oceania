import math
import pygame
import Game
import Convert
import Chunk
import World

class Entity(object):
    
    def __init__(self, pos, imageurl, scale=()):
        self.pos = pos
        self.imageurl = imageurl
        self.scale = scale
        self.load_image()
        #bounding box is in pixels because it can only have ints
        if self.img is None:
            self.bounding_box = pygame.Rect(Convert.world_to_pixel(pos[0]), Convert.world_to_pixel(pos[1]), Game.BLOCK_SIZE, Game.BLOCK_SIZE)
            self.width = 1
            self.height = 1
        else:
            self.bounding_box = pygame.Rect(Convert.world_to_pixel(pos[0]), Convert.world_to_pixel(pos[1]), self.img.get_width(), self.img.get_height())
            self.width = Convert.pixel_to_world(self.img.get_width()) + 1
            self.height = Convert.pixel_to_world(self.img.get_height()) + 1
        self.dir = [0, 0] #direction: -1, 0, 1
        self.vel = [0, 0] #speeds: any numbers
    
    def load_image(self):
        if self.imageurl is "":
            self.img = None
        else:
            self.img = pygame.image.load(self.imageurl).convert_alpha()
            if self.scale != ():
                self.img = pygame.transform.scale(self.img, (self.scale[0], self.scale[1]))
    
    def pixel_pos(self, centered=False):
        if centered:
            return [self.bounding_box.centerx, self.bounding_box.centery]
        return [self.bounding_box.x, self.bounding_box.y]
    
    def get_chunk(self):
        return Convert.world_to_chunk(self.pos[0])[1] #should be accurate
    
    def collides(self, block_pos):
        return self.bounding_box.colliderect(pygame.Rect(Convert.world_to_pixel(block_pos[0]), Convert.world_to_pixel(block_pos[1]), Convert.world_to_pixel(1), Convert.world_to_pixel(1)))
    
    def check_collision(self, chunk, left, right, top, bottom, old_pos, index):
        for block_x in range(left, right):
            for block_y in range(top, bottom):
                check_block = chunk.get_block_at(block_x, block_y, False) #only check the foreground
                #if check_block.is_solid() and self.collides([Convert.chunk_to_world(block_x, chunk), block_y]):
                if World.blocks[check_block]["solid"] and self.collides([Convert.chunk_to_world(block_x, chunk), block_y]):
                    #found a collision! 
                    self.pos[index] = old_pos[index]
                    return True
        return False
    
    def tentative_move(self, world, old_pos, index):
        self.pos[index] += self.vel[index]
        if index == 0:
            self.bounding_box.x = Convert.world_to_pixel(self.pos[index])
        else:
            self.bounding_box.y = Convert.world_to_pixel(self.pos[index])
        block_left = int(Convert.world_to_chunk(self.pos[0])[0])
        chunk_left = Convert.world_to_chunk(self.pos[0])[1]
        block_right = math.ceil(Convert.world_to_chunk(self.pos[0] + self.width)[0])
        chunk_right = Convert.world_to_chunk(self.pos[0] + self.width)[1]
        block_top = int(self.pos[1])
        block_bottom = math.ceil(self.pos[1] + self.height)
        col1 = col2 = col3 = col4 = False
        if chunk_left == chunk_right:
            chunk = world.loaded_chunks.get(chunk_left)
            col1 = self.check_collision(chunk, block_left, block_right, block_top, block_bottom, old_pos, index)
        else:
            #need to check from block_left in chunk_left to block_right in chunk_right and all the blocks in any chunks between them
            chunk = world.loaded_chunks.get(chunk_left)
            col2 = self.check_collision(chunk, block_left, Chunk.WIDTH, block_top, block_bottom, old_pos, index)
            for c in range(chunk_left + 1, chunk_right):
                chunk = world.loaded_chunks.get(c)
                col3 = self.check_collision(chunk, 0, Chunk.WIDTH, block_top, block_bottom, old_pos, index)
            chunk = world.loaded_chunks.get(chunk_right)
            col4 = self.check_collision(chunk, 0, block_right, block_top, block_bottom, old_pos, index)
        if col1 or col2 or col3 or col4:
            self.vel[index] = 0 #reset acceleration?
        if index == 0:
            self.bounding_box.x = Convert.world_to_pixel(self.pos[index])
        else:
            self.bounding_box.y = Convert.world_to_pixel(self.pos[index])
    
    def entity_collisions(self, world):
        pass
    
    def interact(self, item):
        #Used for when the player right-clicks the entity with a block.
        pass
    
    def update(self, world):
        old_pos = [self.pos[0], self.pos[1]]
        self.tentative_move(world, old_pos, 0)
        self.tentative_move(world, old_pos, 1)
        self.entity_collisions(world)
    
    def render(self, screen, pos):
        if self.img is not None:
            screen.blit(self.img, pos)

if __name__ == "__main__":
    Game.main()