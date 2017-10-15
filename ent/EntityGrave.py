import Entity
import Inventory

class EntityGrave(Entity.Entity):
    def __init__(self, pos, chunk, background=False):
        self.inventory = Inventory.Inventory(5, 10)
        super().__init__(pos, "", background)
    
    def load_image(self):
        super().load_image()
        for row in self.inventory:
            for item in row:
                if item is not None:
                    item.load_image()
    
    def fill(self, inventory):
        #copy all items into this inventory
        self.inventory = [i[:] for i in inventory]
    
    #TODO: on die, drop items into world