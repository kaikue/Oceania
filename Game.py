#IMPORTS

import pygame
import os
import sys
import Convert
import Menu
import World
import Player
import InventoryGUI


#GLOBAL CONSTANTS

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLOCK_SIZE = 16
SCALE = 2

MENU = 0
PLAYING = 1
RESET = 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)
SKY = (128, 128, 255)

DEBUG = True #displays fps, coords, grid, etc. but impacts performance.


#GAME FUNCTIONS
#For handling input, overall game functions.
#Savable data should be stored in World.

def start():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_caption("Oceania")
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #add double buffering flag
    global clock
    clock = pygame.time.Clock()
    
    #not putting the music on github yet, just comment out this bit
    pygame.mixer.init()
    pygame.mixer.music.load("mus/Seashore Peace - Ambiance.wav")
    pygame.mixer.music.play(-1, 0.0)
    soundObj = pygame.mixer.Sound("mus/Seashore Peace - Ambiance.wav")
    soundObj.play()
    
    global gamemode
    gamemode = MENU
    global font
    font = pygame.font.SysFont("monospace", 20)
    global menu
    menu = Menu.Menu()
    global gui
    gui = None
    run()

def run():
    while True:
        clock.tick_busy_loop(60)
        update()
        render()

def play():
    global gamemode
    gamemode = PLAYING
    World.load_data()
    global viewport
    viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    global player
    player = Player.Player([0, 140], "img/player.png")
    global world
    world = World.World("defaultworld", player)
    global img_target
    img_target = pygame.image.load("img/target.png").convert_alpha()

def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gamemode == MENU:
                menu.mouse_press()
            if gamemode == PLAYING:
                world.break_block(player, pygame.mouse.get_pos(), viewport, pygame.key.get_pressed()[pygame.K_LSHIFT])
        elif event.type == pygame.MOUSEBUTTONUP:
            if gamemode == MENU:
                menu.mouse_release()
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_e]:
                global gui
                if gui is None:
                    gui = InventoryGUI.InventoryGUI(player)
                else:
                    gui = None
            if pygame.key.get_pressed()[pygame.K_F3]:
                global DEBUG
                DEBUG = not DEBUG
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        close()
    
    if gamemode == MENU:
        menu.update()
    
    elif gamemode == PLAYING:
        player.dir = [0, 0]
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            player.dir[0] -= 1
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            player.dir[0] += 1
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            player.dir[1] -= 1
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            player.dir[1] += 1
        player.update(world)
        viewport.x = Convert.world_to_pixels(player.pos)[0] - SCREEN_WIDTH / 2 #replace with center
        viewport.y = Convert.world_to_pixels(player.pos)[1] - SCREEN_HEIGHT / 2
        world.update()

def render():
    if gamemode == MENU:
        menu.render(screen)
    elif gamemode == PLAYING:
        screen.fill(SKY)
        world.render(screen, viewport)
        if DEBUG:
            #render debug text
            h = 10
            fpsimg = font.render("fps: " + str(clock.get_fps()), 0, WHITE)
            screen.blit(fpsimg, (10, h))
            h += fpsimg.get_height()
            posimg = font.render("pos: [{0:.2f}".format(player.pos[0]) + ", {0:.2f}]".format(player.pos[1]), 0, WHITE)
            screen.blit(posimg, (10, h))
            h += posimg.get_height()
            chunk = world.loaded_chunks.get(Convert.world_to_chunk(player.pos[0])[1])
            chunkimg = font.render("chunk: " + str(chunk.x), 0, WHITE)
            screen.blit(chunkimg, (10, h))
            h += chunkimg.get_height()
            biomeimg = font.render("biome: " + str(chunk.biome["name"]), 0, WHITE)
            screen.blit(biomeimg, (10, h))
            h += biomeimg.get_height()
        player.render(screen, Convert.world_to_viewport(player.pos, viewport))
        if gui is None:
            target_pos = world.find_pos(world.find_angle(player, pygame.mouse.get_pos(), viewport), 
                                        Convert.pixels_to_viewport(player.pixel_pos(True), viewport), 
                                        pygame.mouse.get_pos(),
                                        player.get_break_distance())
            screen.blit(img_target, [x - y for x, y in zip(target_pos, [dim / 2 for dim in img_target.get_size()])]) #zoo-wee mama!
        else:
            gui.render(screen)
    pygame.display.flip()

def close():
    if gamemode == MENU:
        pass
    elif gamemode == PLAYING:
        #pickle loaded chunks
        world.close()
    sys.exit(0)

def get_font():
    return font

def get_world():
    return world

def main():
    start()

if __name__ == "__main__":
    main()

