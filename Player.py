import math
import pygame
import Convert
import Game
from ent.ItemDrop import ItemDrop
from itm import ItemStack
import World
from Inventory import Inventory
from ent.DamageSource import DamageSource
from ent.EntityLiving import EntityLiving


BREAK_DIST = Game.BLOCK_SIZE * 5

class Player(EntityLiving):
    
    def __init__(self, pos, imageurl):
        super(Player, self).__init__(pos, imageurl, 20)
        self.max_speed = 0.25
        self.acceleration = 0.01 #fiddle with this until it seems good
        self.inventory = Inventory(5, 10)
        self.selected_slot = 0
        
        #Temp items for testing
        self.inventory.insert(ItemStack.itemstack_from_name("magicStaff"))
        self.inventory.insert(ItemStack.itemstack_from_name("pickaxe"))
        self.inventory.insert(ItemStack.itemstack_from_name("sword"))
    
    def update(self, world):
        old_chunk = self.get_chunk()
        hspeed = min(abs(self.vel[0] + self.acceleration * self.move_dir[0]), self.max_speed) * self.move_dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * self.move_dir[1]), self.max_speed) * self.move_dir[1]
        self.vel = [hspeed, vspeed]
        super(Player, self).update(world)
        new_chunk = self.get_chunk()
        if new_chunk != old_chunk:
            world.load_chunks(new_chunk)
    
    def collide_with(self, entity, world):
        super(Player, self).collide_with(entity, world)
        if isinstance(entity, ItemDrop):
            if self.inventory.insert(entity.get_itemstack()) == None:
                world.remove_entity(entity)
    
    def right_click_continuous(self, world, mouse_pos, viewport, background):
        item = self.get_held_item()
        block_pos = self.find_angle_pos(mouse_pos, viewport)
        
        if item is None:
            return
        
        item.use_continuous(world, self, mouse_pos, viewport)
        
        if item.can_place:
            #try to place the block
            
            #don't want to place a solid block over an entity
            if not background:
                entities = world.get_nearby_entities(self.get_chunk())
                entities.append(self) #check against player too
                for entity in entities:
                    if entity.collides(block_pos) and entity.background == background and World.get_block(item.name)["solid"]:
                        return
            
            if world.get_block_at(block_pos, False) == "water" and \
                (not background or world.get_block_at(block_pos, True) == "water"):
                world.set_block_at(block_pos, World.get_block(item.name), background)
                blockentity = item.data
                if blockentity is not None:
                    blockentity.load_image()
                    blockentity.set_pos(block_pos)
                    blockentity.background = background
                    world.create_entity(blockentity)
                item.count -= 1
                if item.count == 0:
                    self.inventory[0][self.selected_slot] = None
    
    def left_click_discrete(self, world, mouse_pos, viewport, background):
        held_item = self.get_held_item()
        if held_item is not None:
            damage = held_item.get_attack_damage()
        else:
            damage = 1
        attack = DamageSource(self.pos, "img/attack.png", damage, self, 30) #TODO: offset with mouse_pos
        world.create_entity(attack)
        #TODO: animate held item swinging
    
    def right_click_discrete(self, world, mouse_pos, viewport, background):
        item = self.get_held_item()
        block_pos = self.find_angle_pos(mouse_pos, viewport)
        entities = world.get_nearby_entities(self.get_chunk())
        for entity in entities:
            if entity.collides(block_pos) and entity.background == background:
                if entity.interact(self, item):
                    return
        
        if item is None:
            return
        
        item.use_discrete(world, self, mouse_pos, viewport)
    
    def get_held_item(self):
        return self.inventory[0][self.selected_slot]
    
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
        held_item = self.get_held_item()
        if held_item is None:
            harvest_level = 0
            break_speed = 1
        else:
            harvest_level = held_item.get_harvest_level()
            break_speed = held_item.get_break_speed()
        if (not block["breakable"]) or (block["harvestlevel"] > harvest_level):
            return
        block_to_break = None
        breaking_blocks = world.breaking_blocks[background]
        for breaking_block in breaking_blocks:
            if breaking_block["pos"] == block_pos:
                block_to_break = breaking_block
        if block_to_break is None:
            block_to_break = {"pos": block_pos, "name": block["name"], "progress": 0, "breaktime": block["breaktime"]}
            breaking_blocks.append(block_to_break)
        block_to_break["progress"] += 2 * break_speed
        if block_to_break["progress"] >= block_to_break["breaktime"]:
            #remove the block
            breaking_blocks.remove(block_to_break)
            chunk.set_block_at(Convert.world_to_chunk(block_pos[0])[0], block_pos[1], World.get_block("water"), background)
            blockentity = None
            if block["entity"] != "":
                    #remove the associated entity
                for entity in chunk.entities:
                    if type(entity).__name__ == block["entity"] and [int(entity.pos[0]), int(entity.pos[1])] == block_pos:
                        chunk.entities.remove(entity)
                        blockentity = entity
                        break
            chunk.entities.append(ItemDrop(block_pos, block["name"], block["image"], blockentity))
    
    def get_color(self, background):
        if background:
            return (192, 192, 192, 128)
        else:
            return (255, 255, 255, 128)
    
    def render_break_preview(self, background, world, block, block_pos, screen, viewport):
        blockimg = world.get_block_render(World.get_block_id(block["name"]), block_pos, block["connectedTexture"], background, background).copy()
        mask = pygame.mask.from_surface(blockimg)
        olist = mask.outline()
        polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
        color = self.get_color(background)
        pygame.draw.polygon(polysurface, color, olist, 0)
        screen.blit(polysurface, Convert.world_to_viewport(block_pos, viewport))
    
    def render_block_preview(self, background, held_item, world, block_pos, screen, viewport):
        held_block = World.get_block(held_item.name)
        blockimg = world.get_block_render(World.get_block_id(held_block["name"]), block_pos, held_block["connectedTexture"], background, background).copy()
        mask = pygame.mask.from_surface(blockimg)
        olist = mask.outline()
        polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
        screen.blit(polysurface, Convert.world_to_viewport(block_pos, viewport))
        collides = False
        entities = world.get_nearby_entities(self.get_chunk())
        entities.append(self)
        for entity in entities:
            if entity.collides(block_pos) and entity.background == background:
                collides = True
        color = self.get_color(background)
        if collides and World.get_block(held_block["name"])["solid"]:
            color = (color[0], 0, 0, color[3])
        pygame.draw.polygon(polysurface, color, olist, 0)
        blockimg.blit(polysurface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(blockimg, Convert.world_to_viewport(block_pos, viewport))
    
    def draw_block_highlight(self, world, mouse_pos, viewport, screen, shift):
        #if player can break the block at the position, highlight it
        #if player is holding a block and can place it, render a preview
        block_pos = self.find_angle_pos(mouse_pos, viewport)
        held_item = self.get_held_item()
        if held_item is None:
            harvest_level = 0
        else:
            harvest_level = held_item.get_harvest_level()
        
        block = World.get_block(world.get_block_at(block_pos, shift))
        samewater = block["name"] == "water"
        fgwater = World.get_block(world.get_block_at(block_pos, False))["name"] == "water"
        if block["breakable"] and block["harvestlevel"] <= harvest_level and (not shift or fgwater):
            self.render_break_preview(shift, world, block, block_pos, screen, viewport)
        elif held_item is not None and held_item.can_place and samewater:
            self.render_block_preview(shift, held_item, world, block_pos, screen, viewport)
    
    def render(self, screen, pos):
        #TODO: fancy animations here
        super(Player, self).render(screen, pos)
        item = self.get_held_item()
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
    
    def die(self, world):
        self.health = self.max_health
        #TODO: only create grave at nearest empty foreground space
        world.set_block_at([int(self.pos[0]), int(self.pos[1])], World.get_block("grave"), False)
        #TODO: fill it up with items and clear inventory
        #TODO: respawn