from itm import ItemTool


class ToolPickaxe(ItemTool.ItemTool):
    
    def get_break_speed(self):
        return 2
    
    def get_harvest_level(self):
        return 1