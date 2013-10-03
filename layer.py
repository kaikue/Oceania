"""import block

class Layer(object):
    
    def __init__(self, depth):
        self.depth = depth
        self.blocks = [[]]
        self.entities = []
    
    def render(self, screen, viewport):
        blocky = viewport.y
        for drawy in range(0, viewport.height * block.SIZE, block.SIZE):
            blockx = viewport.x
            for drawx in range(0, viewport.width * block.SIZE, block.SIZE):
                self.blocks[blocky][blockx].render(screen, drawx / self.depth, drawy / self.depth)
                blockx += 1
            blocky += 1
        for entity in self.entities:
            screen.blit(entity.img, entity.x / self.depth, entity.y / self.depth)"""