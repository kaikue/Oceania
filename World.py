import math
import Convert
import Chunk
import TwoWayList

HEIGHT = 256
SEA_LEVEL = HEIGHT / 4
SEA_FLOOR = HEIGHT * 3 / 4

class World(object):
    
    def __init__(self):
        spawn = Chunk.Chunk()
        spawn.generate_spawn()
        self.chunks = TwoWayList.TwoWayList()
        self.chunks.append(spawn)
        r1 = Chunk.Chunk()
        r1.generate_from_chunk(spawn, Chunk.LEFT)
        self.chunks.append(r1)
        r2 = Chunk.Chunk()
        r2.generate_from_chunk(r1, Chunk.LEFT)
        self.chunks.append(r2)
        r1l = Chunk.Chunk()
        r1l.generate_from_chunk(spawn, Chunk.RIGHT)
        self.chunks.prepend(r1l)
        r2l = Chunk.Chunk()
        r2l.generate_from_chunk(r1l, Chunk.RIGHT)
        self.chunks.prepend(r2l)
        self.loaded_chunks = self.chunks #improve
    
    def update(self):
        for x in range(self.loaded_chunks.first, self.loaded_chunks.last):
            check_chunk = self.loaded_chunks.get(x)
            for entity in check_chunk.entities:
                entity.update(self)
                if entity.pos[0] / Chunk.WIDTH != check_chunk.x: 
                    check_chunk.entities.remove(entity)
                    self.chunks.get(entity.pos[0] / Chunk.WIDTH).entities.append(entity)
    
    def break_block(self, player_char, mouse_pos, viewport):
        #find nearest breakable block based on angle from player pos to mouse pos (raycasting?)
        #begin breaking it
        x_diff = mouse_pos[0] - Convert.pixels_to_viewport(player_char.bounding_box.topleft, viewport)[0]
        y_diff = mouse_pos[1] - Convert.pixels_to_viewport(player_char.bounding_box.topleft, viewport)[1]
        angle = math.atan2(-y_diff, x_diff) #not sure if y should be negative
        print(x_diff, y_diff, angle)
    
    def render(self, screen, viewport):
        left_chunk = Convert.world_to_chunk(Convert.pixel_to_world(viewport.x))[1]
        right_chunk = left_chunk + Convert.world_to_chunk(Convert.pixel_to_world(viewport.width))[1] + 2
        #print(left_chunk, right_chunk)
        for i in range(left_chunk, right_chunk):
            try:
                self.loaded_chunks.get(i).render(screen, viewport)
            except IndexError:
                pass
