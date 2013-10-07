import block
import chunk

def chunk_to_world(x, arg_chunk):
    #X pos within the chunk (blocks) to x pos within the world (blocks). Enter 0 to convert chunk's coords to world coords (blocks).
    return x + arg_chunk.x * chunk.WIDTH

def world_to_chunk(x):
    #X pos within the world (blocks) to x pos within some chunk (blocks) and x pos of that chunk (chunks).
    return (x % chunk.WIDTH, x // chunk.WIDTH)

def world_to_pixels(pos):
    #Pos within the world (blocks) to pos within the world (pixels).
    return [pos[0] * block.SIZE, pos[1] * block.SIZE]

def pixels_to_world(pos):
    #Pos within the world (pixels) to pos within the world (blocks).
    return [x_pixels_to_world(pos[0]), y_pixels_to_world(pos[1])]

def x_pixels_to_world(x):
    return x // block.SIZE

def y_pixels_to_world(y):
    return y // block.SIZE

def pixels_to_viewport(pos, viewport):
    return [pos[0] - viewport.x, pos[1] - viewport.y]

def world_to_viewport(pos, viewport):
    return pixels_to_viewport(world_to_pixels(pos), viewport)