from ItemStack import ItemStack


class ToolMagicStaff(ItemStack):
    
    def __init__(self, itemname, imageurl):
        ItemStack.__init__(self, itemname, imageurl, False, stackable = False, itemdata = None)
    
    def use_discrete(self, mouse_pos):
        #create a bolt of energy facing towards direction
        print("using the staff")