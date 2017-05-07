import random
import Game
import Images
from mnu.Menu import Menu, Label
import Button
import Player

CATEGORIES = (Player.HAIR_COLORS, Player.HAIR_LENGTHS, Player.BODY_COLORS, Player.TAIL_COLORS)

class CharacterMenu(Menu):
    
    def __init__(self, prev_menu):
        
        #TODO: make option buttons smaller
        
        self.options = [0, 0, 0, 0]
        
        random_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 2 // 10), "Randomize", "random")
        random_button.menu = self
        
        l_hair_color_button = self.make_category_button(False, Game.SCREEN_HEIGHT * 3 // 10, 0)
        r_hair_color_button = self.make_category_button(True, Game.SCREEN_HEIGHT * 3 // 10, 0)
        l_hair_style_button = self.make_category_button(False, Game.SCREEN_HEIGHT * 4 // 10, 1)
        r_hair_style_button = self.make_category_button(True, Game.SCREEN_HEIGHT * 4 // 10, 1)
        l_body_button = self.make_category_button(False, Game.SCREEN_HEIGHT * 5 // 10, 2)
        r_body_button = self.make_category_button(True, Game.SCREEN_HEIGHT * 5 // 10, 2)
        l_tail_button = self.make_category_button(False, Game.SCREEN_HEIGHT * 6 // 10, 3)
        r_tail_button = self.make_category_button(True, Game.SCREEN_HEIGHT * 6 // 10, 3)
        
        back_button = Button.Button((Game.SCREEN_WIDTH / 4 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Back", "menu")
        back_button.next_menu = prev_menu
        
        create_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Create", "create")
        create_button.character_menu = self
        create_button.world_menu = prev_menu
        
        title_label = Label("Customize Character", (Game.SCREEN_WIDTH / 2 - Label.WIDTH / 2, Game.SCREEN_HEIGHT // 15))
        #TODO: options labels
        
        self.load_images()
        
        super(CharacterMenu, self).__init__([random_button, 
                                             l_hair_color_button, r_hair_color_button,
                                             l_hair_style_button, r_hair_style_button,
                                             l_body_button, r_body_button,
                                             l_tail_button, r_tail_button,
                                             back_button, create_button],
                                            [title_label])
    
    def make_category_button(self, right, y, category):
        x = Game.SCREEN_WIDTH * 3 // 4 - Button.WIDTH / 2 if right else Game.SCREEN_WIDTH // 4 - Button.WIDTH / 2
        text = ">" if right else "<"
        button = Button.Button((x, y), text, "change_option")
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
        player_pos = (Game.SCREEN_WIDTH / 2 - body_image.get_width() / 2, Game.SCREEN_HEIGHT // 3)
        screen.blit(tail_image, player_pos)
        screen.blit(body_image, player_pos)
        screen.blit(hair_image, player_pos)