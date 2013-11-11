#IMPORTS

import pygame
import os
import sys
import Convert
import World
import Player


#GLOBAL CONSTANTS

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLOCK_SIZE = 32

MENU = 0
PLAYING = 1
RESET = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY = (128, 128, 255)

DEBUG = True


#GAME FUNCTIONS
#For handling input, overall game functions.
#Savable data should be stored in World.

def start():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_caption("Oceania")
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    global clock
    clock = pygame.time.Clock()
    #pygame.mixer.init()
    #pygame.mixer.music.load("snd/music.wav")
    #pygame.mixer.music.play(-1, 0.0)
    #soundObj = pygame.mixer.Sound("snd/music.wav")
    #soundObj.play()
    global gamemode
    gamemode = PLAYING
    global font
    font = pygame.font.SysFont("monospace", 20)
    World.load_data()
    global viewport
    viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    global player
    player = Player.Player([0, 180], "img/player.png")
    global world
    world = World.World("defaultworld", player)
    #improve this later
    global img_target
    img_target = pygame.image.load("img/target.png").convert_alpha()
    run()

def run():
    while True:
        clock.tick(60)
        update()
        render()

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            world.break_block(player, pygame.mouse.get_pos(), viewport)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        close()
    elif pressed[pygame.K_l]:
        world.load_all()
    player.dir = [0, 0]
    if pressed[pygame.K_LEFT]:
        player.dir[0] -= 1
    if pressed[pygame.K_RIGHT]:
        player.dir[0] += 1
    if pressed[pygame.K_UP]:
        player.dir[1] -= 1
    if pressed[pygame.K_DOWN]:
        player.dir[1] += 1
    player.update(world)
    viewport.x = Convert.world_to_pixels(player.pos)[0] - SCREEN_WIDTH / 2 #replace with center
    viewport.y = Convert.world_to_pixels(player.pos)[1] - SCREEN_HEIGHT / 2
    world.update()

def render():
    screen.fill(SKY)
    #draw clouds
    world.render(screen, viewport)
    if DEBUG:
        h = 10
        fpsimg = font.render("fps: " + str(clock.get_fps()), 0, BLACK)
        screen.blit(fpsimg, (10, h))
        h += fpsimg.get_height()
        posimg = font.render("pos: " + str(player.pos), 0, BLACK)
        screen.blit(posimg, (10, h))
        h += posimg.get_height()
        chunk = world.loaded_chunks.get(Convert.world_to_chunk(player.pos[0])[1])
        chunkimg = font.render("chunk: " + str(chunk.x), 0, BLACK)
        screen.blit(chunkimg, (10, h))
        h += chunkimg.get_height()
        biomeimg = font.render("biome: " + str(chunk.biome["name"]), 0, BLACK)
        screen.blit(biomeimg, (10, h))
        h += biomeimg.get_height()
    player.render(screen, Convert.world_to_viewport(player.pos, viewport))
    screen.blit(img_target, world.find_pos(world.find_angle(player, pygame.mouse.get_pos(), viewport), Convert.pixels_to_viewport(player.pixel_pos(), viewport)))
    pygame.display.flip()

def close():
    #pickle loaded chunks
    world.close()
    sys.exit(0)

def main():
    start()

if __name__ == "__main__":
    main()


"""
BUGS
Pickling is slow- use marshal?
Eclipse doesn't believe in function-defined global variables- make these objects or something?

NEEDED FEATURES
World generation
    Better terrain
    Caves
        Lava tubes
    Spawn midpoint displacement
    Structures (over multiple chunks)
        Temple
        Volcanic pipe- kimberlite, diamond
    Biomes
Entities
    Enemies, friendlies
    Dropped blocks
Player
    Inventory
Crafting
Menus
    Get input from user to name world
Combat
Move player coordinate to center
Sound
Block placement & destruction
    Make block breaking take time
    Drop block item
    Shorten raycast to nearest block
    Center target image
    Make target only show when pointing at block within range???
        could remove target entirely, highlight selected block/space?
"""