#IMPORTS

import pygame
import os
import sys
import Convert
import World
import Block
import Player


#GLOBAL CONSTANTS

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

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
    global viewport
    viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    global player
    player = Player.Player([0, 180], "img/player.png")
    global world
    world = World.World("defaultworld", player)
    Block.load_images()
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
            pass
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
        fps = font.render("fps: " + str(clock.get_fps()), 0, BLACK)
        screen.blit(fps, (10, 10))
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

NEEDED FEATURES
World generation
    Chunks at side of world (player movement)
    Better terrain
    Caves
    Spawn midpoint displacement
    Structures (over multiple chunks)
    Biomes
Entities
    Enemies, friendlies
    Dropped blocks
Player
    Inventory
Crafting
Menus
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