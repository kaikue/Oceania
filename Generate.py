import perlin
import World

TERRAIN_SCALE = 30
CAVE_SCALE = 40 #controls overall scale & thickness of caves
CAVE_CUTOFF = 0.05 #controls thickness of caves
CAVE_EXPANSION = 0.7 #controls how much thicker caves are at the bottom of the world
noise2d = perlin.PerlinNoiseFactory(2, octaves=3)

def terrain(pos, limits):
    #TODO: only subtract caves if foreground
    (x, y) = pos
    
    #regular 2d Perlin noise
    noise = noise2d(x / TERRAIN_SCALE, y / TERRAIN_SCALE)
    
    #apply gradient to make lower areas denser
    noise_g = gradient_filter(noise, y, limits)
    
    #cut out caves
    cave = noise2d(x / CAVE_SCALE, y / CAVE_SCALE)
    #caves get bigger as you get further down
    cave_g = gradient(y, (limits[0], World.HEIGHT))
    cave_adjust = 1 - cave_g * CAVE_EXPANSION
    cave = cave * cave_adjust
    if -CAVE_CUTOFF < cave < CAVE_CUTOFF:
        return -1
    
    return noise_g

def gradient(y, limits):
    g = (y - limits[0]) / (limits[1] - limits[0])
    g = min(max(g, 0), 1)
    return g

def gradient_filter(n, y, limits):
    #n: value to filter, from -1 to 1
    #y: amount along gradient
    #limits: top and bottom of gradient
    #returns new value of n from -1 to 1
    g = gradient(y, limits)
    return (n + 1) * g - 1