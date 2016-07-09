import pygame
import Game
import World
from GUI import GUI

class InventoryGUI(GUI):
    
    def __init__(self, player, imageurl):
        super(InventoryGUI, self).__init__(imageurl)
        self.player = player
        base = "img/gui/pieces/"
        self.imagepieces = [[self.load_imageurl(base + "top-left.png"), self.load_imageurl(base + "top.png"), self.load_imageurl(base + "top-right.png")],
                            [self.load_imageurl(base + "left.png"), self.load_imageurl(base + "center.png"), self.load_imageurl(base + "right.png")],
                            [self.load_imageurl(base + "bottom-left.png"), self.load_imageurl(base + "bottom.png"), self.load_imageurl(base + "bottom-right.png")]]
    
    def render(self, screen):
        super(InventoryGUI, self).render(screen)
        
        left = (Game.SCREEN_WIDTH - self.width) // 2
        top = (Game.SCREEN_HEIGHT - self.height) // 2
        
        tooltip_item = None
        inventory = self.player.inventory
        for r in range(len(inventory)):
            for c in range(len(inventory[r])):
                inv_item = inventory[r][c]
                if inv_item is not None:
                    #c and r are flipped here so it renders across then down
                    slotX = GUI.SCALING / 2 + left + c * GUI.SCALING
                    slotY = GUI.SCALING / 2 + top + r * GUI.SCALING
                    if r > 0:
                        slotY += GUI.SCALING / 8 #gap under hotbar
                    
                    drawX = slotX + GUI.SCALING / 6
                    drawY = slotY + GUI.SCALING / 6
                    screen.blit(inv_item.img, (drawX, drawY))
                    if inv_item.stackable:
                        countimg = Game.get_font().render(str(inv_item.count), 0, Game.WHITE)
                        screen.blit(countimg, (drawX, drawY))
                    rect = pygame.rect.Rect(slotX, slotY, GUI.SCALING, GUI.SCALING) #inv_item.img.get_rect().move(drawX, drawY)
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        tooltip_item = inv_item
        #TODO draw armor
        
        if tooltip_item is not None:
            #pygame.mouse.set_visible(False)
            font = Game.get_font()
            pos = pygame.mouse.get_pos()
            
            displayName = World.items[tooltip_item.name]["displayName"]
            nameimg = font.render(displayName, 0, Game.WHITE)
            name_w = nameimg.get_width()
            name_h = nameimg.get_height()
            description = World.items[tooltip_item.name]["description"]
            descimg = font.render(description, 0, Game.WHITE)
            desc_w = descimg.get_width()
            desc_h = descimg.get_height()
            
            max_w = max(name_w, desc_w)
            total_h = name_h  + desc_h
            
            #TODO wrap with newlines if anything is too long to fit on screen
            
            corner = 4 * Game.SCALE
            
            screen.blit(self.imagepieces[0][0], pos)
            for x in range(0, max_w, 2 * corner):
                screen.blit(self.imagepieces[0][1], (pos[0] + corner + x, pos[1]))
            screen.blit(self.imagepieces[0][2], (pos[0] + 3 * corner + x, pos[1]))
            
            for y in range(0, total_h, 2 * corner):
                screen.blit(self.imagepieces[1][0], (pos[0], pos[1] + corner + y))
                for x in range(0, max_w, 2 * corner):
                    screen.blit(self.imagepieces[1][1], (pos[0] + corner + x, pos[1] + corner + y))
                screen.blit(self.imagepieces[1][2], (pos[0] + 3 * corner + x, pos[1] + corner + y))
            
            screen.blit(self.imagepieces[2][0], (pos[0], pos[1] + 3 * corner + y))
            for x in range(0, max_w, 2 * corner):
                screen.blit(self.imagepieces[2][1], (pos[0] + corner + x, pos[1] + 3 * corner + y))
            screen.blit(self.imagepieces[2][2], (pos[0] + 3 * corner + x, pos[1] + 3 * corner + y))
            
            h = pos[1] + 4 * Game.SCALE
            screen.blit(nameimg, (pos[0] + corner, h))
            h += name_h
            screen.blit(descimg, (pos[0] + corner, h))
            h += desc_h