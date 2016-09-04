from itm.ItemStack import ItemStack


class ItemSharpFlint(ItemStack):
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        pos = player.find_angle_pos(mouse_pos, viewport)
        block = world.get_block_at(pos, False)
        if block == "bone":
            #make a basic pick?
            pass