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
    return pygame.transform.scale(img, (Game.SCALE * img.get_width(), Game.SCALE * img.get_height()))

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