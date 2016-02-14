import Game
import World
import Entity

class BlockDrop(Entity.Entity):
    
    def __init__(self, pos, blockname, blockentity = None):
        self.blockname = blockname
        self.blockentity = blockentity
        pos = [pos[0] + 0.25, pos[1] + 0.25]
        Entity.Entity.__init__(self, pos, World.get_block(blockname)["image"], (Game.BLOCK_SIZE * Game.SCALE // 2, Game.BLOCK_SIZE * Game.SCALE // 2))