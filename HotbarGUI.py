import pygame

from GUI import GUI
import Game
import World


class HotbarGUI(GUI):
    
    def __init__(self, player, imageurl):
        self.player = player
        super(HotbarGUI, self).__init__(imageurl)
        self.img_heart_full = self.load_extra_image("img/gui/heart.png")
        self.img_heart_empty = self.load_extra_image("img/gui/heart_empty.png")
    
    def render(self, screen):
        left = (Game.SCREEN_WIDTH - self.width) // 2
        top = 16
        screen.blit(self.img, (left, top))
        
        for c in range(len(self.player.inventory[0])):
            inv_item = self.player.inventory[0][c]
            if inv_item is not None:
                screen.blit(World.block_icons[True][World.get_block_id(inv_item.itemtype)], (GUI.SCALING / 6 + left + c * GUI.SCALING, GUI.SCALING / 6 + top))
                countimg = Game.get_font().render(str(inv_item.count), 0, Game.WHITE)
                screen.blit(countimg, (left + c * GUI.SCALING, top))
            #TODO make it work for items too
        #highlight selected item
        pygame.draw.rect(screen, Game.WHITE, pygame.Rect(left + GUI.SCALING * self.player.selected_slot, top, GUI.SCALING, GUI.SCALING), 2)
        
        #draw the hearts
        for i in range(self.player.health):
            screen.blit(self.img_heart_full, (left + i * GUI.SCALING / 2, GUI.SCALING + top * 3 / 2))
        for i in range(self.player.health, self.player.max_health):
            screen.blit(self.img_heart_empty, (left + i * GUI.SCALING / 2, GUI.SCALING + top * 3 / 2))