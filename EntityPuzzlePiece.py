import Game
import Convert
import Entity

class EntityPuzzlePiece(Entity.Entity):
    def __init__(self, pos, puzzle_pos):
        #puzzle_pos must be a pair of ints from 0 to 3, not including (0, 0)
        imageurl = "img/puzzle/puzzle_" + str(puzzle_pos[1]) + "_" + str(puzzle_pos[0]) + ".png"
        super(EntityPuzzlePiece, self).__init__(pos, imageurl, False)
    
    def interact(self, player, item):
        world = Game.get_world()
        sides = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for side in sides:
            goal_pos = [self.pos[0] + side[0], self.pos[1] + side[1]]
            block = world.get_block_at(goal_pos, False)
            if block == "puzzleBackground":
                entity_collision = False
                entities = world.loaded_chunks.get(Convert.world_to_chunk(goal_pos[0])[1]).entities
                for entity in entities:
                    if entity.pos == goal_pos:
                        entity_collision = True
                if not entity_collision:
                    self.set_pos(goal_pos)
                    return True
        return False