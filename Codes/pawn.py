# not used
from grid import *


class Pawn:
    """
    A pawn is an actor that can move on a MapGrid.
    """

    def __init__(self, tile: MapTile) -> None:
        self.tile = tile

    def get_tile(self) -> MapTile:
        return self.tile

    def move(self, dir):
        # TODO sanity check
        self.tile = self.tile.neighbors[dir]
