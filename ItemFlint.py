import Game
import World
from ItemStack import ItemStack


class ItemFlint(ItemStack):
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        pos = player.find_angle_pos(mouse_pos, viewport)
        block = world.get_block_at(pos, False)
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