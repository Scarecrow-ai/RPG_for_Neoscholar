#! /usr/lib/python3

from damage import DamageInfo, DamageType
from pawn import Actor
from grid import Dir
import copy

class EffectTarget:
    """
    An EffectTarget determines what tiles an active capability can target.

    If 'area_grid' isn't None, it is a 2D square grid that shows the effect area.
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
    area_grid = None # must be a square!
    area_grid_size = 0
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
            return self.target_func(actor)
        if self.area_grid:
            rotated_grid = self.get_rotated_grid(dir)
            start_pos = self.get_start_pos()
            grid_size = actor.tile.grid.size
            
            #   [ , , , , , , ]
            #   [ , , x x x x ]
            #   [ , , . x x . ]
            #   [ , , . o . . ]
            #   [ , , . . . . ]
            #   actor.tile.position = (3, 3)
            #   start_pos = (2, 1)
            grid_row_start = max(0, actor.tile.position[0] - start_pos[0])
            grid_row_end = min(grid_size[0], actor.tile.position[0] + (self.area_grid_size - start_pos[0]))
            grid_col_start = max(0, actor.tile.position[1] - start_pos[1])
            grid_col_end = min(grid_size[1], actor.tile.position[1] + (self.area_grid_size - start_pos[1]))
            targets = []
            for i in range(grid_row_start, grid_row_end):
                for j in range(grid_col_start, grid_col_end):
                    if rotated_grid[i][j] == 'x' and actor.tile.grid[i][j].holding:
                        targets.append(actor.tile.grid[i][j].holding)
            if self.area_connected:
                pass # TODO do some funky pathing algorithm here
            if not self.area_multi_target and len(targets) > 1:
                return targets[0] # return one target; TODO choose closest?
            return targets

class ET_OneAhead(EffectTarget):
    "Hits one tile ahead."
    area_grid = [['x', ' '],
                 ['o', ' ']]
    area_grid_size = 2
    area_directional = True

class ET_TwoAhead(EffectTarget):
    "Hits two tiles ahead."
    area_grid = [[' ', 'x', ' '],
                 [' ', 'x', ' '],
                 [' ', 'o', ' ']]
    area_grid_size = 3
    area_directional = True

class Capability:
    """
    A Capability is an attribute of an Actor, and has an intensity and duration value.
    If 'is_active' is True, the capability may be used actively.
    Capabilities can have certain triggers, which are string phrases that cause functions to be called.
    """
    is_active = False
    triggers = {}
    effecttarget: EffectTarget = None

    def __init__(self, actor: Actor, intensity=0, duration=0):
        self.actor = actor
        self.intensity = intensity
        self.duration = duration

    def check_trigger(self, trigger: str, data):
        "Fires a trigger if it exists."
        if trigger in self.triggers:
            self.triggers[trigger](self, data)

    def activate(self, data):
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
        if self.duration > 0:
            self.duration -= 1
            if self.duration <= 0:
                self.on_timeout(self.actor)
                self.actor.capabilities.remove(self)

class CAP_Attack(Capability):
    "Active, generic attack performed by the actor. Data provided is the direction of the attack."
    is_active = True
    effecttarget = ET_OneAhead()

    def activate(self, data: Dir):
        targets = self.effecttarget.get_targets(self.actor, data)
        for t in targets:
            if t is Actor:
                t.take_damage(DamageInfo(self.actor, self.intensity))

class CAP_Thunder(Capability):
    "Active attack that hits two tiles ahead. The attack does thunder damage."
    is_active = True
    effecttarget = ET_TwoAhead()

    def activate(self, data: Dir):
        targets = self.effecttarget.get_targets(self.actor, data)
        for t in targets:
            if t is Actor:
                t.take_damage(DamageInfo(self.actor, self.intensity, DamageType.DMG_SHOCK))

class CAP_HealthRegen(Capability):
    "Restore some health to the actor at the end of a turn."

    def on_turn_end(self):
        self.actor.health = min(self.actor.health_max, self.actor.health + self.intensity)