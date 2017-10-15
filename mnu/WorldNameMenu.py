import pygame
import Game
import Images
from mnu.Menu import Menu, Label
from mnu.CharacterMenu import CharacterMenu
import Button

class WorldNameMenu(Menu):
    
    def __init__(self, prev_menu):
        
        #TODO: name field should be validated- not empty, not the same as any existing world
        #don't let the next button work until it is valid
        
        self.name_textfield = TextField((Game.SCREEN_WIDTH / 2 - TextField.WIDTH / 2, Game.SCREEN_HEIGHT // 3))
        self.name_textfield.select()
        self.seed_textfield = TextField((Game.SCREEN_WIDTH / 2 - TextField.WIDTH / 2, Game.SCREEN_HEIGHT // 2))
        self.text_fields = [self.name_textfield, self.seed_textfield]
        
        back_button = Button.Button((Game.SCREEN_WIDTH / 4 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Cancel", "menu")
        back_button.next_menu = prev_menu
        
        next_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Next", "menu")
        next_button.next_menu = CharacterMenu(self)
        
        title_label = Label("World Settings", (Game.SCREEN_WIDTH / 2 - Label.WIDTH / 2, Game.SCREEN_HEIGHT // 15))
        name_label = Label("Name", (Game.SCREEN_WIDTH // 5 - Label.SMALL_WIDTH / 2, Game.SCREEN_HEIGHT // 3), True)
        seed_label = Label("Seed", (Game.SCREEN_WIDTH // 5 - Label.SMALL_WIDTH / 2, Game.SCREEN_HEIGHT // 2), True)
        
        super().__init__([back_button, next_button], [title_label, name_label, seed_label], True)
    
    def mouse_release(self):
        for text_field in self.text_fields:
            text_field.selected = False
            if text_field.get_rect().collidepoint(pygame.mouse.get_pos()):
                text_field.select()
        super().mouse_release()
    
    def type(self, char):
        for text_field in self.text_fields:
            if text_field.selected:
                text_field.type(char)
    
    def delete(self):
        for text_field in self.text_fields:
            if text_field.selected:
                text_field.delete()
    
    def render(self, screen):
        Menu.render(self, screen)
        for text_field in self.text_fields:
            text_field.render(screen)

class TextField(object):
    
    WIDTH = 96 * Game.SCALE
    HEIGHT = 32 * Game.SCALE
    X_OFFSET = 3 * Game.SCALE
    Y_OFFSET = 3 * Game.SCALE
    
    def __init__(self, pos):
        self.pos = pos
        self.selected = False
        self.text = ""
        self.img = Images.load_imageurl("img/gui/textfield.png")
        self.font = Game.get_font()
    
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], TextField.WIDTH, TextField.HEIGHT)
    
    def select(self):
        self.selected = True
    
    def type(self, char):
        self.text += char
    
    def delete(self):
        self.text = self.text[:-1]
    
    def render(self, screen):
        screen.blit(self.img, self.pos)
        color = Game.LIGHT_GRAY
        
        text_to_render = self.text
        if len(text_to_render) == 0 and self.selected:
            text_to_render = "|"
        
        text_img = self.font.render(text_to_render, 0, color)
        x = self.pos[0] + TextField.X_OFFSET
        y = self.pos[1] + TextField.Y_OFFSET
        screen.blit(text_img, (x, y))