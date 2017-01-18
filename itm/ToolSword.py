from itm import ItemTool


class ToolSword(ItemTool.ItemTool):
    
    def get_attack_damage(self):
        return 5
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        #TODO: sweep attack
        pass