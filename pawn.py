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

    def get_pixel_pos(self):
        "Returns the pixel position of the tile the Pawn is on."
        return self.tile.grid.get_tile_pos(self.tile)

class Capability:
    """
    A Capability is an attribute of an Actor.
    A Capability has an intensity and duration value.
    If 'is_active' is True, the capability may be used actively.
    if 'is_timed' is True, the capability lasts a limited amount of turns. A duration of 0 indicates infinite duration.
    """
    is_active = False
    is_timed = False

    def __init__(self, intensity=0, duration=0):
        self.intensity = intensity
        self.duration = duration

    def activate(self, actor: Actor):
        "Called when an actor activates a capability."
        pass

    def on_timeout(self, actor: Actor):
        "Called when the capability's duration is over."
        pass

    def on_turn_start(self, actor: Actor):
        "Called when an actor starts their action."
        pass

    def on_turn_end(self, actor: Actor):
        "Called when an actor ends their action."
        pass

    def advance_turn(self, actor: Actor):
        "Handles capability duration."
        if self.is_timed and self.duration > 0:
            self.duration -= 1
            if self.duration <= 0:
                self.on_timeout(actor)
                actor.capabilities.remove(self)


class CAP_HealthRegen(Capability):
    """
    This capability restores some health to the actor at the end of a turn.
    """

    def on_turn_end(self, actor: Actor):
        actor.health = min(actor.health_max, actor.health + self.intensity)

class Actor(Pawn):
    """
    An Actor is a pawn that has a set of capabilities.
    An Actor has a health value, and an alive boolean value, although not all actors can be hurt.
    """
    self.capabilities = []
    self.health_max = 1000

    def __init__(self, tile: MapTile) -> None:
        self.health = self.health_max
        self.alive = True
    
    def is_alive(self) -> bool:
        return self.alive