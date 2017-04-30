from itm.ItemStack import ItemStack

HEAL_AMOUNT = 4

class ItemFruit(ItemStack):
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        player.heal(HEAL_AMOUNT)
        player.remove_held_item()