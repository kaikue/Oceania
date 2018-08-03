import perlin

TERRAIN_SCALE = 30
CAVE_SCALE = 40 #controls overall scale & thickness of caves
CAVE_CUTOFF = 0.07 #controls thickness of caves
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
    #TODO: caves get bigger as you get further down
    #need to make more subtle filter maybe?
    #cave_g = gradient_filter(cave, y, (-World.HEIGHT, World.HEIGHT))
    if -CAVE_CUTOFF < cave < CAVE_CUTOFF:
        return -1
    
    return noise_g

def gradient_filter(n, y, limits):
    #n: value to filter, from -1 to 1
    #y: amount along gradient
    #limits: top and bottom of gradient
    #returns new value of n from -1 to 1
    g = (y - limits[0]) / (limits[1] - limits[0])
    g = min(max(g, 0), 1)
    return (n + 1) * g - 1