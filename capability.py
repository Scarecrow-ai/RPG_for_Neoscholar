#! /usr/lib/python3

from pawn import Actor
from grid import Dir
import copy

class EffectTarget:
    """
    An EffectTarget determines what tiles an active capability can target.

    If 'area_grid' isn't None, it is a 2D grid that shows the effect area.
    The grid has three values, 'x' for effective area, 'o' for actor's position, and ' ' for unaffected tiles.
    For example, the following grid hits in a T shape:
    area_grid = [['x', 'x', 'x'],
                 [' ', 'x', ' '],
                 [' ', 'o', ' ']]
    This may be a directional attack if 'area_directional' is True (so can be rotated in 4 directions);
    otherwise it is a radial attack and cannot be rotated. (The provided direction is assumed to be facing North)
    If 'area_multi_target' is not True, the attack can only hit one target.
    If 'area_connected' is not True, the attack can be blocked by the world.
    An tile of attack is blocked if there is no connection from it to the actor in any cardinal direction.

    If 'use_target_func' is True, instead of consulting the area_grid, the target_func is called and its targets are used.
    """
    area_grid = None
    area_directional = True
    area_multi_target = True
    area_connected = False

    use_target_func = False
    def target_func(self, actor: Actor):
        "Returns a list of targets valid for this EffectTarget."
        pass

    def get_rotated_grid(self, dir: Dir):
        "Returns a rotated grid of this EffectTarget by a direction."
        if not self.area_grid:
            return None
        elif self.area_directional:
            rotated_grid = copy.deepcopy(self.area_grid) # Defaults to North
            if dir == dir.WEST:
                rotated_grid = list(zip(*rotated_grid[::-1])) # This magic looking piece of work rotates the list clockwise.
            elif dir == dir.SOUTH:
                rotated_grid = list(zip(*rotated_grid[::-1])) # Do it twice to do 180 degrees
                rotated_grid = list(zip(*rotated_grid[::-1]))
            elif dir == dir.EAST:
                rotated_grid = list(zip(*rotated_grid))[::-1] # This rotates CCW
            return rotated_grid
        else:
            return self.area_grid

    def get_start_pos(self):
        "Calculates, caches and returns the starting index of the area grid."
        if not self.start_pos:
            for i in range(len(self.area_grid)):
                for j in range(len(self.area_grid[i])):
                    if self.area_grid[i][j] == 'o':
                        self.start_pos = (i, j)
                        break
        return self.start_pos

    def get_targets(self, actor: Actor, dir: Dir):
        "Returns the targets of this EffectTarget."
        if self.use_target_func:
            return target_func(actor)
        if self.area_grid:
            rotated_grid = self.get_rotated_grid(dir)
            start_tile = actor.tile
            start_pos = self.get_start_pos()

            if self.area_connected:
                pass # TODO do some funky pathing algorithm here
            
            # TODO finish getting targets

class Capability:
    """
    A Capability is an attribute of an Actor.
    A Capability has an intensity and duration value.
    If 'is_active' is True, the capability may be used actively.
    if 'is_timed' is True, the capability lasts a limited amount of turns. A duration of 0 indicates infinite duration.
    A capabilities can have certain triggers, which are string phrases that cause functions to be called.
    """
    is_active = False
    is_timed = False
    triggers = {}
    effecttarget: EffectTarget = None

    def __init__(self, actor: Actor, intensity=0, duration=0):
        self.actor = actor
        self.intensity = intensity
        self.duration = duration

    def check_trigger(self, trigger: str):
        "Fires a trigger if it exists."
        if trigger in triggers:
            triggers[trigger](self)

    def activate(self):
        "Called when an actor activates a capability."
        pass

    def on_timeout(self):
        "Called when the capability's duration is over."
        pass

    def on_turn_start(self):
        "Called when an actor starts their action."
        pass

    def on_turn_end(self):
        "Called when an actor ends their action."
        pass

    def advance_turn(self):
        "Handles capability duration."
        if self.is_timed and self.duration > 0:
            self.duration -= 1
            if self.duration <= 0:
                self.on_timeout(self.actor)
                self.actor.capabilities.remove(self)

class CAP_HealthRegen(Capability):
    """
    This capability restores some health to the actor at the end of a turn.
    """

    def on_turn_end(self):
        self.actor.health = min(self.actor.health_max, self.actor.health + self.intensity)