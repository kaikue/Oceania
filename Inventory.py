import math
import pygame
import Game
import World
import gui.GUI as GUI
import Images

HOTBAR_GAP = GUI.SCALING // 8
TOOLTIP_GAP = 5 * Game.SCALE #between name and description

class Inventory(object):
    
    def __init__(self, rows, cols):
        self.items = []
        for _ in range(rows):
            self.items.append([None] * cols)
    
    def insert_single(self, itemstack):
        item = itemstack.copy_one()
        #first look for places that can stack
        for row in self.items:
            for i in range(len(row)):
                if row[i] is not None and row[i].can_stack(item):
                    row[i].count += 1
                    return True
        #then look for empty slots
        for row in self.items:
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = item
                    return True
        return False
    
    def insert(self, itemstack):
        while self.insert_single(itemstack):
            itemstack.count -= 1
            if itemstack.count == 0:
                return None
        return itemstack
    
    def __getitem__(self, i):
        return self.items[i]
    
    def __setitem__(self, i, value):
        self.items[i] = value
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.items == other.items
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def slot_at(self, pos, left, top, hotbargap):
        #TODO: give armor slot if necessary... negative coordinate?
        pos = (pos[0] - left - GUI.SCALING * 13 // 8, pos[1] - top - GUI.SCALING // 2)
        if hotbargap and pos[1] > GUI.SCALING:
            pos = (pos[0], pos[1] - HOTBAR_GAP)
        row = pos[1] // GUI.SCALING
        col = pos[0] // GUI.SCALING
        if not (0 <= row < len(self.items) and 0 <= col < len(self.items[row])):
            return None
        else:
            return (row, col)
    
    def render(self, left, top, screen, hotbargap, item_to_skip = None):
        mouse_pos = pygame.mouse.get_pos()
        tooltip_item = None
        for r in range(len(self.items)):
            for c in range(len(self.items[r])):
                inv_item = self.items[r][c]
                if inv_item is not None and inv_item is not item_to_skip:
                    #c and r are flipped here so it renders across then down
                    slotX = left + GUI.SCALING * 13 / 8 +  c * GUI.SCALING
                    slotY = top + GUI.SCALING / 2 + r * GUI.SCALING
                    if r > 0 and hotbargap:
                        slotY += HOTBAR_GAP
                    
                    inv_item.render((slotX, slotY), screen)
                    
                    rect = pygame.rect.Rect(slotX, slotY, GUI.SCALING, GUI.SCALING)
                    if rect.collidepoint(mouse_pos):
                        tooltip_item = inv_item
                        highlight_pos = (slotX, slotY)
        #TODO: draw armor if not none
        
        if tooltip_item is not None and item_to_skip is None:
            screen.blit(Images.highlight_image, highlight_pos)
            
            display_name = World.items[tooltip_item.name]["displayName"]
            description = World.items[tooltip_item.name]["description"]
            self.draw_tooltip(screen, display_name, description)
    
    def draw_tooltip(self, screen, name, description = []):
        font = Game.get_font(False)
        big_font = Game.get_font(True)
        mouse_pos = pygame.mouse.get_pos()
        
        name_image = GUI.render_string_array([name], big_font, 0, Game.WHITE)
        desc_image = GUI.render_string_array(description, font, 0, Game.WHITE)
        name_width = name_image.get_width()
        name_height = name_image.get_height()
        desc_width = desc_image.get_width()
        desc_height = desc_image.get_height()
        width = max(name_width, desc_width)
        height = name_height
        if desc_height > 0:
            height += TOOLTIP_GAP + desc_height
        corner = 4 * Game.SCALE
        edge = 2 * corner
        
        pos = (mouse_pos[0] + corner, mouse_pos[1])
        
        #if too long, flip it to the other side of the mouse
        if pos[0] + width + 2 * corner > Game.SCREEN_WIDTH:
            pos = (max(pos[0] - width - 4 * corner, 0), pos[1]) #gap for mouse
        if pos[1] + height + 2 * corner > Game.SCREEN_HEIGHT:
            pos = (pos[0], pos[1] - height - 2 * corner)
        
        #top border
        screen.blit(Images.tooltip_pieces[0][0], pos)
        for x in range(0, width, edge):
            screen.blit(Images.tooltip_pieces[0][1], (pos[0] + corner + x, pos[1]))
        screen.blit(Images.tooltip_pieces[0][2], (pos[0] + 3 * corner + x, pos[1]))
        
        #middle
        slices = math.ceil(height / edge)
        for s in range(slices):
            y = height * s // slices
            screen.blit(Images.tooltip_pieces[1][0], (pos[0], pos[1] + corner + y))
            for x in range(0, width, edge):
                screen.blit(Images.tooltip_centers[((x + y) // edge) % 4], (pos[0] + corner + x, pos[1] + corner + y))
            screen.blit(Images.tooltip_pieces[1][2], (pos[0] + 3 * corner + x, pos[1] + corner + y))
        
        #bottom border
        y = corner + height
        screen.blit(Images.tooltip_pieces[2][0], (pos[0], pos[1] + y))
        for x in range(0, width, edge):
            screen.blit(Images.tooltip_pieces[2][1], (pos[0] + corner + x, pos[1] + y))
        screen.blit(Images.tooltip_pieces[2][2], (pos[0] + 3 * corner + x, pos[1] + y))
        
        #text
        screen.blit(name_image, (pos[0] + corner, pos[1] + corner))
        screen.blit(desc_image, (pos[0] + corner, pos[1] + corner + name_height + TOOLTIP_GAP))