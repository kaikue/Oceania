import Game
import Convert
import Entity

class EntityPuzzlePiece(Entity.Entity):
    ANIMATION_MAX = 50
    
    def __init__(self, pos, puzzle_pos):
        #puzzle_pos must be a pair of ints from 0 to 3, not including (0, 0)
        self.puzzle_pos = puzzle_pos
        imageurl = "img/puzzle/puzzle_" + str(puzzle_pos[1]) + "_" + str(puzzle_pos[0]) + ".png"
        super(EntityPuzzlePiece, self).__init__(pos, imageurl, False)
        self.animating = False
        self.animation_stage = 0
        self.locked = False
        self.old_pos = pos
    
    def update(self, world):
        if self.animating:
            self.animation_stage += 1
            if self.animation_stage == EntityPuzzlePiece.ANIMATION_MAX:
                self.animating = False
                self.animation_stage = 0
    
    def interact(self, player, item):
        if self.locked or self.animating:
            return False
        
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
                    self.old_pos = self.pos
                    self.animating = True
                    self.set_pos(goal_pos)
                    return True
        return False
    
    def render(self, screen, pos):
        if self.animating:
            old_pixel_pos = Convert.world_to_pixels(self.old_pos)
            new_pixel_pos = Convert.world_to_pixels(self.pos)
            animation_ratio = 1 - (self.animation_stage / EntityPuzzlePiece.ANIMATION_MAX)
            difference = ((old_pixel_pos[0] - new_pixel_pos[0]) * animation_ratio,
                          (old_pixel_pos[1] - new_pixel_pos[1]) * animation_ratio)
            screen.blit(self.img, (pos[0] + difference[0], pos[1] + difference[1]))
        else:
            screen.blit(self.img, pos)