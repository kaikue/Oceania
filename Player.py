import pygame
import Game
import World
import Entity
import Convert
from BlockDrop import BlockDrop
from ItemStack import ItemStack

MAX_STACK_SIZE = 100
BREAK_DIST = 48

class Player(Entity.Entity):
    
    def __init__(self, pos, imageurl):
        Entity.Entity.__init__(self, pos, imageurl=imageurl)
        self.max_speed = 0.25
        self.acceleration = 0.01 #fiddle with this until it seems good
        self.inventory = [[None] * 10, [None] * 10, [None] * 10, [None] * 10, [None] * 10] #5 by 10 empty inventory
        self.selected_slot = 0
    
    def update(self, world):
        old_chunk = Convert.world_to_chunk(self.pos[0])[1]
        hspeed = min(abs(self.vel[0] + self.acceleration * self.dir[0]), self.max_speed) * self.dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * self.dir[1]), self.max_speed) * self.dir[1]
        self.vel = [hspeed, vspeed]
        super(Player, self).update(world)
        new_chunk = Convert.world_to_chunk(self.pos[0])[1]
        if new_chunk != old_chunk:
            world.load_chunks(new_chunk)
        
        entities = world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1]).entities
        for entity in entities:
            if(self.bounding_box.colliderect(entity.bounding_box)):
                if type(entity) is BlockDrop:
                    if self.pickup(entity.blockname):
                        entities.remove(entity)
    
    def pickup(self, blocktype):
        for row in self.inventory:
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = ItemStack(blocktype)
                    return True
                elif row[i].itemtype == blocktype and row[i].count < MAX_STACK_SIZE:
                    row[i].count += 1
                    return True
        return False
    
    def get_break_distance(self):
        #extend with certain items?
        return BREAK_DIST
    
    def render(self, screen, pos):
        screen.blit(self.img, pos)
        #render tail
    
    def render_hotbar(self, screen):
        width = Game.SCALE * Game.BLOCK_SIZE * len(self.inventory[0])
        left = (Game.SCREEN_WIDTH - width) / 2
        top = 16
        pygame.draw.rect(screen, Game.BLACK, pygame.Rect(left, top, width, Game.SCALE * Game.BLOCK_SIZE), 0)
        inventory = self.inventory
        for c in range(len(inventory[0])):
            inv_item = inventory[0][c]
            if inv_item is not None:
                screen.blit(World.block_images[False][World.get_block_id(inv_item.itemtype)], (left + c * 32, top))
                countimg = Game.get_font().render(str(inv_item.count), 0, Game.WHITE)
                screen.blit(countimg, (left + c * 32, top))
            #TODO make it work for items too
        #highlight selected item
        pygame.draw.rect(screen, Game.WHITE, pygame.Rect(left + Game.SCALE * Game.BLOCK_SIZE * self.selected_slot, top, Game.SCALE * Game.BLOCK_SIZE, Game.SCALE * Game.BLOCK_SIZE), 2)
    
    def change_slot(self, direction):
        if direction:
            self.selected_slot += 1
            if self.selected_slot >= len(self.inventory[0]):
                self.selected_slot -= len(self.inventory[0])
        else:
            self.selected_slot -= 1
            if self.selected_slot < 0:
                self.selected_slot += len(self.inventory[0])