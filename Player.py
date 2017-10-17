import math
import pygame
import Convert
import Game
import Images
from ent.ItemDrop import ItemDrop
from itm import ItemStack
import World
from Inventory import Inventory
import ent.DamageSource
from ent.DamageSourceSweep import DamageSourceSweep
from ent.EntityLiving import EntityLiving


BREAK_DIST = Game.BLOCK_SIZE * 5
ANIM_TIME = 10

HAIR_COLORS = ["yellow", "red", "brown", "black", "gray", "white", "green", "blue", "none"]
HAIR_LENGTHS = ["short", "medium", "long"]
BODY_COLORS = ["peach", "tan", "brown", "white", "purple", "black"]
TAIL_COLORS = ["blue", "green", "red", "purple", "orange", "black"]

class Player(EntityLiving):
    
    def __init__(self, pos, options):
        self.hair_color = options[0]
        self.hair_length = options[1]
        self.body_color = options[2]
        self.tail_color = options[3]
        
        super().__init__(pos, "", 20)
        self.max_speed = 0.25
        self.acceleration = 0.01
        self.inventory = Inventory(5, 10)
        self.selected_slot = 0
        
        self.anim_timer = 0
        self.anim_frame = False
        
        self.anim_state = 0
        self.anim_dir = 0
        
        #Temp items for testing
        self.inventory.insert(ItemStack.itemstack_from_name("magicStaff"))
        self.inventory.insert(ItemStack.itemstack_from_name("pickaxe"))
        self.inventory.insert(ItemStack.itemstack_from_name("sword"))
    
    def load_images_for(self, directory):
        img_idle_l = Images.load_imageurl("img/player/" + directory + "/idle.png")
        img_idle_r = Images.flip_horizontal(img_idle_l)
        imgs_idle = (img_idle_l, img_idle_r)
        img_swim_1_l = Images.load_imageurl("img/player/" + directory + "/swim1.png")
        img_swim_1_u = Images.rotate(img_swim_1_l, -90)
        img_swim_1_r = Images.flip_horizontal(img_swim_1_l)
        img_swim_1_d = Images.rotate(img_swim_1_l, 90)
        imgs_swim_1 = (img_swim_1_l, img_swim_1_u, img_swim_1_r, img_swim_1_d)
        img_swim_2_l = Images.load_imageurl("img/player/" + directory + "/swim2.png")
        img_swim_2_u = Images.rotate(img_swim_2_l, -90)
        img_swim_2_r = Images.flip_horizontal(img_swim_2_l)
        img_swim_2_d = Images.rotate(img_swim_2_l, 90)
        imgs_swim_2 = (img_swim_2_l, img_swim_2_u, img_swim_2_r, img_swim_2_d)
        return (imgs_idle, imgs_swim_1, imgs_swim_2)
    
    def load_image(self):
        self.hair_images = self.load_images_for("hair/" + HAIR_COLORS[self.hair_color] + "/" + HAIR_LENGTHS[self.hair_length])
        self.body_images = self.load_images_for("body/" + BODY_COLORS[self.body_color])
        self.tail_images = self.load_images_for("tail/" + TAIL_COLORS[self.tail_color])
        self.img = self.body_images[0][0]
        self.hair_img = self.hair_images[0][0]
        self.tail_img = self.tail_images[0][0]
    
    def update(self, world):
        old_chunk = self.get_chunk()
        hspeed = min(abs(self.vel[0] + self.acceleration * self.move_dir[0]), self.max_speed) * self.move_dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * self.move_dir[1]), self.max_speed) * self.move_dir[1]
        self.vel = [hspeed, vspeed]
        super().update(world)
        self.update_image()
        
        new_chunk = self.get_chunk()
        if new_chunk != old_chunk:
            world.load_chunks(new_chunk)
    
    def update_image(self):
        xvel = Game.cutoff(self.vel[0], 0.01)
        yvel = Game.cutoff(self.vel[1], 0.01)
        
        if xvel != 0 or yvel != 0:
            self.anim_timer += 1
            if self.anim_timer == ANIM_TIME:
                self.anim_timer = 0
                self.anim_frame = not self.anim_frame
            if self.anim_frame:
                self.anim_state = 2
            else:
                self.anim_state = 1
        
        if xvel < 0:
            self.anim_dir = 0
        elif xvel > 0:
            self.anim_dir = 2
        elif yvel < 0:
            self.anim_dir = 1
        elif yvel > 0:
            self.anim_dir = 3
        else:
            if self.facing == Game.LEFT:
                self.anim_dir = 0
            else:
                self.anim_dir = 1
            self.anim_state = 0
            self.anim_timer = 0
        self.img = self.body_images[self.anim_state][self.anim_dir]
        self.hair_img = self.hair_images[self.anim_state][self.anim_dir]
        self.tail_img = self.tail_images[self.anim_state][self.anim_dir]
        
        self.bounding_box.width = self.img.get_width()
        self.bounding_box.height = self.img.get_height()
    
    def render(self, screen, pos):
        screen.blit(self.tail_img, pos)
        super().render(screen, pos)
        screen.blit(self.hair_img, pos)
        
        if self.attack is None:
            item = self.get_held_item()
            if item is not None:
                self.render_held_item(screen, pos, item)
        else:
            self.attack.render_actual(screen)
    
    def render_held_item(self, screen, pos, item):
        #calculate position of held item in player's hand based on animation state
        #    as well as whether it's a placeable block
        if self.anim_state == 0:
            offset_y = Game.BLOCK_SIZE * Game.SCALE * 1 / 16
            if self.anim_dir == 0: #left
                offset_x = Game.BLOCK_SIZE * Game.SCALE * -12 / 16
                if item.can_place:
                    offset_x += Game.BLOCK_SIZE * Game.SCALE * 2 / 16
                else:
                    img = item.imgs[0]
            else: #right
                offset_x = Game.BLOCK_SIZE * Game.SCALE * 20 / 16
                if item.can_place:
                    offset_x += Game.BLOCK_SIZE * Game.SCALE * -2 / 16
                else:
                    img = item.imgs[1]
        else:
            if self.anim_dir == 0: #left
                offset_x = Game.BLOCK_SIZE * Game.SCALE * 0 / 16
                offset_y = Game.BLOCK_SIZE * Game.SCALE * 12 / 16
                if self.anim_state == 2:
                    offset_x += Game.BLOCK_SIZE * Game.SCALE * 1 / 16
                if item.can_place:
                    offset_y += Game.BLOCK_SIZE * Game.SCALE * -2 / 16
                else:
                    img = item.imgs[2]
            elif self.anim_dir == 1: #up
                offset_x = Game.BLOCK_SIZE * Game.SCALE * -12 / 16
                offset_y = Game.BLOCK_SIZE * Game.SCALE * 0 / 16
                if self.anim_state == 2:
                    offset_y += Game.BLOCK_SIZE * Game.SCALE * 1 / 16
                if item.can_place:
                    offset_x += Game.BLOCK_SIZE * Game.SCALE * 2 / 16
                else:
                    img = item.imgs[0]
            elif self.anim_dir == 2: #right
                offset_x = Game.BLOCK_SIZE * Game.SCALE * 27 / 16
                offset_y = Game.BLOCK_SIZE * Game.SCALE * 12 / 16
                if self.anim_state == 2:
                    offset_x -= Game.BLOCK_SIZE * Game.SCALE * 1 / 16
                if item.can_place:
                    offset_y += Game.BLOCK_SIZE * Game.SCALE * -2 / 16
                else:
                    img = item.imgs[3]
            else: #down
                offset_x = Game.BLOCK_SIZE * Game.SCALE * 12 / 16
                offset_y = Game.BLOCK_SIZE * Game.SCALE * 27 / 16
                if self.anim_state == 2:
                    offset_y -= Game.BLOCK_SIZE * Game.SCALE * 1 / 16
                if item.can_place:
                    offset_x += Game.BLOCK_SIZE * Game.SCALE * -2 / 16
                else:
                    img = item.imgs[4]
        
        if item.can_place:
            img = item.imgs[0]
            offset_x += Game.BLOCK_SIZE * Game.SCALE * 1 / 4
            offset_y += Game.BLOCK_SIZE * Game.SCALE * 1 / 4
        
        screen.blit(img, [pos[0] + offset_x, pos[1] + offset_y])
    
    def collide_with(self, entity, world):
        super().collide_with(entity, world)
        if isinstance(entity, ItemDrop):
            if self.inventory.insert(entity.get_itemstack()) == None:
                world.remove_entity(entity)
    
    def left_click_continuous(self, world, mouse_pos, viewport, background):
        self.break_block(world, pygame.mouse.get_pos(), viewport, background)
        self.do_attack(world, mouse_pos, viewport)
    
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
                self.remove_held_item()
    
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
    
    def left_click_discrete(self, world, mouse_pos, viewport, background):
        pass
    
    def do_attack(self, world, mouse_pos, viewport):
        if self.attack is not None:
            return
        held_item = self.get_held_item()
        if held_item is not None:
            damage = held_item.get_attack_damage()
            knockback = held_item.get_knockback()
            reach = ent.DamageSourceSweep.DEFAULT_REACH #TODO
        else:
            damage = ent.DamageSource.DEFAULT_ATTACK
            knockback = ent.DamageSource.DEFAULT_KNOCKBACK
            reach = ent.DamageSourceSweep.DEFAULT_REACH
        pos = self.pos[:]
        angle = self.find_angle(mouse_pos, viewport)
        self.attack = DamageSourceSweep(pos, damage, knockback, reach, angle, held_item, self, 30)
        world.create_entity(self.attack)
    
    def get_held_item(self):
        return self.inventory[0][self.selected_slot]
    
    def remove_held_item(self):
        item = self.get_held_item()
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
            chunk.entities.append(ItemDrop(block_pos, block["name"], blockentity))
    
    def get_color(self, background):
        if background:
            return (192, 192, 192, 128)
        else:
            return (255, 255, 255, 128)
    
    def render_break_preview(self, background, world, block, block_pos, screen, viewport):
        chunk = world.loaded_chunks.get(Convert.world_to_chunk(block_pos[0])[1])
        blockimg = world.get_block_render(World.get_block_id(block["name"]), block_pos, block["connectedTexture"], background, chunk, background).copy()
        mask = pygame.mask.from_surface(blockimg)
        olist = mask.outline()
        polysurface = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA)
        color = self.get_color(background)
        pygame.draw.polygon(polysurface, color, olist, 0)
        screen.blit(polysurface, Convert.world_to_viewport(block_pos, viewport))
    
    def render_block_preview(self, background, held_item, world, block_pos, screen, viewport):
        held_block = World.get_block(held_item.name)
        chunk = world.loaded_chunks.get(Convert.world_to_chunk(block_pos[0])[1])
        blockimg = world.get_block_render(World.get_block_id(held_block["name"]), block_pos, held_block["connectedTexture"], background, chunk, background).copy()
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