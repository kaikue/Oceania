#GLOBAL CONSTANTS

VERSION = "0.1.2"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLOCK_SIZE = 16
SCALE = 2

MAINMENU = 0
PLAYING = 1
RESET = 2
OPENGUI = 3
PAUSEMENU = 4

LEFT = False
RIGHT = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (224, 224, 224)
MEDIUM_GRAY = (160, 160, 160)
TRANSPARENT = (0, 0, 0, 0)
SKY = (128, 128, 255)
BLUE = (62, 121, 221)
RED = (255, 0, 0)

DEBUG = True #displays fps, coords, etc.

BREAK_LENGTH = 4


#IMPORTS
#Do these after the constants are set, so that the imported classes can reference them.

import pygame
from pygame.locals import DOUBLEBUF
import os
import sys
import Convert
from mnu.MainMenu import MainMenu
from mnu.PauseMenu import PauseMenu
from mnu.OptionsMenu import OptionsMenu
import World
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
    global music
    music = False
    pygame.mixer.init()
    global font
    font = pygame.font.Font("fnt/coders_crux.ttf", 16 * SCALE)
    global big_font
    big_font = pygame.font.Font("fnt/coders_crux.ttf", 24 * SCALE)
    show_main_menu()
    global gui
    gui = None
    run()

def run():
    while True:
        clock.tick_busy_loop(60)
        update()
        render()

def start_setup():
    global gamemode
    gamemode = PLAYING
    World.load_data()
    global viewport
    viewport = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

def generate_world(world_name, seed, player_options):
    global world
    world = World.World(world_name)
    world.generate(seed, player_options)

def load_world(world_name):
    global world
    world = World.World(world_name)
    world.load()

def finish_setup():
    global world
    global hotbarGui
    hotbarGui = HotbarGUI(world.player, "img/gui/hotbar.png")

def is_shift_pressed():
    pressed = pygame.key.get_pressed()
    return pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]

def update():
    shift = is_shift_pressed()
    global gamemode
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gamemode == MAINMENU or gamemode == PAUSEMENU:
                if event.button == 1:
                    menu.mouse_press()
            elif gamemode == PLAYING:
                player = world.player
                if event.button == 1:
                    #left click
                    player.left_click_discrete(world, pygame.mouse.get_pos(), viewport, shift)
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
            elif gamemode == OPENGUI:
                global gui
                gui.click(pygame.mouse.get_pos(), event.button, shift)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if gamemode == MAINMENU or gamemode == PAUSEMENU:
                menu.mouse_release()
        elif event.type == pygame.KEYDOWN:
            #typed a key
            if gamemode == PLAYING:
                player = world.player
                if event.key == pygame.K_e:
                    gui = InventoryGUI(player, "img/gui/inventory.png")
                    gamemode = OPENGUI
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
                    pause()
            elif gamemode == OPENGUI:
                if event.key == pygame.K_e or event.key == pygame.K_ESCAPE:
                    gui.close(world)
                    gui = None
                    gamemode = PLAYING
            elif gamemode == PAUSEMENU:
                if event.key == pygame.K_ESCAPE:
                    unpause()
            elif gamemode == MAINMENU:
                if event.key == pygame.K_BACKSPACE:
                    menu.delete()
                elif event.key == pygame.K_SPACE:
                    menu.type(" ")
                elif is_legal_key(pygame.key.name(event.key)):
                    menu.type(pygame.key.name(event.key))
    
    if gamemode == MAINMENU or gamemode == PAUSEMENU:
        menu.update()
    
    elif gamemode == PLAYING:
        player = world.player
        player.move_dir = [0, 0]
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            player.move_dir[0] -= 1
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            player.move_dir[0] += 1
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            player.move_dir[1] -= 1
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            player.move_dir[1] += 1
        
        mousebuttons = pygame.mouse.get_pressed()
        if mousebuttons[0]:
            player.break_block(world, pygame.mouse.get_pos(), viewport, shift)
        if mousebuttons[2]:
            player.right_click_continuous(world, pygame.mouse.get_pos(), viewport, shift)
        player.update(world)
        viewport.x = Convert.world_to_pixels(player.pos)[0] - SCREEN_WIDTH / 2
        viewport.y = Convert.world_to_pixels(player.pos)[1] - SCREEN_HEIGHT / 2
        world.update()
    
    elif gamemode == OPENGUI:
        gui.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed(), shift)

def render():
    if gamemode == MAINMENU or gamemode == PAUSEMENU:
        menu.render_background(screen)
        menu.render(screen)
        
    elif gamemode in (PLAYING, OPENGUI):
        player = world.player
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
        
        #add blue overlay- not completely sure this is good
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(64)
        overlay.fill(BLUE)
        screen.blit(overlay, (0, 0))
        
        if gamemode == PLAYING:
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

def pause():
    global gamemode
    gamemode = PAUSEMENU
    global menu
    menu = PauseMenu()

def unpause():
    global gamemode
    gamemode = PLAYING

def show_options():
    global menu
    menu = OptionsMenu(menu)

def set_menu(new_menu):
    global menu
    menu = new_menu

def show_main_menu():
    global gamemode
    gamemode = MAINMENU
    global menu
    menu = MainMenu()

def is_music_enabled():
    global music
    return music

def toggle_music():
    global music
    music = not music
    if music:
        play_music()
    else:
        stop_music()
    return music

def play_music():
    #not putting the music on github yet
    pygame.mixer.music.load("mus/Seashore Peace - Ambiance.wav")
    pygame.mixer.music.play(-1, 0.0)

def stop_music():
    pygame.mixer.music.stop()

def close():
    if gamemode in (PLAYING, OPENGUI, PAUSEMENU):
        #pickle loaded chunks and other game state data
        world.close()
    sys.exit(0)

def get_font(big = False):
    if big:
        return big_font
    else:
        return font

def get_worlds():
    parent_dir = "dat"
    #From http://stackoverflow.com/a/800201
    worlds = [name for name in os.listdir(parent_dir)
              if os.path.isdir(os.path.join(parent_dir, name))]
    #From http://stackoverflow.com/a/168424 - sort by last modified (use state file time)
    worlds.sort(key=lambda x: os.path.getmtime(parent_dir + "/" + x + "/state"))
    worlds.reverse()
    return worlds

def get_world():
    return world

def set_gui(g):
    global gui
    gui = g
    global gamemode
    if gui is None:
        gamemode = PLAYING
    else:
        gamemode = OPENGUI

def play_sound(sound):
    soundObj = pygame.mixer.Sound(sound)
    soundObj.play()

def cutoff(n, cutoff):
    if -cutoff <= n <= cutoff:
        return 0
    else:
        return n

def is_legal_key(key):
    return len(key) == 1 and str.isalnum(key)