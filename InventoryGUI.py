import pygame
import Game
import World
import GUI

class InventoryGUI(GUI.GUI):
    
    def __init__(self, player, imageurl):
        super(InventoryGUI, self).__init__(imageurl)
        self.player = player
        base = "img/gui/pieces/"
        self.imagepieces = [[self.load_imageurl(base + "top-left.png"), self.load_imageurl(base + "top.png"), self.load_imageurl(base + "top-right.png")],
                            [self.load_imageurl(base + "left.png"), None, self.load_imageurl(base + "right.png")],
                            [self.load_imageurl(base + "bottom-left.png"), self.load_imageurl(base + "bottom.png"), self.load_imageurl(base + "bottom-right.png")]]
        self.centers = [self.load_imageurl(base + "center0.png"), 
                        self.load_imageurl(base + "center1.png"), 
                        self.load_imageurl(base + "center2.png"), 
                        self.load_imageurl(base + "center3.png")]
    
    def render(self, screen):
        super(InventoryGUI, self).render(screen)
        
        left = (Game.SCREEN_WIDTH - self.width) // 2
        top = (Game.SCREEN_HEIGHT - self.height) // 2
        
        font = Game.get_font()
        mouse_pos = pygame.mouse.get_pos()
           
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
                        countimg = font.render(str(inv_item.count), 0, Game.WHITE)
                        screen.blit(countimg, (slotX + 2 * Game.SCALE, slotY + 2 * Game.SCALE))
                    rect = pygame.rect.Rect(slotX, slotY, GUI.SCALING, GUI.SCALING)
                    if rect.collidepoint(mouse_pos):
                        tooltip_item = inv_item
                        highlight_pos = (slotX, slotY)
        #TODO draw armor
        
        if tooltip_item is not None:
            screen.blit(self.highlightimg, highlight_pos)
            
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
            
            screen.blit(self.imagepieces[0][0], pos)
            for x in range(0, width, 2 * corner):
                screen.blit(self.imagepieces[0][1], (pos[0] + corner + x, pos[1]))
            screen.blit(self.imagepieces[0][2], (pos[0] + 3 * corner + x, pos[1]))
            
            for y in range(0, height, 2 * corner):
                screen.blit(self.imagepieces[1][0], (pos[0], pos[1] + corner + y))
                for x in range(0, width, 2 * corner):
                    screen.blit(self.centers[((x + y) // (2 * corner)) % 4], (pos[0] + corner + x, pos[1] + corner + y))
                screen.blit(self.imagepieces[1][2], (pos[0] + 3 * corner + x, pos[1] + corner + y))
            
            screen.blit(self.imagepieces[2][0], (pos[0], pos[1] + 3 * corner + y))
            for x in range(0, width, 2 * corner):
                screen.blit(self.imagepieces[2][1], (pos[0] + corner + x, pos[1] + 3 * corner + y))
            screen.blit(self.imagepieces[2][2], (pos[0] + 3 * corner + x, pos[1] + 3 * corner + y))
            
            screen.blit(text_image, (pos[0] + corner, pos[1] + corner))