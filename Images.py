import pygame
import Game

break_images = []
tooltip_pieces = []
tooltip_centers = []
highlight_image = None

def load_imageurl(imageurl):
    if imageurl == "":
        return None
    img = pygame.image.load(imageurl).convert_alpha()
    return scale(img, Game.SCALE)

def load_images():
    base = "img/gui/pieces/"
    global tooltip_pieces
    tooltip_pieces = [[load_imageurl(base + "top-left.png"), load_imageurl(base + "top.png"), load_imageurl(base + "top-right.png")],
                      [load_imageurl(base + "left.png"), None, load_imageurl(base + "right.png")],
                      [load_imageurl(base + "bottom-left.png"), load_imageurl(base + "bottom.png"), load_imageurl(base + "bottom-right.png")]]
    global tooltip_centers
    tooltip_centers = [load_imageurl(base + "center0.png"), 
                       load_imageurl(base + "center1.png"), 
                       load_imageurl(base + "center2.png"), 
                       load_imageurl(base + "center3.png")]
    for i in range(Game.BREAK_LENGTH):
        img = pygame.image.load("img/break_" + str(i) + ".png").convert_alpha()
        global break_images
        break_images.append(pygame.transform.scale(img, (img.get_width() * Game.SCALE, img.get_height() * Game.SCALE)))
    global highlight_image
    highlight_image = load_imageurl("img/gui/highlight.png")

def flip_horizontal(img):
    return pygame.transform.flip(img, True, False)

def flip_vertical(img):
    return pygame.transform.flip(img, False, True)

def flip_completely(img):
    return pygame.transform.flip(img, True, True)

def rotate(img, angle):
    return pygame.transform.rotate(img, angle)

def scale(img, scale):
    return pygame.transform.scale(img, (int(scale * img.get_width()), int(scale * img.get_height())))

def make_itemdrop_image(blockimg):
    #takes unscaled block image
    img = pygame.Surface((Game.BLOCK_SIZE, Game.BLOCK_SIZE), pygame.SRCALPHA, 32).convert_alpha()
    img.blit(blockimg, (0, 0))
    img = pygame.transform.scale(img, (Game.BLOCK_SIZE // Game.SCALE, Game.BLOCK_SIZE // Game.SCALE))
    return pygame.transform.scale(img, (Game.BLOCK_SIZE, Game.BLOCK_SIZE))

def crop(blockimg):
    #takes scaled block image
    img = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA, 32).convert_alpha()
    img.blit(blockimg, (0, 0))
    return img
