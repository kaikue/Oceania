import pygame
import Game
import Images

WIDTH = 96 * Game.SCALE
HEIGHT = 32 * Game.SCALE

def music_message(enabled):
    return ("Disable" if enabled else "Enable") + " Music"

class Button(object):
    
    def __init__(self, pos, text, effect):
        self.pos = pos
        self.text = text
        self.effect = effect
        self.pressed = False
        self.font = Game.get_font()
        self.unpressed_image = Images.load_imageurl("img/gui/button_up.png")
        self.hovered_image = Images.load_imageurl("img/gui/button_hover.png")
        self.pressed_image = Images.load_imageurl("img/gui/button_down.png")
    
    def activate(self):
        if self.effect == "menu":
            Game.set_menu(self.next_menu)
        elif self.effect == "resume":
            Game.unpause()
        elif self.effect == "quit":
            Game.close()
        elif self.effect == "options":
            Game.show_options()
        elif self.effect == "music":
            enabled = Game.toggle_music()
            self.text = music_message(enabled)
        elif self.effect == "load_world":
            Game.start_setup()
            Game.load_world(self.world_to_load)
            Game.finish_setup()
        elif self.effect == "scroll_worlds":
            self.world_menu.scroll_by(self.scroll_amount)
            self.world_menu.display_worlds()
        elif self.effect == "create":
            player_options = self.character_menu.options
            name = self.world_menu.name
            seed = self.world_menu.seed
            Game.start_setup()
            Game.generate_world(name, seed, player_options)
            Game.finish_setup()
        elif self.effect == "random":
            self.menu.randomize()
        
        self.pressed = False
    
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], WIDTH, HEIGHT)
    
    def mouse_hover(self):
        return self.get_rect().collidepoint(pygame.mouse.get_pos())
    
    def render(self, screen):
        color = Game.LIGHT_GRAY
        if self.mouse_hover():
            if self.pressed:
                img = self.pressed_image
                color = Game.MEDIUM_GRAY
            else:
                img = self.hovered_image
        else:
            img = self.unpressed_image
        screen.blit(img, self.pos)
        text_img = self.font.render(self.text, 0, color)
        h = text_img.get_height() - (2 * Game.SCALE)
        w = text_img.get_width()
        screen.blit(text_img, (self.pos[0] + (WIDTH - w) / 2, self.pos[1] + (HEIGHT - h) / 2))