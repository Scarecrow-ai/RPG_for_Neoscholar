#! /usr/lib/python3

from capability import Capability
from grid import *
from enum import *
from damage import *

class Pawn:
    """
    A pawn is an entity that can move on a MapGrid.
    """
    layer = 0 # used in sprite drawing

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
    An Actor is a pawn that has a set of capabilities, and has some health and can be hurt.
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

    def trigger_capabilities(self, trigger: str, data):
        for c in self.capabilities:
            c.check_trigger(trigger, data)
    
    def use_capability(self, capability: Capability, data):
        capability.activate(data)

    def take_damage(self, dmginfo: DamageInfo):
        "Actor takes damage from damage info. If the damage reduces the actor's health to 0 or lower, the actor is no longer alive."
        if self.alive == False:
            return

        self.trigger_capabilities("OnTakeDamage", dmginfo)

        self.health = self.health - dmginfo.damage
        if self.health <= 0:
            self.alive = False