from itm.ItemStack import ItemStack


class ItemTool(ItemStack):
    
    def __init__(self, name):
        ItemStack.__init__(self, name, stackable = False, data = None)