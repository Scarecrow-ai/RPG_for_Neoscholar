#! /usr/lib/python3

import pygame
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

class Actor(Pawn, pygame.sprite.Sprite):
    """
    An Actor is a pawn that has a set of capabilities, and has some health and can be hurt.
    Actors inherit Sprites.
    """
    capabilities = []
    health_max = 1000
    speed = 1
    sprites = {}

    def sprite_setup(self):
        self.sprites_walk = [
            pygame.transform.scale(pygame.image.load('Assets/步行1_0_0.png').convert_alpha(), (29, 47)),
            pygame.transform.scale(pygame.image.load('Assets/步行1_1_1.png').convert_alpha(), (29, 47)),
            pygame.transform.scale(pygame.image.load('Assets/步行1_2_2.png').convert_alpha(), (29, 47)),
            pygame.transform.scale(pygame.image.load('Assets/步行1_3_3.png').convert_alpha(), (29, 47))
        ]
        self.sprites_swing = [
            pygame.transform.scale(pygame.image.load('Assets/swingT1_0_16.png').convert_alpha(), (50, 46)),
            pygame.transform.scale(pygame.image.load('Assets/swingT1_1_17.png').convert_alpha(), (71, 63)),
            pygame.transform.scale(pygame.image.load('Assets/swingT1_2_18.png').convert_alpha(), (75, 79))
        ]
        self.sprites_punch = [
                pygame.transform.scale(pygame.image.load('Assets/容易刺_0_32.png').convert_alpha(), (50, 46)),
                pygame.transform.scale(pygame.image.load('Assets/容易刺_1_33.png').convert_alpha(), (71, 63)),
        ]
        self.sprites_death = [pygame.transform.scale(pygame.image.load('Assets/S_Holy02.png').convert_alpha(), (28, 44))],
        self.sprites_sit = [pygame.transform.scale(pygame.image.load('Assets/sit_0.png').convert_alpha(), (28, 44))]

    def __init__(self, name: str, tile: grid.MapTile) -> None:
        Pawn.__init__(self, name, tile)
        pygame.sprite.Sprite.__init__(self)

        self.health = self.health_max
        self.alive = True
        self.sprite_setup()
        self.change_sprites(self.sprites_sit[0])
        self.rect = self.image.get_rect(center=tile.grid.get_tile_pos(self.tile))
        self.mask = pygame.mask.from_surface(self.image)
        self.using_skill = None
        self.skill_target = None

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

    def change_sprites(self, sprites):
        length, height = sprites.get_size()
        height += 10
        self.image = pygame.Surface((length, height), pygame.SRCALPHA)
        self.draw_health_bar()
        self.image.blit(sprites, (0, 10), (0, 0, length, height))

    def draw_health_bar(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 22, 10), 1)
        pygame.draw.rect(self.image, (0, 128, 0), (1, 1, int(self.health / self.health_max * 20), 8))
        pygame.draw.rect(self.image, (255, 0, 0),
                         (int(self.health / self.health_max * 20) + 1, 1, int((self.health_max - self.health) / self.health_max * 20), 8))