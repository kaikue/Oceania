#IMPORTS

import pygame
import os
import sys
import world
import player


#GLOBAL CONSTANTS

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

MENU = 0
PLAYING = 1
RESET = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY = (128, 128, 255)

VIEW_WIDTH = 40
VIEW_HEIGHT = 30

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
    #gameworld.generate()
    global view_x
    view_x = 0
    global view_y
    view_y = 170
    global player_char
    player_char = player.Player(0, 180, "img/player.png", 6)
    run()

def run():
    while True:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            
            #elif event.type == pygame.KEYDOWN:
                #if pygame.key.get_pressed()[pygame.K_SPACE]:
                    #gameworld.reset()
        clock.tick(60)
        update()
        render()
        #pygame.time.wait(1)

def update():
    pressed = pygame.key.get_pressed()
    player_char.dir = [0, 0]
    if pressed[pygame.K_LEFT]:
        #viewx -= 1
        player_char.dir[0] -= 1
    if pressed[pygame.K_RIGHT]:
        #viewx += 1
        player_char.dir[0] += 1
    if pressed[pygame.K_UP]:
        #viewy -= 1
        player_char.dir[1] -= 1
    if pressed[pygame.K_DOWN]:
        #viewy += 1
        player_char.dir[1] += 1
    player_char.update()
    #viewx = max(viewx, 0)
    #if viewx + VIEW_WIDTH > world.WIDTH:
    #    viewx = world.WIDTH - VIEW_WIDTH
    #global viewx
    #global viewy
    #viewy = max(viewy, 0)
    #if viewy + VIEW_HEIGHT > world.HEIGHT:
    #    viewy = world.HEIGHT - VIEW_HEIGHT
    gameworld.update()

def render():
    screen.fill(SKY)
    #draw clouds
    gameworld.render(screen, pygame.Rect(view_x, view_y, VIEW_WIDTH, VIEW_HEIGHT))
    if DEBUG:
        fps = font.render("fps: " + str(clock.get_fps()), 0, BLACK)
        screen.blit(fps, (10, 10))
    player_char.render(screen, player_char.x - view_x, player_char.y - view_y)
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
        man i sound so legitimate
    Chunks at side of world (player movement)
    Caves
    Spawn midpoint displacement
Player
    Camera movement
Crafting
Menus
Combat
Block placement & destruction
"""