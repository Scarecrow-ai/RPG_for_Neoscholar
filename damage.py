#! /usr/lib/python3

from grid import MapTile
from enum import *

class DamageType(Flag):
    "An enum that represents damage type."
    # physical
    DMG_GENERIC = auto()
    DMG_SLASH = auto()
    DMG_BLUNT = auto()
    # magical
    DMG_BURN = auto()
    DMG_FREEZE = auto()
    DMG_SHOCK = auto()

class DamageInfo:
    """
    A class that represents an instance of damage.
    """
    def __init__(self, attacker, damage: int, type: DamageType = DamageType.DMG_GENERIC, position: MapTile = None):
        self.attacker = attacker
        self.damage = damage
        self.type = type
        self.position = position