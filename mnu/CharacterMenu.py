import random
import Game
import Images
from mnu.Menu import Menu, Label
import Button
import Player

CATEGORIES = (Player.HAIR_COLORS, Player.HAIR_LENGTHS, Player.BODY_COLORS, Player.TAIL_COLORS)

class CharacterMenu(Menu):
    
    def __init__(self, prev_menu):
        
        self.options = [0, 0, 0, 0]
        
        random_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, self.get_category_y(-1)), "Randomize", "random")
        random_button.menu = self
        
        l_hair_color_button = self.make_category_button(False, 0)
        r_hair_color_button = self.make_category_button(True, 0)
        l_hair_style_button = self.make_category_button(False, 1)
        r_hair_style_button = self.make_category_button(True, 1)
        l_body_button = self.make_category_button(False, 2)
        r_body_button = self.make_category_button(True, 2)
        l_tail_button = self.make_category_button(False, 3)
        r_tail_button = self.make_category_button(True, 3)
        
        back_button = Button.Button((Game.SCREEN_WIDTH / 4 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Back", "menu")
        back_button.next_menu = prev_menu
        
        create_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Create", "create")
        create_button.character_menu = self
        create_button.world_menu = prev_menu
        
        title_label = Label("Customize Character", (Game.SCREEN_WIDTH / 2 - Label.WIDTH / 2, Game.SCREEN_HEIGHT // 15))
        label_x = Game.SCREEN_WIDTH // 5 - Label.SMALL_WIDTH / 2
        hair_color_label = Label("Hair Color", (label_x, self.get_category_y(0)), True)
        hair_style_label = Label("Hairstyle", (label_x, self.get_category_y(1)), True)
        body_label = Label("Body", (label_x, self.get_category_y(2)), True)
        tail_label = Label("Tail", (label_x, self.get_category_y(3)), True)
        
        self.load_images()
        
        super(CharacterMenu, self).__init__([random_button, 
                                             l_hair_color_button, r_hair_color_button,
                                             l_hair_style_button, r_hair_style_button,
                                             l_body_button, r_body_button,
                                             l_tail_button, r_tail_button,
                                             back_button, create_button],
                                            [title_label, 
                                             hair_color_label, hair_style_label,
                                             body_label, tail_label], True)
    
    def get_category_y(self, category):
        return Game.SCREEN_HEIGHT * 3 // 10 + category * (Button.HEIGHT + Game.SCALE)
    
    def make_category_button(self, right, category):
        x = Game.SCREEN_WIDTH * 2 // 3 - Button.SMALL_WIDTH / 2 if right else Game.SCREEN_WIDTH * 1 // 3 - Button.SMALL_WIDTH / 2
        y = self.get_category_y(category)
        text = ">" if right else "<"
        button = Button.Button((x, y), text, "change_option", True)
        button.menu = self
        button.category = category
        button.amount = 1 if right else -1
        return button
    
    def load_images(self):
        self.images = [[], 
                       self.load_category_images("body", 2),
                       self.load_category_images("tail", 3)]
        for color in Player.HAIR_COLORS:
            self.images[0].append(self.load_category_images("hair/" + color, 1))
    
    def load_category_images(self, folder, category):
        images = []
        for option in CATEGORIES[category]:
            image = Images.load_imageurl("img/player/" + folder + "/" + option + "/idle.png")
            image = Images.scale(image, 3)
            images.append(image)
        return images
    
    def change_option(self, category, amount):
        self.options[category] = (self.options[category] + amount) % len(CATEGORIES[category])
        
    def randomize(self):
        for i in range(len(CATEGORIES)):
            self.options[i] = random.randrange(len(CATEGORIES[i]))
    
    def render(self, screen):
        Menu.render(self, screen)
        
        hair_image = self.images[0][self.options[0]][self.options[1]]
        body_image = self.images[1][self.options[2]]
        tail_image = self.images[2][self.options[3]]
        player_pos = (Game.SCREEN_WIDTH / 2 - body_image.get_width() / 2, Game.SCREEN_HEIGHT * 8 // 22)
        screen.blit(tail_image, player_pos)
        screen.blit(body_image, player_pos)
        screen.blit(hair_image, player_pos)