class ItemStack(object):
    
    def __init__(self, itemtype, can_place):
        self.itemtype = itemtype
        self.can_place = can_place
        self.count = 1
    
    def __str__(self):
        return str(self.count) + "x " + self.itemtype