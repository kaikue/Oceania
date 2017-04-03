import Game
import Images
import gui.GUI as GUI


class HotbarGUI(GUI.GUI):
    
    def __init__(self, player, imageurl):
        super(HotbarGUI, self).__init__(imageurl)
        self.player = player
        self.img_heart_full = Images.load_imageurl("img/gui/heart.png")
        self.img_heart_empty = Images.load_imageurl("img/gui/heart_empty.png")
    
    def render(self, screen):
        left = (Game.get_screen_width() - self.width) // 2
        top = 8 * Game.get_scale()
        screen.blit(self.img, (left, top))
        
        for c in range(len(self.player.inventory[0])):
            inv_item = self.player.inventory[0][c]
            if inv_item is not None:
                inv_item.render((left + c * GUI.get_scaling(), top), screen)
        
        screen.blit(Images.highlight_image, (left + GUI.get_scaling() * self.player.selected_slot, top))
        
        #draw the hearts
        for i in range(self.player.health):
            screen.blit(self.img_heart_full, (left + i * GUI.get_scaling() / 2, GUI.get_scaling() + top * 3 / 2))
        for i in range(self.player.health, self.player.max_health):
            screen.blit(self.img_heart_empty, (left + i * GUI.get_scaling() / 2, GUI.get_scaling() + top * 3 / 2))