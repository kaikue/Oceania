import pygame
import Game
import World
import GUI
import ItemStack
import Images

class Inventory(object):
    
    def __init__(self, rows, cols):
        self.items = []
        for _ in range(rows):
            self.items.append([None] * cols)
    
    def insert(self, itemdrop):
        for row in self.items:
            for i in range(len(row)):
                if row[i] is None:
                    item = ItemStack.itemstack_from_name(itemdrop.name)
                    item.data = itemdrop.data
                    row[i] = item
                    return True
                elif row[i].can_stack(itemdrop):
                    row[i].count += 1
                    return True
        return False
    
    def __getitem__(self, i):
        return self.items[i]
    
    def __setitem__(self, i, value):
        self.items[i] = value
    
    def render(self, left, top, screen, hotbargap):
        font = Game.get_font()
        mouse_pos = pygame.mouse.get_pos()
           
        tooltip_item = None
        for r in range(len(self.items)):
            for c in range(len(self.items[r])):
                inv_item = self.items[r][c]
                if inv_item is not None:
                    #c and r are flipped here so it renders across then down
                    slotX = GUI.SCALING / 2 + left + c * GUI.SCALING
                    slotY = GUI.SCALING / 2 + top + r * GUI.SCALING
                    if r > 0 and hotbargap:
                        slotY += GUI.SCALING / 8 #gap under hotbar
                    
                    inv_item.render(slotX, slotY, screen)
                    
                    rect = pygame.rect.Rect(slotX, slotY, GUI.SCALING, GUI.SCALING)
                    if rect.collidepoint(mouse_pos):
                        tooltip_item = inv_item
                        highlight_pos = (slotX, slotY)
        #TODO draw armor if not none
        
        if tooltip_item is not None:
            screen.blit(Images.highlight_image, highlight_pos)
            
            text = World.items[tooltip_item.name]["description"]
            if isinstance(text, str):
                text = [text]
            else:
                text = text.copy()
            displayName = World.items[tooltip_item.name]["displayName"]
            text.insert(0, displayName)
            text_image = GUI.render_string_array(text, font, 0, Game.WHITE)
            
            width = text_image.get_width()
            height = text_image.get_height()
            corner = 4 * Game.SCALE
            
            pos = (mouse_pos[0] + corner, mouse_pos[1])
            
            #if too long, flip it to the other side of the mouse
            if pos[0] + width + 2 * corner > Game.SCREEN_WIDTH:
                pos = (max(pos[0] - width - 4 * corner, 0), pos[1]) #gap for mouse
            if pos[1] + height + 2 * corner > Game.SCREEN_HEIGHT:
                pos = (pos[0], pos[1] - height - 2 * corner)
            
            screen.blit(Images.tooltip_pieces[0][0], pos)
            for x in range(0, width, 2 * corner):
                screen.blit(Images.tooltip_pieces[0][1], (pos[0] + corner + x, pos[1]))
            screen.blit(Images.tooltip_pieces[0][2], (pos[0] + 3 * corner + x, pos[1]))
            
            for y in range(0, height, 2 * corner):
                screen.blit(Images.tooltip_pieces[1][0], (pos[0], pos[1] + corner + y))
                for x in range(0, width, 2 * corner):
                    screen.blit(Images.tooltip_centers[((x + y) // (2 * corner)) % 4], (pos[0] + corner + x, pos[1] + corner + y))
                screen.blit(Images.tooltip_pieces[1][2], (pos[0] + 3 * corner + x, pos[1] + corner + y))
            
            screen.blit(Images.tooltip_pieces[2][0], (pos[0], pos[1] + 3 * corner + y))
            for x in range(0, width, 2 * corner):
                screen.blit(Images.tooltip_pieces[2][1], (pos[0] + corner + x, pos[1] + 3 * corner + y))
            screen.blit(Images.tooltip_pieces[2][2], (pos[0] + 3 * corner + x, pos[1] + 3 * corner + y))
            
            screen.blit(text_image, (pos[0] + corner, pos[1] + corner))