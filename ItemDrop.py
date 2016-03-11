from Entity import Entity

class ItemDrop(Entity):
    
    def __init__(self, pos, itemtype, img, stackable, can_place, itemdata = None):
        self.itemtype = itemtype
        self.stackable = stackable
        self.can_place = can_place
        self.itemdata = itemdata
        #center the position in the block
        pos = [pos[0] + 0.25, pos[1] + 0.25]
        Entity.__init__(self, pos, loadedimage=img)