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
        self.max_health = 20
        self.health = 18
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
                    if self.pickup(entity):
                        world.loaded_chunks.get(entity.get_chunk()).entities.remove(entity)
    
    def get_nearby_entities(self, world):
        entities = list(world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1]).entities)
        entities += world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1] - 1).entities
        entities += world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1] + 1).entities
        return entities
    
    def pickup(self, block):
        #TODO make this work for items as well
        for row in self.inventory:
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = ItemStack(block.blockname, True, block.blockentity)
                    return True
                elif row[i].itemtype == block.blockname and row[i].count < MAX_STACK_SIZE and block.blockentity is None:
                    #can't stack blocks with entities like chests
                    row[i].count += 1
                    return True
        return False
    
    def use_held_item(self, world, mouse_pos, viewport, background):
        angle = self.find_angle(mouse_pos, viewport)
        block_pos = Convert.pixels_to_world(self.find_pos(angle, self.pixel_pos(True), Convert.viewport_to_pixels(mouse_pos, viewport), self.get_break_distance()))
        item = self.inventory[0][self.selected_slot]
        
        if not background:
            entities = self.get_nearby_entities(world)
            entities.append(self) #check against player too
            for entity in entities:
                if entity.collides(block_pos):
                    entity.interact(item)
                    return #don't want to place a block over an entity
        
        if item is None or not item.can_place:
            return
        
        #don't place blocks with entities in the background
        if item.blockentity is not None and background:
            return
        
        if World.blocks[world.get_block_at(block_pos, False)]["name"] == "water" and \
            (not background or World.blocks[world.get_block_at(block_pos, True)]["name"] == "water"):
            world.set_block_at(block_pos, World.get_block(item.itemtype), background)
            if item.blockentity is not None:
                item.blockentity.pos = block_pos
                world.loaded_chunks.get(Convert.world_to_chunk(block_pos[0])[1]).entities.append(item.blockentity)
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
            blockentity = None
            if block["entity"] is not "":
                for entity in chunk.entities:
                    if type(entity).__name__ == block["entity"] and [int(entity.pos[0]), int(entity.pos[1])] == block_pos:
                        chunk.entities.remove(entity)
                        blockentity = entity
                        break
            chunk.entities.append(BlockDrop(block_pos, block["name"], blockentity))
    
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