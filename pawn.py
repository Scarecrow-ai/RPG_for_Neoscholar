#! /usr/lib/python3

from grid import *

class Pawn:
    """
    A pawn is an actor that can move on a MapGrid.
    """

    def __init__(self, tile: MapTile) -> None:
        self.tile = tile

    def get_tile(self) -> MapTile:
        return self.tile

    def move(self, dir: Dir):
        # TODO sanity check
        self.tile = self.tile.neighbors[dir]

class Actor(Pawn):
    """
    An actor is a pawn that has a set of capabilities.
    """

    def __init__(self, tile: MapTile) -> None:
        pass