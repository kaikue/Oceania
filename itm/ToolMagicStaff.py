import math
import Convert
from itm import ItemTool
from ent import DamageSource
from ent.EntityEnemy import EntityEnemy

class ToolMagicStaff(ItemTool.ItemTool):
    
    PROJECTILE_SPEED = 0.3
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        #TODO: different types of projectile
        pos = player.pos[:]
        damage_source = DamageSource.DamageSource(pos, 5, 0.5, "img/projectiles/orb.png", player, 60)
        pixel_player_pos = Convert.world_to_viewport(pos, viewport)
        difference = (mouse_pos[0] - pixel_player_pos[0],
                      mouse_pos[1] - pixel_player_pos[1])
        length = math.sqrt(difference[0] ** 2 + difference[1] ** 2)
        normalized = [difference[0] / length * ToolMagicStaff.PROJECTILE_SPEED, 
                      difference[1] / length * ToolMagicStaff.PROJECTILE_SPEED]
        damage_source.vel = [player.vel[0] + normalized[0],
                             player.vel[1] + normalized[1]]
        world.create_entity(damage_source)
        
        world.create_entity(EntityEnemy(Convert.viewport_to_world(mouse_pos, viewport), "img/blob.png", 10)) #TODO: remove