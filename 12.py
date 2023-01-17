# This code is in the Public Domain
# -- richard@mechanicalcat.net
import pygame
import random


class Map:
    def __init__(self, map, tiles):
        self.tiles = pygame.image.load(tiles)

        l = [line.strip() for line in open(map).readlines()]
        self.map = [[None]*len(l[0]) for j in range(len(l))]
        for i in range(len(l[0])):
            for j in range(len(l)):
                tile = l[j][i]
                tile = tile_coords[tile]
                if tile is None:
                    continue
                elif isinstance(tile, type([])):
                    tile = random.choice(tile)
                cx, cy = tile
                if random.choice((0,1)):
                    cx += 192
                if random.choice((0,1)):
                    cy += 192
                self.map[j][i] = (cx, cy)

    def draw(self, view, viewpos):
        '''Draw the map to the "view" with the top-left of "view" being at
           "viewpos" in the map.
        '''
        sx, sy = view.get_size()
        bx = viewpos[0]/64
        by = viewpos[1]/64
        for x in range(0, sx+64, 64):
            i = x/64 + bx
            for y in range(0, sy+64, 64):
                j = y/64 + by
                try:
                    tile = self.map[j][i]
                except IndexError:
                    # too close to the edge
                    continue
                if tile is None:
                    continue
                cx, cy = tile
                view.blit(self.tiles, (x, y), (cx, cy, 64, 64))

    def limit(self, view, pos):
        '''Limit the "viewpos" variable such that it defines a valid top-left
           rectangle of "view"'s size over the map.
        '''
        x, y = pos
        # easy
        x = max(x, 0)
        y = max(y, 0)

        # figure number of tiles in a view, hence max x and y viewpos
        sx, sy = view.get_size()
        nx, ny = sx/64, sy/64
        mx = (len(self.map[0]) - nx) * 64
        my = (len(self.map) - ny) * 64
        print y, my

        return (min(x, mx), min(y, my))

def main():
    pygame.init()
    win = pygame.display.set_mode((640, 480))

    map = Map('map.txt', 'tiles.png')
    viewpos = (0,0)
    move = False
    clock = pygame.time.Clock()
    sx, sy = win.get_size()
    while 1:
        event = pygame.event.poll()
        while event.type != NOEVENT:
            if event.type in (QUIT, KEYDOWN):
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN:
                x, y = viewpos
                dx, dy = event.pos
                x += dx - sx/2
                y += dy - sy/2
                viewpos = map.limit(win, (x, y))
                move = True
            event = pygame.event.poll()

        win.fill((0,0,0))
        map.draw(win, viewpos)
        pygame.display.flip()

        clock.tick(30)


if __name__ == '__main__':
    main()
