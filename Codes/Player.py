#! /usr/bin/env python3

# A simple demo to support Battle_Module.py, not expected to be used directly in the final work
import pygame
from Animation import Animation
from Utils import vector_subtraction, vector_norm, vector_division


class Player:
    skills = None
    atk = None
    defense = None
    speed = None

    def use_skill(self, skill):  # Switch-case are not supported.
        pass

    def get_skills(self):
        return list(self.skills.keys())

    def update(self):
        pass

    def lose_hp(self, val):
        pass


class Player_team(pygame.sprite.Sprite):
    walk_sprites_surf = None
    grid = None

    def __init__(self, players, tile_pos, grid):
        pygame.sprite.Sprite.__init__(self)
        self.members = players
        if Player_team.walk_sprites_surf is None:
            Player_team.walk_sprites_surf = [
                pygame.transform.scale(pygame.image.load('../Assets/步行1_0_0.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_1_1.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_2_2.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_3_3.png').convert_alpha(), (29, 47))]
        if Player_team.grid is None:
            Player_team.grid = grid
        self.walk_animation = Animation(self, Player_team.walk_sprites_surf, 6)
        self.change_sprites(Player_team.walk_sprites_surf[0])
        self.mask = pygame.mask.from_surface(self.image)
        self.tile = grid.tile_at(tile_pos)
        self.tile.obj_on.append(self)
        self.rect = self.image.get_rect(center=grid.tile_to_pos(self.tile))
        self.target_tile = None

    def update(self):
        if self.target_tile:
            if self.walk(self.target_tile):
                self.target_tile = None

    # return arrived or not
    def walk(self, target_tile):
        animation_down, sprite_changed = self.walk_animation.play()
        if sprite_changed:
            self.face_target(target_tile)
        self.move_to_tile(target_tile)

    def face_target(self, target_tile):
        if self.rect.center[0] == self.grid.tile_to_pos(target_tile)[0]:
            return
        self.image = pygame.transform.flip(self.image, self.rect.center[0] < self.grid.tile_to_pos(target_tile)[0],
                                           False)

    def move_to_tile(self, target_tile):
        arrived = False
        if self in self.tile.obj_on:
            self.tile.obj_on.remove(self)
        if self not in target_tile.obj_on:
            target_tile.obj_on.append(self)
        if self.tile.position != target_tile.position:
            vector = vector_subtraction(Player_team.grid.tile_to_pos(target_tile),
                                        Player_team.grid.tile_to_pos(self.tile))
            self.rect.move_ip(vector_division(vector, 0.3 * vector_norm(vector)))
            self.tile = Player_team.grid.pos_to_tile(self.rect.center)
        else:
            self.tile = Player_team.grid.pos_to_tile(self.rect.center)
            self.rect.center = Player_team.grid.tile_to_pos(self.tile)
            arrived = True
            if self not in self.tile.obj_on:
                self.tile.obj_on.append(self)
        return arrived

    def set_target_tile(self, tile):
        self.target_tile = tile

    def change_sprites(self, sprites):
        length, height = sprites.get_size()
        height += 10
        self.image = pygame.Surface((length, height), pygame.SRCALPHA)
        self.image.blit(sprites, (0, 10), (0, 0, length, height))

    def draw(self, surface):
        assert isinstance(surface, pygame.Surface)
        surface.blit(self.image, self.rect)


