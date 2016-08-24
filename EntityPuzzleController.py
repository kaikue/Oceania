import random
import Game
import Entity
import EntityPuzzlePiece

class EntityPuzzleController(Entity.Entity):
    SIZE = 4
    
    def __init__(self, pos, chunk):
        super(EntityPuzzleController, self).__init__(pos, "", False)
        self.pieces = []
        for r in range(EntityPuzzleController.SIZE):
            for c in range(EntityPuzzleController.SIZE):
                p = (r, c)
                if p != (0, 0):
                    e = EntityPuzzlePiece.EntityPuzzlePiece([self.pos[0] + 1 + r, self.pos[1] + 1 + c], p)
                    chunk.entities.append(e)
                    self.pieces.append(e)
        
        #shuffle pieces
        random.shuffle(self.pieces)
        x = 0
        y = 1
        for piece in self.pieces:
            piece.set_pos([self.pos[0] + 1 + x, self.pos[1] + 1 + y])
            y += 1
            if y == EntityPuzzleController.SIZE:
                y = 0
                x += 1
        
        #count inversions
        inversions = self.count_inversions()
        
        #flip if necessary
        if inversions % 2 == EntityPuzzleController.SIZE % 2:
            pos0, pos1 = self.pieces[0].pos, self.pieces[1].pos
            self.pieces[0].set_pos(pos1)
            self.pieces[1].set_pos(pos0)
    
    def update(self, world):
        corner_empty = True
        for piece in self.pieces:
            if piece.pos == [self.pos[0] + 1, self.pos[1] + 1]:
                corner_empty = False
        solved = corner_empty and self.count_inversions() == 0
        if solved:
            Game.play_sound("sfx/puzzle/complete.ogg")
            for piece in self.pieces:
                piece.locked = True
    
    def count_inversions(self):
        inversions = 0
        prev = -1
        for piece in self.pieces:
            i = piece.puzzle_pos[1] * EntityPuzzleController.SIZE + piece.puzzle_pos[0]
            if i < prev:
                inversions += 1
            prev = i
        return inversions