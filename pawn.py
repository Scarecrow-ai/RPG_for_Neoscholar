#! /usr/lib/python3

from enum import *
import grid, damage as dmg

class Pawn:
    """
    A pawn is an entity that can move on a MapGrid.
    """
    layer = 0 # used in sprite drawing

    def __init__(self, name: str, tile: grid.MapTile) -> None:
        self.name = name
        self.tile = tile
        self.tile.holding = self

    def get_tile(self) -> grid.MapTile:
        return self.tile

    def move(self, dir: grid.Dir) -> bool:
        "Moves the pawn a certain direction. Returns true if movement successful."
        target_tile = self.tile.neighbors[dir]

        if target_tile == None or target_tile.holding != None:
            return False

        self.tile.holding = None
        target_tile.holding = self
        self.tile = target_tile
        return True

    def get_pixel_pos(self): # -> tuple(int, int):
        "Returns the pixel position of the tile the Pawn is on."
        return self.tile.grid.get_tile_pos(self.tile)

class Actor(Pawn):
    """
    An Actor is a pawn that has a set of capabilities, and has some health and can be hurt.
    """
    capabilities = []
    health_max = 1000

    def __init__(self, name: str, tile: grid.MapTile) -> None:
        super().__init__(name, tile)
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
    
    def use_capability(self, capability: "Capability", data):
        capability.activate(data)

    def take_damage(self, dmginfo: dmg.DamageInfo):
        "Actor takes damage from damage info. If the damage reduces the actor's health to 0 or lower, the actor is no longer alive."
        if self.alive == False:
            return

        # self.trigger_capabilities("OnTakeDamage", dmginfo)

        self.health = self.health - dmginfo.damage
        name = dmginfo.attacker != None and dmginfo.attacker.name or "something"
        print(f"{self.name} took {dmginfo.damage} damage from {name} ({self.health}hp)")

        if self.health <= 0:
            self.alive = False
            print(f"{self.name} died!")