class ItemStack(object):
    
    def __init__(self, itemtype):
        self.itemtype = itemtype
        self.count = 1
    
    def __str__(self):
        return str(self.count) + "x " + self.itemtype