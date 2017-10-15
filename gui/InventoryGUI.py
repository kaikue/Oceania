import pygame
import Game
import Convert
from ent.ItemDrop import ItemDrop
from itm import ItemStack
import gui.GUI as GUI

class InventoryGUI(GUI.GUI):
    
    def __init__(self, player, imageurl):
        super().__init__(imageurl)
        self.player = player
        self.left = (Game.SCREEN_WIDTH - self.width) // 2
        self.top = (Game.SCREEN_HEIGHT - self.height) // 2
        self.moving_item = None
    
    def render(self, screen):
        super().render(screen)
        self.player.inventory.render(self.left, self.top, screen, True, self.moving_item)
        self.draw_moving_item(screen)
    
    def draw_moving_item(self, screen):
        if self.moving_item is not None:
            self.moving_item.render(pygame.mouse.get_pos(), screen)
    
    def click(self, pos, right, shift):
        slot = self.player.inventory.slot_at(pos, self.left, self.top, True)
        self.click_slot(slot, right, shift, self.player.inventory, None)
    
    def click_slot(self, slot, button, shift, clicked_inventory, other_inventory):
        if slot is None:
            return
        
        clicked = clicked_inventory[slot[0]][slot[1]]
        
        if button == 1: #left click
            if shift:
                if other_inventory is not None and clicked is not None: #insert stack
                    clicked = other_inventory.insert(clicked)
            else:
                if self.moving_item is not None and clicked is not None: #stack and swap
                    copy = clicked.copy_one()
                    if clicked.can_stack(copy):
                        while clicked is not None and self.moving_item.can_stack(copy):
                            self.moving_item.count += 1
                            clicked = clicked.take_one()
                clicked, self.moving_item = self.moving_item, clicked
        
        elif button == 2: #scroll wheel click
            if other_inventory is not None and clicked is not None: #insert all with same name
                for row in clicked_inventory:
                    for i in range(len(row)):
                        if row[i] is not None and row[i].name == clicked.name:
                            row[i] = other_inventory.insert(row[i])
                if clicked.count == 0: #need to check for this since we didn't explicitly set it
                    clicked = None
        
        elif button == 3: #right click
            if shift:
                if other_inventory is not None and clicked is not None: #insert half
                    clicked, to_insert = clicked.take_half()
                    if to_insert is not None:
                        to_insert = other_inventory.insert(to_insert)
                        if to_insert is not None:
                            if clicked is None:
                                clicked = to_insert.copy_one()
                            clicked.count += to_insert.count
            else:
                if self.moving_item is not None: #place 1
                    if clicked == None:
                        clicked = self.moving_item.copy_one()
                        self.moving_item = self.moving_item.take_one()
                    else:
                        if self.moving_item.can_stack(clicked):
                            clicked.count += 1
                            self.moving_item = self.moving_item.take_one()
                else:
                    if clicked is not None: #take half
                        clicked, self.moving_item = clicked.take_half()
        
        else:
            #transfer in direction of scroll (player inventory on bottom)
            transfer = button == 4
            if other_inventory == self.player.inventory:
                transfer = not transfer
            
            if transfer:
                if other_inventory is not None and clicked is not None: #transfer one
                    if other_inventory.insert_single(clicked):
                        clicked.count -= 1
                        if clicked.count == 0:
                            clicked = None
        
            else:
                if other_inventory is not None and clicked is not None and clicked.count < ItemStack.MAX_STACK_SIZE: #retrieve one
                    done = False
                    for row in other_inventory:
                        for i in range(len(row)):
                            if not done and row[i] is not None and row[i].name == clicked.name:
                                clicked.count += 1
                                row[i].count -= 1
                                if row[i].count == 0:
                                    row[i] = None
                                done = True
        
        clicked_inventory[slot[0]][slot[1]] = clicked
    
    def close(self, world):
        if self.moving_item is not None:
            chunk = world.loaded_chunks.get(Convert.world_to_chunk(self.player.pos[0])[1])
            chunk.entities.append(ItemDrop(self.player.pos, self.moving_item.name, self.moving_item.data, self.moving_item.count))
            self.moving_item = None