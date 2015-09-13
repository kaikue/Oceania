import Entity
import Convert
from BlockDrop import BlockDrop
from ItemStack import ItemStack

class Player(Entity.Entity):
    
    def __init__(self, pos, imageurl):
        Entity.Entity.__init__(self, pos, imageurl=imageurl)
        self.max_speed = 0.25
        self.acceleration = 0.01 #fiddle with this until it seems good
        self.inventory = [[None] * 5, [None] * 5, [None] * 5, [None] * 5, [None] * 5] #5 by 5 empty inventory
    
    def update(self, world):
        old_chunk = Convert.world_to_chunk(self.pos[0])[1]
        hspeed = min(abs(self.vel[0] + self.acceleration * self.dir[0]), self.max_speed) * self.dir[0]
        vspeed = min(abs(self.vel[1] + self.acceleration * self.dir[1]), self.max_speed) * self.dir[1]
        self.vel = [hspeed, vspeed]
        super(Player, self).update(world)
        new_chunk = Convert.world_to_chunk(self.pos[0])[1]
        if new_chunk != old_chunk:
            world.load_chunks(new_chunk)
        
        entities = world.loaded_chunks.get(Convert.world_to_chunk(self.pos[0])[1]).entities
        for entity in entities:
            if(self.bounding_box.colliderect(entity.bounding_box)):
                if type(entity) is BlockDrop:
                    if self.pickup(entity.blockname):
                        entities.remove(entity)
                    print(self.inventory)
    
    def pickup(self, blocktype):
        for row in self.inventory:
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = ItemStack(blocktype)
                    return True
                elif row[i].itemtype == blocktype:
                    row[i].count += 1
                    return True
        return False