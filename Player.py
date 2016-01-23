import math
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
        
        entities = self.get_nearby_entities(world)
        for entity in entities:
            if(self.bounding_box.colliderect(entity.bounding_box)):
                if type(entity) is BlockDrop:
                    if self.pickup(entity.blockname):
                        world.loaded_chunks.get(entity.get_chunk()).entities.remove(entity)
    
    def get_nearby_entities(self, world):
        entities = list(world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1]).entities)
        entities += world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1] - 1).entities
        entities += world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1] + 1).entities
        return entities
    
    def pickup(self, blocktype):
        for row in self.inventory:
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = ItemStack(blocktype, True)
                    return True
                elif row[i].itemtype == blocktype and row[i].count < MAX_STACK_SIZE:
                    row[i].count += 1
                    return True
        return False
    
    def use_held_item(self, pos, shift, world):
        item = self.inventory[0][self.selected_slot]
        entities = self.get_nearby_entities(world)
        for entity in entities:
            if entity.collides(pos):
                entity.interact(item)
                return #don't want to place a block over an entity
        
        if item is not None and item.can_place and World.blocks[world.get_block_at(pos, False)]["name"] == "water" and (not shift or World.blocks[world.get_block_at(pos, True)]["name"] == "water"):
            world.set_block_at(pos, World.get_block(item.itemtype), shift)
            item.count -= 1
            if item.count == 0:
                self.inventory[0][self.selected_slot] = None
    
    def get_break_distance(self):
        #extend with certain items?
        return BREAK_DIST
    
    def find_angle(self, mouse_pos, viewport):
        #find nearest breakable block based on angle from player pos to mouse pos (raycasting?)
        x_diff = Convert.viewport_to_pixel(mouse_pos[0], viewport, 0) - self.bounding_box.centerx
        y_diff = Convert.viewport_to_pixel(mouse_pos[1], viewport, 1) - self.bounding_box.centery
        angle = math.atan2(y_diff, x_diff)
        return angle
    
    def find_pos(self, angle, offset, close_pos, max_dist):
        #in pixels
        dist = math.hypot(close_pos[0] - offset[0], close_pos[1] - offset[1])
        capped_dist = min(dist, max_dist) 
        return [offset[0] + capped_dist * math.cos(angle), offset[1] + capped_dist * math.sin(angle)]
    
    def break_block(self, world, mouse_pos, viewport, background):
        angle = self.find_angle(mouse_pos, viewport)
        block_pos = Convert.pixels_to_world(self.find_pos(angle, self.pixel_pos(True), Convert.viewport_to_pixels(mouse_pos, viewport), self.get_break_distance()))
        chunk = world.loaded_chunks.get(Convert.world_to_chunk(block_pos[0])[1])
        #if there's a foreground block covering the background, don't break anything
        if background and World.blocks[world.get_block_at(block_pos, False)]["name"] != "water":
            return
        block = World.blocks[world.get_block_at(block_pos, background)]
        if block["breakable"]:
            chunk.set_block_at(Convert.world_to_chunk(block_pos[0])[0], block_pos[1], World.get_block("water"), background)
            chunk.entities.append(BlockDrop(block_pos, block["name"]))
    
    def render(self, screen, pos):
        screen.blit(self.img, pos)
        #render tail
    
    def change_slot(self, direction):
        if direction:
            self.selected_slot += 1
            if self.selected_slot >= len(self.inventory[0]):
                self.selected_slot -= len(self.inventory[0])
        else:
            self.selected_slot -= 1
            if self.selected_slot < 0:
                self.selected_slot += len(self.inventory[0])