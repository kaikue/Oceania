import World
from ItemStack import ItemStack


class ItemSharpFlint(ItemStack):
    
    def __init__(self, itemname, imageurl, can_place, stackable = True, itemdata = None):
        ItemStack.__init__(self, itemname, imageurl, can_place, stackable, itemdata)
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        pos = player.find_angle_pos(mouse_pos, viewport)
        block = World.blocks[world.get_block_at(pos, False)]["name"]
        if block == "bone":
            #make a basic pick?
            pass