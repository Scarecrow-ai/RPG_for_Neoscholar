#! /usr/lib/python3

from grid import *

class Pawn:
    """
    A pawn is an entity that can move on a MapGrid.
    """

    def __init__(self, tile: MapTile) -> None:
        self.tile = tile

    def get_tile(self) -> MapTile:
        return self.tile

    def move(self, dir: Dir):
        "Moves the pawn a certain direction."
        # TODO sanity check
        self.tile = self.tile.neighbors[dir]

    def get_pixel_pos(self) -> tuple(int, int):
        "Returns the pixel position of the tile the Pawn is on."
        return self.tile.grid.get_tile_pos(self.tile)

class Actor(Pawn):
    """
    An Actor is a pawn that has a set of capabilities.
    An Actor has a health value, and an alive boolean value, although not all actors can be hurt.
    """
    capabilities = []
    health_max = 1000

    def __init__(self, tile: MapTile) -> None:
        self.health = self.health_max
        self.alive = True
    
    def is_alive(self) -> bool:
        return self.alive

    def get_active_capabilities(self):
        "Returns a list of capabilities that can be actively used."
        return [c for c in self.capabilities if c.is_active == True]