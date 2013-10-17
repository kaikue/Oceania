#IMPORTS

import pygame
import os
import sys
import convert
import world
import player
import block


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
    global gameworld
    gameworld = world.World()
    global view_x
    view_x = 0
    global view_y
    view_y = 0
    global player_char
    player_char = player.Player([0, 180], "img/player.png")
    run()

def run():
    while True:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        clock.tick(60)
        update()
        render()
        #pygame.time.wait(1)

def update():
    pressed = pygame.key.get_pressed()
    player_char.dir = [0, 0]
    if pressed[pygame.K_LEFT]:
        player_char.dir[0] -= 1
    if pressed[pygame.K_RIGHT]:
        player_char.dir[0] += 1
    if pressed[pygame.K_UP]:
        player_char.dir[1] -= 1
    if pressed[pygame.K_DOWN]:
        player_char.dir[1] += 1
    player_char.update(gameworld)
    global view_x, view_y
    view_x = convert.world_to_pixels(player_char.pos)[0] - SCREEN_WIDTH / 2 #replace with center
    view_y = convert.world_to_pixels(player_char.pos)[1] - SCREEN_HEIGHT / 2
    gameworld.update()

def render():
    screen.fill(SKY)
    #draw clouds
    viewport = pygame.Rect(view_x, view_y, SCREEN_WIDTH, SCREEN_HEIGHT)
    gameworld.render(screen, viewport)
    if DEBUG:
        fps = font.render("fps: " + str(clock.get_fps()), 0, BLACK)
        screen.blit(fps, (10, 10))
    player_char.render(screen, convert.world_to_viewport(player_char.pos, viewport))
    pygame.display.flip()

def main():
    start()

if __name__ == "__main__":
    main()


"""
BUGS

NEEDED FEATURES
World generation
    Serialization of unloaded chunks
    Chunks at side of world (player movement)
    Better terrain
    Caves
    Spawn midpoint displacement
Entities
    Collision detection
Player
    Inventory
Crafting
Menus
Combat
Block placement & destruction
Rename modules to make variable naming easier
"""