class boy(Player, pygame.sprite.Sprite):
    skills = {'Swing': 0, 'Thunder': 1}
    atk = 40
    defense = 50
    speed = 20
    max_hp = 1000
    walk_sprites_surf = None
    swing_sprites_surf = None
    punch_sprites_surf = None
    punch_effect_sprite = None
    sit_sprites = None
    death_sprites = None
    grid = None
    name = 'boy'

    def __init__(self, tile_pos, grid):
        pygame.sprite.Sprite.__init__(self)
        self.hp = self.max_hp

        # load sprites
        if boy.walk_sprites_surf is None:
            boy.walk_sprites_surf = [
                pygame.transform.scale(pygame.image.load('../Assets/步行1_0_0.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_1_1.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_2_2.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_3_3.png').convert_alpha(), (29, 47))]

            boy.swing_sprites_surf = [
                pygame.transform.scale(pygame.image.load('../Assets/swingT1_0_16.png').convert_alpha(), (50, 46)),
                pygame.transform.scale(pygame.image.load('../Assets/swingT1_1_17.png').convert_alpha(), (71, 63)),
                pygame.transform.scale(pygame.image.load('../Assets/swingT1_2_18.png').convert_alpha(), (75, 79))]
            boy.punch_sprites_surf = [
                pygame.transform.scale(pygame.image.load('../Assets/容易刺_0_32.png').convert_alpha(), (50, 46)),
                pygame.transform.scale(pygame.image.load('../Assets/容易刺_1_33.png').convert_alpha(), (71, 63)),
            ]

            boy.sit_sprites = pygame.transform.scale(pygame.image.load('../Assets/sit_0.png').convert_alpha(),
                                                     (28, 44))

            boy.death_sprites = pygame.transform.scale(pygame.image.load('../Assets/S_Holy02.png').convert_alpha(),
                                                       (28, 44))
            boy.punch_effect_sprite = pygame.transform.scale(
                pygame.image.load('../Assets/S_Thunder07.png').convert_alpha(),
                (58, 94))
        if boy.grid is None:
            boy.grid = grid

        self.swing_animation = Animation(self, boy.swing_sprites_surf, 6)
        self.punch_animation = Animation(self, boy.punch_sprites_surf, 6, effect_sprite=boy.punch_effect_sprite)
        self.walk_animation = Animation(self, boy.walk_sprites_surf, 6)
        self.change_sprites(boy.sit_sprites)
        self.mask = pygame.mask.from_surface(self.image)
        self.tile = grid.tile_at(tile_pos)
        self.tile.obj_on.append(self)
        self.rect = self.image.get_rect(center=grid.tile_to_pos(self.tile))
        self.using_skill = None
        self.skill_target = None
        self.dead = False
        self.goal_tile = None

    def use_skill(self, skill):  # Switch-case are not supported.
        self.using_skill = self.skills[skill]
        return None

    def choose_target(self, target):
        self.skill_target = target
        return self

    def battle_update(self):
        if self.dead:
            return None
        if self.goal_tile is not None:
            i = 1
            target_tile = boy.grid.tile_at((min(boy.grid.size[0] - 1, self.goal_tile.position[0] + i),self.goal_tile.position[1]))
            while len(target_tile.obj_on) != 0 and not (len(target_tile.obj_on) == 1 and self in target_tile.obj_on):
                i -= 1
                target_tile = boy.grid.tile_at((min(boy.grid.size[0] - 1, self.goal_tile.position[0] + i),
                                                self.goal_tile.position[1]))
            if not self.walk(target_tile, False):
                return self
            else:
                self.goal_tile = None
                if self not in self.tile.obj_on:
                    self.tile.obj_on.append(self)
                    return True
        if self.using_skill == 0:
            i = 1
            target_tile = boy.grid.tile_at((min(boy.grid.size[0] - 1, self.skill_target.tile.position[0] + i),
                                            self.skill_target.tile.position[1]))
            while len(target_tile.obj_on) != 0 and not (len(target_tile.obj_on) == 1 and self in target_tile.obj_on):
                i -= 1
                target_tile = boy.grid.tile_at((min(boy.grid.size[0] - 1, self.skill_target.tile.position[0] + i),
                                                self.skill_target.tile.position[1]))
            if not self.walk(target_tile):
                return self
            else:
                if self not in self.tile.obj_on:
                    self.tile.obj_on.append(self)
                return self.swing(self.skill_target)
        if self.using_skill == 1:
            i = 3
            target_tile = boy.grid.tile_at((min(boy.grid.size[0] - 1, self.skill_target.tile.position[0] + i),
                                            self.skill_target.tile.position[1]))
            while len(target_tile.obj_on) != 0 and not (len(target_tile.obj_on) == 1 and self in target_tile.obj_on):
                i -= 1
                target_tile = boy.grid.tile_at((min(boy.grid.size[0] - 1, self.skill_target.tile.position[0] + i),
                                                self.skill_target.tile.position[1]))
            if not self.walk(target_tile):
                return self
            else:
                if self not in self.tile.obj_on:
                    self.tile.obj_on.append(self)
                return self.Thunder(self.skill_target)

    # return arrived or not
    def walk(self, target_tile, avoid = True):
        animation_down, sprite_changed = self.walk_animation.play()
        if sprite_changed:
            self.face_target()
        if (target_tile.position[0] - self.tile.position[0]) > 0:
            next_tile = self.tile.east
        elif (target_tile.position[0] - self.tile.position[0]) < 0:
            next_tile = self.tile.west
        elif (target_tile.position[1] - self.tile.position[1]) > 0:
            next_tile = self.tile.south
        elif (target_tile.position[1] - self.tile.position[1]) < 0:
            next_tile = self.tile.north
        else:
            if self not in self.tile.obj_on:
                self.tile.obj_on.append(self)
            return True
        while avoid and len(next_tile.obj_on) != 0 and not (len(next_tile.obj_on) == 1 and self in next_tile.obj_on):
            next_tile = next_tile.north
        if self not in self.tile.obj_on:
            self.tile.obj_on.append(self)
        self.move_to_tile(next_tile)

    def swing(self, target):
        return self.attack_skill(target, self.swing_animation, 1.5)

    def Thunder(self, target):
        return self.attack_skill(target, self.punch_animation, 1.0)

    def attack_skill(self, target, animation, power):
        next_move = self
        animation_done, sprite_changed = animation.play()
        if sprite_changed:
            self.face_target()
        if animation_done:
            self.sit()
            self.face_target()
            target.lose_hp(power * self.atk)
            self.skill_target = None
            self.using_skill = None
            next_move = None
        return next_move

    def sit(self):
        self.change_sprites(self.sit_sprites)
        self.face_target()

    def change_sprites(self, sprites):
        length, height = sprites.get_size()
        height += 10
        self.image = pygame.Surface((length, height), pygame.SRCALPHA)
        self.draw_health_bar()
        self.image.blit(sprites, (0, 10), (0, 0, length, height))

    def draw_health_bar(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 22, 10), 1)
        pygame.draw.rect(self.image, (0, 128, 0), (1, 1, int(self.hp / self.max_hp * 20), 8))
        pygame.draw.rect(self.image, (255, 0, 0),
                         (int(self.hp / self.max_hp * 20) + 1, 1, int((self.max_hp - self.hp) / self.max_hp * 20), 8))

    def lose_hp(self, val):
        self.hp -= val
        if self.hp <= 0:
            self.dead = True
            self.change_sprites(self.death_sprites)
        self.draw_health_bar()

    def is_dead(self):
        return self.dead

    def face_target(self):
        if self.skill_target is not None:
            self.image = pygame.transform.flip(self.image, self.rect.left < self.skill_target.rect.left, False)

    def move_to_tile(self, target_tile):
        arrived = False
        if self in self.tile.obj_on:
            self.tile.obj_on.remove(self)
        if self not in target_tile.obj_on:
            target_tile.obj_on.append(self)
        if self.tile.position != target_tile.position:
            vector = vector_subtraction(boy.grid.tile_to_pos(target_tile), boy.grid.tile_to_pos(self.tile))
            self.rect.move_ip(vector_division(vector, 0.3 * vector_norm(vector)))
            self.tile = boy.grid.pos_to_tile(self.rect.center)
        else:
            self.tile = boy.grid.pos_to_tile(self.rect.center)
            self.rect.center = boy.grid.tile_to_pos(self.tile)
            arrived = True
            if self not in self.tile.obj_on:
                self.tile.obj_on.append(self)
        return arrived

    def __str__(self):
        return 'player'
