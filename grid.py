#! /usr/lib/python3

from enum import Enum

class Dir(Enum):
    "An enum representing direction on a 2D grid. Its values correspond to the direction's x/y movement."
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    # NORTHEAST = (1, -1) # Probably not useful
    # NORTHWEST = (-1, -1)
    # SOUTHEAST = (1, 1)
    # SOUTHWEST = (-1, 1)


class MapTile:
    """
    A MapTile is the most basic unit of position in the game.
    A MapTile has a position value, as well as its neighbors (if any exist).
    One tile can hold up to one one character.
    """
    holding: "Pawn"
    grid: "MapGrid"
    position: tuple(int, int)
    neighbors: dict(Dir, "MapTile")

    def __init__(self, x, y, grid=None) -> None:
        self.holding = None
        self.grid = grid
        self.position = (x, y)
        self.neighbors = {}
        self.neighbors[Dir.NORTH] = None
        self.neighbors[Dir.EAST] = None
        self.neighbors[Dir.SOUTH] = None
        self.neighbors[Dir.WEST] = None


class MapGrid:
    """
    A MapGrid is a 2D array of MapTiles.
    """
    origin: tuple(int, int)
    size: tuple(int, int)
    siz: int # pixel size of each tile (is this useful?)
    grid: list(list(MapTile))

    def __init__(self, w, h, x=0, y=0, siz=32) -> None:
        self.origin = (x, y)
        self.size = (w, h)
        self.siz = siz
        self.grid = []
        for i in range(self.size[0]):
            self.grid.append([])
            for j in range(self.size[1]):
                self.grid[i].append(MapTile(i, j, self.grid))
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                cell = self.grid[i][j]
                if i - 1 >= 0:
                    cell.neighbors[Dir.NORTH] = self.grid[i - 1][j]
                if i + 1 < self.size[0]:
                    cell.neighbors[Dir.SOUTH] = self.grid[i + 1][j]
                if j - 1 >= 0:
                    cell.neighbors[Dir.WEST] = self.grid[i][j - 1]
                if j + 1 < self.size[1]:
                    cell.neighbors[Dir.EAST] = self.grid[i][j + 1]

    def get_pixel_pos(self, row, col) -> tuple(int, int):
        """Returns the top-left pixel position of the tile of a certain row and column.
        Note that the row and column positions correspond to Y and X on the screen."""
        return (self.origin[1] + col * self.siz, self.origin[0] + row * self.siz)

    def get_tile_pos(self, tile: MapTile) -> tuple(int, int):
        """Returns the top-left pixel position of a certain tile on the grid.
        Note that the row and column positions correspond to Y and X on the screen."""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == tile:
                    return (self.origin[1] + j * self.siz, self.origin[0] + i * self.siz)
        return None
        