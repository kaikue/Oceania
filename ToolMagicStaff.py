import ItemTool


class ToolMagicStaff(ItemTool.ItemTool):
    
    def use_discrete(self, world, player, mouse_pos, viewport):
        #create a bolt of energy facing towards direction
        print("using the staff")