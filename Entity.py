import math
import pygame
import Game
import Convert
import Chunk
import World
import Images

class Entity(object):
    
    def __init__(self, pos, imageurl, background=False):
        self.imageurl = imageurl
        self.load_image()
        self.set_pos(pos)
        self.move_dir = [0, 0] #direction: -1, 0, 1
        self.vel = [0, 0] #speeds: any numbers
        self.facing = Game.LEFT
        self.background = background
    
    def load_image(self):
        self.img = Images.load_imageurl(self.imageurl)
    
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
                check_block = World.get_block(chunk.get_block_at(block_x, block_y, self.background))
                if check_block["solid"] and self.collides([Convert.chunk_to_world(block_x, chunk), block_y]):
                    #found a collision! 
                    self.pos[index] = old_pos[index]
                    return True
        return False
    
    def tentative_move(self, world, old_pos, index):
        if self.vel[index] == 0:
            #don't do the collision stuff if we don't have to- this "fixes" a chunkloading bug
            #just clamp to scaled pixel position
            world_pos = Convert.world_to_pixel(self.pos[index])
            pixel_pos = world_pos / Game.SCALE
            #prevent clipping left into block
            clamped_pixel_pos = math.ceil(pixel_pos) if self.facing == Game.LEFT else math.floor(pixel_pos)
            block_pos = clamped_pixel_pos / Game.BLOCK_SIZE
            self.pos[index] = block_pos
            return
        
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
        if chunk_left == chunk_right and world.is_loaded_chunk(chunk_left):
            chunk = world.loaded_chunks.get(chunk_left)
            col1 = self.check_collision(chunk, block_left, block_right, block_top, block_bottom, old_pos, index)
        else:
            #need to check from block_left in chunk_left to block_right in chunk_right and all the blocks in any chunks between them
            if world.is_loaded_chunk(chunk_left):
                chunk = world.loaded_chunks.get(chunk_left)
                col2 = self.check_collision(chunk, block_left, Chunk.WIDTH, block_top, block_bottom, old_pos, index)
            for c in range(chunk_left + 1, chunk_right):
                if world.is_loaded_chunk(c):
                    chunk = world.loaded_chunks.get(c)
                    col3 = self.check_collision(chunk, 0, Chunk.WIDTH, block_top, block_bottom, old_pos, index)
            if world.is_loaded_chunk(chunk_right):
                chunk = world.loaded_chunks.get(chunk_right)
                col4 = self.check_collision(chunk, 0, block_right, block_top, block_bottom, old_pos, index)
        if col1 or col2 or col3 or col4:
            self.vel[index] = 0
        if index == 0:
            self.bounding_box.x = Convert.world_to_pixel(self.pos[index])
        else:
            self.bounding_box.y = Convert.world_to_pixel(self.pos[index])
        
        if self.move_dir[0] == -1:
            self.facing = Game.LEFT
        elif self.move_dir[0] == 1:
            self.facing = Game.RIGHT
    
    def entity_collisions(self, world):
        entities = world.get_nearby_entities(Convert.world_to_chunk(self.pos[0])[1])
        for entity in entities:
            if(self.bounding_box.colliderect(entity.bounding_box)):
                self.collide_with(entity, world)
    
    def collide_with(self, entity, world):
        pass
    
    def interact(self, player, item):
        #Used for when the player right-clicks this entity with a block.
        #Return false if the player should continue to use their held item after calling this, true otherwise.
        return False
    
    def update(self, world):
        old_pos = [self.pos[0], self.pos[1]]
        self.tentative_move(world, old_pos, 0)
        self.tentative_move(world, old_pos, 1)
        self.entity_collisions(world)
    
    def set_pos(self, pos):
        self.pos = pos
        #bounding box is in pixels because it can only have ints
        if self.img is None:
            self.bounding_box = pygame.Rect(Convert.world_to_pixel(pos[0]), Convert.world_to_pixel(pos[1]), Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE)
            self.width = 1
            self.height = 1
        else:
            self.bounding_box = pygame.Rect(Convert.world_to_pixel(pos[0]), Convert.world_to_pixel(pos[1]), self.img.get_width(), self.img.get_height())
            self.width = Convert.pixel_to_world_ceil(self.img.get_width())
            self.height = Convert.pixel_to_world_ceil(self.img.get_height())
    
    def render(self, screen, pos):
        if Game.DEBUG:
            #draw bounding rect
            pygame.draw.rect(screen, Game.BLACK, 
                             pygame.rect.Rect(Convert.pixels_to_viewport(self.bounding_box.topleft, Game.get_viewport()), 
                                              (self.bounding_box.width, self.bounding_box.height)), 1)
        
        if self.img is not None:
            screen.blit(self.img, pos)
    
    def __str__(self):
        return str(self.__class__.__name__) + " at " + str(self.pos)