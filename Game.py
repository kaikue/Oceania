#IMPORTS

import pygame
from pygame.locals import DOUBLEBUF
import os
import sys
import Convert
import Menu
import World
import Player
import InventoryGUI
from HotbarGUI import HotbarGUI


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
MUSIC = False #play background music


#GAME FUNCTIONS
#For handling input, overall game functions.
#Savable data should be stored in World.

def start():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.display.set_caption("Oceania")
    flags = DOUBLEBUF # | FULLSCREEN
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    global clock
    clock = pygame.time.Clock()
    
    #not putting the music on github yet
    if MUSIC:
        pygame.mixer.init()
        pygame.mixer.music.load("mus/Seashore Peace - Ambiance.wav")
        pygame.mixer.music.play(-1, 0.0)
        #soundObj = pygame.mixer.Sound("mus/Seashore Peace - Ambiance.wav")
        #soundObj.play()
    
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
    global hotbarGui
    hotbarGui = HotbarGUI(player, "img/gui/hotbar.png")

def update():
    shift = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gamemode == MENU:
                menu.mouse_press()
            if gamemode == PLAYING:
                if event.button == 1:
                    #left click
                    pass
                elif event.button == 2:
                    #scroll wheel click
                    pass
                elif event.button == 3:
                    #right click
                    player.right_click_discrete(world, pygame.mouse.get_pos(), viewport, shift)
                elif event.button == 4:
                    #scroll wheel up
                    player.change_slot(False)
                elif event.button == 5:
                    #scroll wheel down
                    player.change_slot(True)
        elif event.type == pygame.MOUSEBUTTONUP:
            if gamemode == MENU:
                menu.mouse_release()
        elif event.type == pygame.KEYDOWN:
            #typed a key
            if gamemode == PLAYING:
                if pygame.key.get_pressed()[pygame.K_e]:
                    global gui
                    if gui is None:
                        gui = InventoryGUI.InventoryGUI(player, "img/gui/inventory.png")
                    else:
                        gui = None
                if pygame.key.get_pressed()[pygame.K_F3]:
                    global DEBUG
                    DEBUG = not DEBUG
                if pygame.key.get_pressed()[pygame.K_1]:
                    player.selected_slot = 0
                if pygame.key.get_pressed()[pygame.K_2]:
                    player.selected_slot = 1
                if pygame.key.get_pressed()[pygame.K_3]:
                    player.selected_slot = 2
                if pygame.key.get_pressed()[pygame.K_4]:
                    player.selected_slot = 3
                if pygame.key.get_pressed()[pygame.K_5]:
                    player.selected_slot = 4
                if pygame.key.get_pressed()[pygame.K_6]:
                    player.selected_slot = 5
                if pygame.key.get_pressed()[pygame.K_7]:
                    player.selected_slot = 6
                if pygame.key.get_pressed()[pygame.K_8]:
                    player.selected_slot = 7
                if pygame.key.get_pressed()[pygame.K_9]:
                    player.selected_slot = 8
                if pygame.key.get_pressed()[pygame.K_0]:
                    player.selected_slot = 9
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
        mousebuttons = pygame.mouse.get_pressed()
        if mousebuttons[0]:
            player.break_block(world, pygame.mouse.get_pos(), viewport, shift)
        if mousebuttons[2]:
            player.right_click_continuous(world, pygame.mouse.get_pos(), viewport, shift)
        player.update(world)
        viewport.x = Convert.world_to_pixels(player.pos)[0] - SCREEN_WIDTH / 2
        viewport.y = Convert.world_to_pixels(player.pos)[1] - SCREEN_HEIGHT / 2
        world.update()

def render():
    if gamemode == MENU:
        menu.render(screen)
        
    elif gamemode == PLAYING:
        shift = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]
        screen.fill(SKY)
        
        #background
        world.render(screen, viewport, True)
        if shift:
            player.draw_block_highlight(world, pygame.mouse.get_pos(), viewport, screen, shift)
        world.render_breaks(screen, viewport, True)
        
        #foreground
        world.render(screen, viewport, False)
        if not shift:
            player.draw_block_highlight(world, pygame.mouse.get_pos(), viewport, screen, shift)
        world.render_breaks(screen, viewport, False)
        player.render(screen, Convert.world_to_viewport(player.pos, viewport))
        
        if gui is None:
            hotbarGui.render(screen)
        else:
            gui.render(screen)
        
        if DEBUG:
            #render debug text
            h = 360
            fpsimg = font.render("fps: {0:.2f}".format(clock.get_fps()), 0, WHITE)
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
    pygame.display.flip()

def close():
    if gamemode == MENU:
        pass
    elif gamemode == PLAYING:
        #pickle loaded chunks and other game state data
        world.close()
    sys.exit(0)

def get_font():
    return font

def get_world():
    return world

def play_sound(sound):
    soundObj = pygame.mixer.Sound(sound)
    soundObj.play()

def main():
    start()

if __name__ == "__main__":
    main()