import Game
import World
import gui.GUI as GUI
import importlib
import ent.DamageSource


MAX_STACK_SIZE = 100

def itemstack_from_name(itemname):
    item = World.items[itemname]
    item_class = getattr(importlib.import_module("itm." + item["class"]), item["class"])
    return item_class(itemname)


class ItemStack(object):
    
    def __init__(self, name, stackable = True, data = None, count = 1):
        self.name = name
        self.load_image()
        self.can_place = World.items[name]["can_place"]
        self.count = count
        self.stackable = stackable
        self.data = data
    
    def load_image(self):
        self.img = World.item_images[self.name]
    
    def can_stack(self, itemstack):
        return itemstack is not None and \
            itemstack.count + self.count <= MAX_STACK_SIZE and \
            itemstack.name == self.name and \
            self.stackable and \
            itemstack.data == self.data
    
    def take_one(self):
        self.count -= 1
        if self.count == 0:
            return None
        else:
            return self

    def take_half(self):
        other_stack = self.copy_one()
        other_stack.count = self.count
        self.count = self.count // 2
        other_stack.count -= self.count
        s = self
        if self.count == 0:
            s = None
        if other_stack.count == 0:
            other_stack = None
        return s, other_stack
    
    def copy_one(self):
        itemstack = itemstack_from_name(self.name)
        itemstack.stackable = self.stackable
        itemstack.data = self.data
        return itemstack
    
    def get_attack_damage(self):
        return ent.DamageSource.DEFAULT_ATTACK
    
    def get_knockback(self):
        return ent.DamageSource.DEFAULT_KNOCKBACK
    
    def get_break_speed(self):
        return 1
    
    def get_harvest_level(self):
        return 0
    
    def use_continuous(self, world, player, mouse_pos, viewport):
        pass
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        pass
    
    def render(self, pos, screen):
        img = self.img
        if self.can_place:
            img = World.block_images[False][World.get_block_id(self.name)]
        screen.blit(img, (pos[0] + GUI.SCALING / 6, pos[1] + GUI.SCALING / 6))
        if self.stackable:
            countimg = Game.get_font().render(str(self.count), 0, Game.WHITE)
            screen.blit(countimg, (pos[0] + 3 * Game.SCALE, pos[1] + 3 * Game.SCALE))
    
    def __str__(self):
        return str(self.count) + "x " + self.name