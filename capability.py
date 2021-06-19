#! /usr/lib/python3

from pawn import Actor

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