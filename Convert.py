import Block
import Chunk

def chunk_to_world(x, chunk):
    #X pos within the chunk (blocks) to x pos within the world (blocks). Enter 0 to convert chunk's coords to world coords (blocks).
    return x + chunk.x * Chunk.WIDTH

def world_to_chunk(x):
    #X pos within the world (blocks) to x pos within some chunk (blocks) and x pos of that chunk (chunks).
    return (x % Chunk.WIDTH, int(x // Chunk.WIDTH))

def world_to_pixels(pos):
    #Pos within the world (blocks) to pos within the world (pixels).
    return [world_to_pixel(pos[0]), world_to_pixel(pos[1])]

def world_to_pixel(p):
    return p * Block.SIZE

def pixels_to_world(pos):
    #Pos within the world (pixels) to pos within the world (blocks).
    return [pixel_to_world(pos[0]), pixel_to_world(pos[1])]

def pixel_to_world(p):
    return p // Block.SIZE

def pixels_to_viewport(pos, viewport):
    return [pos[0] - viewport.x, pos[1] - viewport.y]

def world_to_viewport(pos, viewport):
    return pixels_to_viewport(world_to_pixels(pos), viewport)

def chunk_to_pixel(pos, chunk):
    return world_to_pixel([chunk_to_world(pos[0], chunk)[0], pos[1]])
