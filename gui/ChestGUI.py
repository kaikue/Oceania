import gui.GUI as GUI
from gui.InventoryGUI import InventoryGUI
import Images

class ChestGUI(InventoryGUI):
    
    def __init__(self, chest_inventory, player, imageurl):
        super(ChestGUI, self).__init__(player, imageurl)
        self.chest_inventory = chest_inventory
        self.transfer_down_image = Images.load_imageurl("img/gui/arrow_down.png")
        self.transfer_up_image = Images.load_imageurl("img/gui/arrow_up.png")
        self.transfer_down_position = (self.left + GUI.SCALING * 5 / 8, self.top + GUI.SCALING * 5 / 8)
        self.transfer_up_position = (self.left + GUI.SCALING * 5 / 8, self.top + GUI.SCALING * 39 / 8)
    
    def render(self, screen):
        super(InventoryGUI, self).render(screen)
        
        self.chest_inventory.render(self.left, self.top, screen, False, self.moving_item)
        self.player.inventory.render(self.left, self.top + GUI.SCALING * 51 / 12, screen, True, self.moving_item)
        
        screen.blit(self.transfer_down_image, self.transfer_down_position)
        screen.blit(self.transfer_up_image, self.transfer_up_position)
        
        self.draw_moving_item(screen)
    
    def click(self, pos, right, shift):
        if self.transfer_down_position[0] <= pos[0] <= self.transfer_down_position[0] + GUI.SCALING * 3 / 4 and \
            self.transfer_down_position[1] <= pos[1] <= self.transfer_down_position[1] + GUI.SCALING * 3 / 4:
            for r in range(len(self.chest_inventory.items)):
                for c in range(len(self.chest_inventory.items[r])):
                    slot = (r, c)
                    self.click_slot(slot, 1, True, self.chest_inventory, self.player.inventory)
        
        if self.transfer_up_position[0] <= pos[0] <= self.transfer_up_position[0] + GUI.SCALING * 3 / 4 and \
            self.transfer_up_position[1] <= pos[1] <= self.transfer_up_position[1] + GUI.SCALING * 3 / 4:
            for r in range(len(self.player.inventory.items)):
                for c in range(len(self.player.inventory.items[r])):
                    slot = (r, c)
                    self.click_slot(slot, 1, True, self.player.inventory, self.chest_inventory)
        
        slot = self.chest_inventory.slot_at(pos, self.left, self.top, True)
        self.click_slot(slot, right, shift, self.chest_inventory, self.player.inventory)
        
        slot = self.player.inventory.slot_at(pos, self.left, self.top + GUI.SCALING * 13 // 3, True)
        self.click_slot(slot, right, shift, self.player.inventory, self.chest_inventory)