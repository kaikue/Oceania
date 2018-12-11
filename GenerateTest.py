import sys
import random
import pygame
import perlin
import Generate
import World

def gen(width, height, screen):
    xs = list(range(width))
    random.shuffle(xs)
    for x in xs:
        for y in range(height):
            value = Generate.terrain((x, y), (50, 150))[0]
            w = 128 + 127 * value
            color = (w, w, w)
            if value > -0.5:
                color = (255, w, w)
            else:
                color = (w, w, 255)
            #screen.set_at((x, y), color)
            pygame.draw.rect(screen, color, (x*2, y*2, 2, 2))
            pygame.display.update()
    print("Generation complete")

if __name__ == "__main__":
    width = 100
    height = World.HEIGHT
    
    pygame.init()
    screen = pygame.display.set_mode((width*2, height*2))
    
    Generate.setup(100)
    gen(width, height, screen)
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                elif event.key == pygame.K_SPACE:
                    Generate.noise2d = perlin.PerlinNoiseFactory(2, octaves=3)
                    gen(width, height, screen)