from ItemStack import ItemStack


class ToolPickaxe(ItemStack):
    
    def __init__(self, itemname, imageurl):
        ItemStack.__init__(self, itemname, imageurl, False, stackable = False, itemdata = None)
    
    def get_break_speed(self):
        return 2
    
    def get_harvest_level(self):
        return 1