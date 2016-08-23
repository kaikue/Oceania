import Entity
import EntityPuzzlePiece

class EntityPuzzleController(Entity.Entity):
    def __init__(self, pos, chunk):
        super(EntityPuzzleController, self).__init__(pos, "", False)
        for r in range(4):
            for c in range(4):
                p = (r, c)
                if p != (0, 0):
                    e = EntityPuzzlePiece.EntityPuzzlePiece([pos[0] + 1 + r, pos[1] + 1 + c], p)
                    chunk.entities.append(e)
    
    def update(self, world):
        #check if solved
        pass