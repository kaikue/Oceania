from ItemStack import ItemStack


class ItemTool(ItemStack):
    
    def __init__(self, itemname):
        ItemStack.__init__(self, itemname, stackable = False, data = None)