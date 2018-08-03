import sys
import pygame
import Generate
import World

if __name__ == "__main__":
    width = 100
    height = World.HEIGHT
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    
    for x in range(width):
        for y in range(height):
            value = Generate.terrain((x, y), (50, 150))
            w = 128 + 127 * value
            color = (w, w, w)
            if value > -0.5:
                color = (255, w, w)
            else:
                color = (w, w, 255)
            screen.set_at((x, y), color)
    print("Generation complete")
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)