import Game
import World
from ItemStack import ItemStack


class ItemFlint(ItemStack):
    
    def __init__(self, itemname, imageurl, can_place, stackable = True, itemdata = None):
        ItemStack.__init__(self, itemname, imageurl, can_place, stackable, itemdata)
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        pos = player.find_angle_pos(mouse_pos, viewport)
        block = World.blocks[world.get_block_at(pos, False)]["name"]
        if block == "flint":
            Game.play_sound("sfx/rock/hit.wav")
            world.set_block_at(pos, World.get_block("flint_knapped_1"), False)
        elif block == "flint_knapped_1":
            Game.play_sound("sfx/rock/hit.wav")
            world.set_block_at(pos, World.get_block("flint_knapped_2"), False)
        elif block == "flint_knapped_2":
            Game.play_sound("sfx/rock/hit.wav")
            world.set_block_at(pos, World.get_block("flint_knapped_3"), False)
        elif block == "flint_knapped_3":
            Game.play_sound("sfx/rock/hit.wav")
            world.set_block_at(pos, World.get_block("flint_knapped_4"), False)