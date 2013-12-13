import Game
import World
import Entity

class BlockDrop(Entity.Entity):
    
    def __init__(self, pos, blockname):
        pos = [pos[0] + 0.25, pos[1] + 0.25]
        Entity.Entity.__init__(self, pos, World.blocks[blockname]["image"], (Game.BLOCK_SIZE // 2, Game.BLOCK_SIZE // 2))