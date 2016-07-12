import gui.GUI as GUI
from gui.InventoryGUI import InventoryGUI

class ChestGUI(InventoryGUI):
    
    def __init__(self, chest_inventory, player, imageurl):
        super(ChestGUI, self).__init__(player, imageurl)
        self.chest_inventory = chest_inventory
    
    def render(self, screen):
        super(InventoryGUI, self).render(screen)
        
        self.chest_inventory.render(self.left, self.top, screen, False, self.moving_item)
        self.player.inventory.render(self.left, self.top + GUI.SCALING * 51 / 12, screen, True, self.moving_item)
        
        self.draw_moving_item(screen)
    
    def click(self, pos, right, shift):
        slot = self.chest_inventory.slot_at(pos, self.left, self.top, True)
        self.click_slot(slot, right, shift, self.chest_inventory, self.player.inventory)
        
        slot = self.player.inventory.slot_at(pos, self.left, self.top + GUI.SCALING * 13 // 3, True)
        self.click_slot(slot, right, shift, self.player.inventory, self.chest_inventory)