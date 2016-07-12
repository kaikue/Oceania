#GLOBAL CONSTANTS

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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

BREAK_LENGTH = 4


#IMPORTS
#Do these after the constants are set, so that the imported classes can reference them.

import pygame
from pygame.locals import DOUBLEBUF
import os
import sys
import Convert
import Menu
import World
import Player
import gui.GUI as GUI
from gui.InventoryGUI import InventoryGUI
from gui.HotbarGUI import HotbarGUI


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
    font = pygame.font.Font("fnt/coders_crux.ttf", 16 * SCALE)
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
    pressed = pygame.key.get_pressed()
    shift = pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gamemode == MENU:
                menu.mouse_press()
            if gamemode == PLAYING:
                if event.button == 1:
                    #left click
                    global gui
                    if gui is not None:
                        gui.click(pygame.mouse.get_pos(), False, shift)
                elif event.button == 2:
                    #scroll wheel click
                    pass
                elif event.button == 3:
                    #right click
                    global gui
                    if gui is not None:
                        gui.click(pygame.mouse.get_pos(), True, shift)
                    else:
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
                if event.key == pygame.K_e:
                    if gui is None:
                        gui = InventoryGUI(player, "img/gui/inventory.png")
                    else:
                        gui.close(world)
                        gui = None
                if event.key == pygame.K_F3:
                    global DEBUG
                    DEBUG = not DEBUG
                if event.key == pygame.K_1:
                    player.selected_slot = 0
                if event.key == pygame.K_2:
                    player.selected_slot = 1
                if event.key == pygame.K_3:
                    player.selected_slot = 2
                if event.key == pygame.K_4:
                    player.selected_slot = 3
                if event.key == pygame.K_5:
                    player.selected_slot = 4
                if event.key == pygame.K_6:
                    player.selected_slot = 5
                if event.key == pygame.K_7:
                    player.selected_slot = 6
                if event.key == pygame.K_8:
                    player.selected_slot = 7
                if event.key == pygame.K_9:
                    player.selected_slot = 8
                if event.key == pygame.K_0:
                    player.selected_slot = 9
                if event.key == pygame.K_ESCAPE:
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
            chunk = world.loaded_chunks.get(Convert.world_to_chunk(player.pos[0])[1])
            debugtext = ["fps: {0:.2f}".format(clock.get_fps()),
                        "pos: [{0:.2f}".format(player.pos[0]) + ", {0:.2f}]".format(player.pos[1]),
                        "chunk: " + str(chunk.x),
                        "biome: " + str(chunk.biome["name"])]
            debugimg = GUI.render_string_array(debugtext, font, 0, WHITE)
            h = SCREEN_HEIGHT - debugimg.get_height()
            screen.blit(debugimg, (2 * SCALE, h))
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