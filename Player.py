import math
import importlib
import pygame
import Convert
import Game
from Entity import Entity
from ItemDrop import ItemDrop
from ItemStack import ItemStack
from ToolMagicStaff import ToolMagicStaff
from ToolPickaxe import ToolPickaxe
import World


BREAK_DIST = 48

class Player(Entity):
    
    def __init__(self, pos, imageurl):
        Entity.__init__(self, pos, imageurl=imageurl, scale=(2, 2))
        self.max_health = 20
        self.health = 18
        self.max_speed = 0.25
        self.acceleration = 0.01 #fiddle with this until it seems good
        self.inventory = [[None] * 10, [None] * 10, [None] * 10, [None] * 10, [None] * 10] #5 by 10 empty inventory
        self.selected_slot = 0
        
        #Temp items for testing
        self.inventory[0][0] = ToolMagicStaff("magicStaff", "img/tools/staff.png")
        self.inventory[0][1] = ToolPickaxe("pickaxe", "img/tools/pickaxe.png")
    
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
                if isinstance(entity, ItemDrop):
                    if self.pickup(entity):
                        world.loaded_chunks.get(entity.get_chunk()).entities.remove(entity)
    
    def get_nearby_entities(self, world):
        entities = list(world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1]).entities)
        entities += world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1] - 1).entities
        entities += world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1] + 1).entities
        return entities
    
    def pickup(self, itemdrop):
        for row in self.inventory:
            for i in range(len(row)):
                if row[i] is None:
                    if itemdrop.itemclass == "":
                        item = ItemStack(itemdrop.itemtype, itemdrop.imageurl, itemdrop.can_place, stackable = itemdrop.stackable, itemdata = itemdrop.itemdata)
                    else:
                        EntityClass = getattr(importlib.import_module(itemdrop.itemclass), itemdrop.itemclass)
                        item = EntityClass(itemdrop.itemtype, itemdrop.imageurl, itemdrop.can_place, stackable = itemdrop.stackable, itemdata = itemdrop.itemdata)
                    row[i] = item
                    return True
                elif row[i].can_stack(itemdrop):
                    row[i].count += 1
                    return True
        return False
    
    def right_click_continuous(self, world, mouse_pos, viewport, background):
        item = self.inventory[0][self.selected_slot]
        block_pos = self.find_angle_pos(mouse_pos, viewport)
        
        if item is None:
            return
        
        item.use_continuous(world, self, mouse_pos, viewport)
        
        if item.can_place:
            #try to place the block
            
            #don't want to place a solid block over an entity
            if not background:
                entities = self.get_nearby_entities(world)
                entities.append(self) #check against player too
                for entity in entities:
                    if entity.collides(block_pos) and World.get_block(item.itemname)["solid"]:
                        return
            
            #don't place blocks with entities in the background
            blockentity = item.itemdata
            if blockentity is not None and background:
                return
            
            if world.get_block_at(block_pos, False) == "water" and \
                (not background or world.get_block_at(block_pos, True) == "water"):
                world.set_block_at(block_pos, World.get_block(item.itemname), background)
                if blockentity is not None:
                    blockentity.pos = block_pos
                    world.loaded_chunks.get(Convert.world_to_chunk(block_pos[0])[1]).entities.append(blockentity)
                item.count -= 1
                if item.count == 0:
                    self.inventory[0][self.selected_slot] = None
    
    def right_click_discrete(self, world, mouse_pos, viewport, background):
        item = self.inventory[0][self.selected_slot]
        block_pos = self.find_angle_pos(mouse_pos, viewport)
        entities = self.get_nearby_entities(world)
        for entity in entities:
            if entity.collides(block_pos):
                entity.interact(item)
        
        if item is None:
            return
        
        item.use_discrete(world, self, mouse_pos, viewport)
    
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
    
    def find_angle_pos(self, mouse_pos, viewport):
        angle = self.find_angle(mouse_pos, viewport)
        return Convert.pixels_to_world(self.find_pos(angle, self.pixel_pos(True), Convert.viewport_to_pixels(mouse_pos, viewport), self.get_break_distance()))
    
    def break_block(self, world, mouse_pos, viewport, background):
        block_pos = self.find_angle_pos(mouse_pos, viewport)
        chunk = world.loaded_chunks.get(Convert.world_to_chunk(block_pos[0])[1])
        #if there's a foreground block covering the background, don't break anything
        if background and world.get_block_at(block_pos, False) != "water":
            return
        block = World.get_block(world.get_block_at(block_pos, background))
        held_item = self.inventory[0][self.selected_slot]
        if held_item is None:
            harvest_level = 0
            break_speed = 1
        else:
            harvest_level = held_item.get_harvest_level()
            break_speed = held_item.get_break_speed()
        if (not block["breakable"]) or (block["harvestlevel"] > harvest_level):
            return
        block_to_break = None
        for breaking_block in world.breaking_blocks[background]:
            if breaking_block["pos"] == block_pos:
                block_to_break = breaking_block
        if block_to_break is None:
            block_to_break = {"pos": block_pos, "name": block["name"], "progress": 0, "breaktime": block["breaktime"]}
            world.breaking_blocks[background].append(block_to_break)
        block_to_break["progress"] += 2 * break_speed
        if block_to_break["progress"] >= block_to_break["breaktime"]:
            #remove the block
            world.breaking_blocks[background].remove(block_to_break)
            chunk.set_block_at(Convert.world_to_chunk(block_pos[0])[0], block_pos[1], World.get_block("water"), background)
            blockentity = None
            if block["entity"] is not "":
                    #remove the associated entity
                for entity in chunk.entities:
                    if type(entity).__name__ == block["entity"] and [int(entity.pos[0]), int(entity.pos[1])] == block_pos:
                        chunk.entities.remove(entity)
                        blockentity = entity
                        break
            chunk.entities.append(ItemDrop(block_pos, block["name"], block["image"], block["item"], True, True, blockentity))
    
    def draw_block_highlight(self, world, mouse_pos, viewport, screen, shift):
        #if player can break the foreground block at the position, highlight it
        #if player is holding a block and can place it in the foreground, render a preview
        #repeat for background
        block_pos = self.find_angle_pos(mouse_pos, viewport)
        held_item = self.inventory[0][self.selected_slot]
        if held_item is None:
            harvest_level = 0
        else:
            harvest_level = held_item.get_harvest_level()
        
        block = World.get_block(world.get_block_at(block_pos, False))
        if not shift and block["breakable"] and block["harvestlevel"] <= harvest_level:
            blockimg = world.get_block_render(World.get_block_id(block["name"]), block_pos, block["connectedTexture"], False).copy()
            mask = pygame.mask.from_surface(blockimg)
            olist = mask.outline()
            polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
            pygame.draw.polygon(polysurface, (255, 255, 255, 128), olist, 0)
            screen.blit(polysurface, Convert.world_to_viewport(block_pos, viewport))
            return
        if not shift and held_item is not None and held_item.can_place and block["name"] == "water":
            held_block = World.get_block(held_item.itemname)
            blockimg = world.get_block_render(World.get_block_id(held_block["name"]), block_pos, held_block["connectedTexture"], False).copy()
            mask = pygame.mask.from_surface(blockimg)
            olist = mask.outline()
            polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
            screen.blit(polysurface, Convert.world_to_viewport(block_pos, viewport))
            collides = False
            entities = self.get_nearby_entities(world)
            entities.append(self)
            for entity in entities:
                if entity.collides(block_pos):
                    collides = True
            if collides and World.get_block(held_block["name"])["solid"]:
                pygame.draw.polygon(polysurface, (255, 0, 0, 128), olist, 0)
            else:
                pygame.draw.polygon(polysurface, (255, 255, 255, 128), olist, 0)
            blockimg.blit(polysurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(blockimg, Convert.world_to_viewport(block_pos, viewport))
            return
        
        fgwater = block["name"] == "water"
        block = World.get_block(world.get_block_at(block_pos, True))
        if shift and block["breakable"] and block["harvestlevel"] <= harvest_level and fgwater:
            blockimg = world.get_block_render(World.get_block_id(block["name"]), block_pos, block["connectedTexture"], True, True).copy()
            mask = pygame.mask.from_surface(blockimg)
            olist = mask.outline()
            polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
            pygame.draw.polygon(polysurface, (192, 192, 192, 128), olist, 0)
            screen.blit(polysurface, Convert.world_to_viewport(block_pos, viewport))
            return
        if shift and held_item is not None and held_item.can_place and block["name"] == "water" and fgwater:
            held_block = World.get_block(held_item.itemname)
            blockimg = world.get_block_render(World.get_block_id(held_block["name"]), block_pos, held_block["connectedTexture"], True, True).copy()
            mask = pygame.mask.from_surface(blockimg)
            olist = mask.outline()
            polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
            screen.blit(polysurface, Convert.world_to_viewport(block_pos, viewport))
            #check for background entities?
            pygame.draw.polygon(polysurface, (192, 192, 192, 128), olist, 0)
            blockimg.blit(polysurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(blockimg, Convert.world_to_viewport(block_pos, viewport))
            return
    
    def render(self, screen, pos):
        #TODO fancy animations here
        screen.blit(self.img, pos)
        item = self.inventory[0][self.selected_slot]
        if item is not None:
            screen.blit(item.img, [pos[0] - (Game.BLOCK_SIZE * Game.SCALE * 5 / 8), pos[1] + (Game.BLOCK_SIZE * Game.SCALE / 16)])
    
    def change_slot(self, direction):
        if direction:
            self.selected_slot += 1
            if self.selected_slot >= len(self.inventory[0]):
                self.selected_slot -= len(self.inventory[0])
        else:
            self.selected_slot -= 1
            if self.selected_slot < 0:
                self.selected_slot += len(self.inventory[0])