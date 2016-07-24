import pygame
import Game
import World

break_images = []
tooltip_pieces = []
tooltip_centers = []
highlight_image = None
block_images = {}
block_images_background = {}
block_drop_images = {}
item_images = {}

def load_imageurl(imageurl):
    if imageurl == "":
        return None
    img = pygame.image.load(imageurl).convert_alpha()
    return pygame.transform.scale(img, (Game.SCALE * img.get_width(), Game.SCALE * img.get_height()))

def load_images(blocks, items):
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
    
    water_image = pygame.image.load("img/water.png")
    st_water_image = water_image.copy()
    st_water_image.set_alpha(128)
    pygame.display.set_icon(water_image) #TODO: change the icon to something better
    
    #load block images- foreground, background, drops
    global block_images
    global block_images_background
    global block_drop_images
    for block in blocks:
        path = block["image"]
        if path == "":
            continue
        #foreground image
        blockimg = pygame.image.load(path).convert_alpha()
        surf = pygame.transform.scale(blockimg, (blockimg.get_width() * Game.SCALE, blockimg.get_height() * Game.SCALE))
        block_images[block["id"]] = surf
        #background image
        #blit the image onto the water tile so it isn't just empty transparency
        image = blockimg.copy()
        for x in range(image.get_width() // Game.BLOCK_SIZE):
            for y in range(image.get_height() // Game.BLOCK_SIZE):
                image.blit(water_image, (x * Game.BLOCK_SIZE, y * Game.BLOCK_SIZE))
        image.blit(blockimg, (0, 0))
        for x in range(image.get_width() // Game.BLOCK_SIZE):
            for y in range(image.get_height() // Game.BLOCK_SIZE):
                image.blit(st_water_image, (x * Game.BLOCK_SIZE, y * Game.BLOCK_SIZE))
        surf = pygame.transform.scale(image, (image.get_width() * Game.SCALE, image.get_height() * Game.SCALE))
        block_images_background[block["id"]] = surf
        #drop image
        image = pygame.Surface((Game.BLOCK_SIZE, Game.BLOCK_SIZE), pygame.SRCALPHA, 32).convert_alpha()
        image.blit(blockimg, (0, 0))
        image = pygame.transform.scale(image, (Game.BLOCK_SIZE // Game.SCALE, Game.BLOCK_SIZE // Game.SCALE))
        block_drop_images[block["id"]] = pygame.transform.scale(image, (Game.BLOCK_SIZE, Game.BLOCK_SIZE))
    block_images[World.get_block_id("water")] = pygame.Surface((Game.BLOCK_SIZE, Game.BLOCK_SIZE), pygame.SRCALPHA, 32)
    #load item images
    global item_images
    for item_name in items.keys():
        item = items[item_name]
        path = item["image"]
        if path == "":
            continue
        imoge = pygame.Surface((Game.BLOCK_SIZE * Game.SCALE, Game.BLOCK_SIZE * Game.SCALE), pygame.SRCALPHA, 32).convert_alpha()
        imoge.blit(load_imageurl(path), (0, 0))
        item_images[item_name] = imoge