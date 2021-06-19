#! /usr/bin/env python3

from enum import Enum

import pygame


# Probably not useful, and may lead to circular reference
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

    def __init__(self, x, y):
        self.position = (x, y)
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    def each_neighbor(self):
        for tile in [self.north, self.south, self.east, self.west]:
            yield tile


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
                    cell.west = self.grid[i - 1][j]
                if i + 1 < self.size[0]:
                    cell.east = self.grid[i + 1][j]
                if j - 1 >= 0:
                    cell.north = self.grid[i][j - 1]
                if j + 1 < self.size[1]:
                    cell.south = self.grid[i][j + 1]

    def tile_at(self, pos):
        return self.grid[pos[0]][pos[1]]

    # change tile's center position to pixel position
    def tile_to_pos(self, tile, window_size_x=1280, window_size_y=720):
        pos_x = window_size_x / self.size[0] * (tile.position[0] + 1 / 2)
        pos_y = window_size_y / self.size[1] * (tile.position[1] + 1 / 2)
        return pos_x, pos_y

    # change pixel position to tile position
    def pos_to_tile(self, pos, window_size_x=1280, window_size_y=720):
        tile_pos_x = int(pos[0] / (window_size_x / self.size[0]))
        tile_pos_y = int(pos[1] / (window_size_y / self.size[1]))
        return self.tile_at((tile_pos_x, tile_pos_y))
