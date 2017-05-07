import random
import Game
import Images
from mnu.Menu import Menu
import Button
import Player

CATEGORIES = (Player.HAIR_COLORS, Player.HAIR_LENGTHS, Player.BODY_COLORS, Player.TAIL_COLORS)

class CharacterMenu(Menu):
    
    def __init__(self, prev_menu):
        #TODO: character buttons and rendering
        self.options = [0, 0, 0, 0]
        
        random_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 1 // 5), "Randomize", "random")
        random_button.menu = self
        
        back_button = Button.Button((Game.SCREEN_WIDTH / 4 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Back", "menu")
        back_button.next_menu = prev_menu
        
        create_button = Button.Button((Game.SCREEN_WIDTH / 2 - Button.WIDTH / 2, Game.SCREEN_HEIGHT * 4 // 5), "Create", "create")
        create_button.character_menu = self
        create_button.world_menu = prev_menu
        
        self.load_images()
        
        super(CharacterMenu, self).__init__([random_button, back_button, create_button])
    
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
        
    def randomize(self):
        for i in range(len(CATEGORIES)):
            self.options[i] = random.randrange(len(CATEGORIES[i]))
    
    def render(self, screen):
        Menu.render(self, screen)
        
        hair_image = self.images[0][self.options[0]][self.options[1]]
        body_image = self.images[1][self.options[2]]
        tail_image = self.images[2][self.options[3]]
        player_pos = (Game.SCREEN_WIDTH / 2, Game.SCREEN_HEIGHT // 3)
        screen.blit(tail_image, player_pos)
        screen.blit(body_image, player_pos)
        screen.blit(hair_image, player_pos)