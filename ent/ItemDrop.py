import World
from Entity import Entity
from itm import ItemStack

class ItemDrop(Entity):
    
    def __init__(self, pos, name, data = None, count = 1):
        #center the position in the block
        pos = [pos[0] + 0.25, pos[1] + 0.25]
        self.name = name
        super().__init__(pos, "")
        self.data = data
        self.count = count
    
    def load_image(self):
        self.img = World.item_images[self.name][0]
    
    def get_itemstack(self):
        itemstack = ItemStack.itemstack_from_name(self.name)
        itemstack.count = self.count
        itemstack.data = self.data
        return itemstack