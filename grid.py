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

    def __init__(self, x, y) -> None:
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

    def __init__(self, w, h) -> None:
        self.size = (w, h)
        self.grid = []
        for i in range(self.size[0]):
            self.grid.append([])
            for j in range(self.size[1]):
                self.grid[i].append(MapTile(i, j))
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