import pygame
import Game
import gui.GUI as GUI
from gui.InventoryGUI import InventoryGUI
import Images

class ChestGUI(InventoryGUI):
    
    def __init__(self, chest_inventory, player, imageurl):
        super(ChestGUI, self).__init__(player, imageurl)
        self.chest_inventory = chest_inventory
        self.transfer_down_image = Images.load_imageurl("img/gui/arrow_down.png")
        self.transfer_up_image = Images.load_imageurl("img/gui/arrow_up.png")
        self.merge_down_image = Images.load_imageurl("img/gui/arrow_down_line.png")
        self.merge_up_image = Images.load_imageurl("img/gui/arrow_up_line.png")
        self.transfer_down_position = (self.left + GUI.SCALING * 5 / 8, self.top + GUI.SCALING * 5 / 8)
        self.transfer_up_position = (self.left + GUI.SCALING * 5 / 8, self.top + GUI.SCALING * 39 / 8)
    
    def render(self, screen):
        super(InventoryGUI, self).render(screen)
        
        self.chest_inventory.render(self.left, self.top, screen, False, self.moving_item)
        self.player.inventory.render(self.left, self.top + GUI.SCALING * 51 / 12, screen, True, self.moving_item)
        
        shift = Game.is_shift_pressed()
        if shift:
            screen.blit(self.merge_down_image, self.transfer_down_position)
            screen.blit(self.merge_up_image, self.transfer_up_position)
        else:
            screen.blit(self.transfer_down_image, self.transfer_down_position)
            screen.blit(self.transfer_up_image, self.transfer_up_position)
        
        mouse_pos = pygame.mouse.get_pos()
        if self.in_transfer_button(self.transfer_down_position, mouse_pos):
            tooltip = "Take Merge" if shift else "Take All"
            self.chest_inventory.draw_tooltip(screen, tooltip)
        if self.in_transfer_button(self.transfer_up_position, mouse_pos):
            tooltip = "Deposit Merge" if shift else "Deposit All"
            self.chest_inventory.draw_tooltip(screen, tooltip)
        
        self.draw_moving_item(screen)
    
    def in_transfer_button(self, button_position, target_position):
        return button_position[0] <= target_position[0] <= button_position[0] + GUI.SCALING * 3 / 4 and \
            button_position[1] <= target_position[1] <= button_position[1] + GUI.SCALING * 3 / 4
    
    def has_item_of_type(self, inv, item):
        if item is None:
            return False
        for row in inv.items:
            for itemstack in row:
                if (itemstack is not None) and (itemstack.name == item.name):
                    return True
        return False
    
    def transfer_all_from(self, from_inv, to_inv, shift):
        for r in range(len(from_inv.items)):
            for c in range(len(from_inv.items[r])):
                slot = (r, c)
                if self.has_item_of_type(to_inv, from_inv.items[r][c]) or not shift:
                    self.click_slot(slot, 1, True, from_inv, to_inv)
    
    def click(self, pos, button, shift):
        if self.in_transfer_button(self.transfer_down_position, pos):
            self.transfer_all_from(self.chest_inventory, self.player.inventory, shift)
        
        if self.in_transfer_button(self.transfer_up_position, pos):
            self.transfer_all_from(self.player.inventory, self.chest_inventory, shift)
        
        slot = self.chest_inventory.slot_at(pos, self.left, self.top, False)
        self.click_slot(slot, button, shift, self.chest_inventory, self.player.inventory)
        
        slot = self.player.inventory.slot_at(pos, self.left, self.top + GUI.SCALING * 13 // 3, True)
        self.click_slot(slot, button, shift, self.player.inventory, self.chest_inventory)