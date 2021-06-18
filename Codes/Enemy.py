# A simple demo to support Battle_Module.py, not expected to be used directly in the final work
import pygame
from Utils import vector_subtraction, vector_norm, vector_division
from Animation import Animation


class Enemy:
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


class zombie(Enemy, pygame.sprite.Sprite):
    skills = {'Swing': 0}
    atk = 150
    defense = 50
    speed = 14
    max_hp = 100
    walk_sprites_surf = None
    swing_sprites_surf = None
    sit_sprites = None
    death_sprites = None
    specie = 'zombie'
    init_count = 0

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.hp = self.max_hp
        self.name = zombie.specie + str(zombie.init_count)
        zombie.init_count += 1
        # load sprites
        if zombie.walk_sprites_surf is None:
            sprites = pygame.transform.flip(pygame.image.load('../Assets/zombie.png').convert_alpha(), True, False)
            zombie.walk_sprites_surf = [
                pygame.transform.scale(sprites.subsurface(0, 222, 72, 111), (58, 94)),
                pygame.transform.scale(sprites.subsurface(72, 222, 72, 111), (58, 94)),
                pygame.transform.scale(sprites.subsurface(144, 222, 72, 111), (58, 94)),
                pygame.transform.scale(sprites.subsurface(216, 222, 72, 111), (58, 94))]

            zombie.swing_sprites_surf = [
                pygame.transform.scale(sprites.subsurface(0, 111, 72, 111), (58, 94)),
                pygame.transform.scale(sprites.subsurface(72, 111, 72, 111), (58, 94)),
                pygame.transform.scale(sprites.subsurface(144, 111, 72, 111), (58, 94)),
                pygame.transform.scale(sprites.subsurface(216, 111, 72, 111), (58, 94))]

            zombie.sit_sprites = pygame.transform.scale(sprites.subsurface(0, 333, 72, 111), (58, 94))

            zombie.death_sprites = pygame.transform.scale(pygame.image.load('../Assets/S_Holy02.png').convert_alpha(),
                                                          (28, 44))

        self.swing_animation = Animation(self, zombie.swing_sprites_surf, 6)
        self.walk_animation = Animation(self, zombie.walk_sprites_surf, 6)
        self.change_sprites(zombie.sit_sprites)
        self.mask = pygame.mask.from_surface(self.image)
        self.draw_health_bar()
        self.rect = self.image.get_rect(center=pos)
        self.using_skill = None
        self.skill_target = None
        self.dead = False

    def use_skill(self, skill):  # Switch-case are not supported.
        self.using_skill = self.skills[skill]
        return self

    def choose_target(self, target):
        self.skill_target = target
        return self

    def update(self):
        if self.dead:
            return None
        if self.using_skill == 0:
            if vector_norm(vector_subtraction(self.rect.topleft, self.skill_target.rect.topleft)) > 50:
                self.walk(self.skill_target, True)
                return self
            else:
                return self.swing(self.skill_target)

    def walk(self, target, direction):  # direction is a bool whether character walk to target
        if direction:
            vector = vector_subtraction(target.rect.topleft, self.rect.topleft)
        else:
            vector = vector_subtraction(self.rect.topleft, target.rect.topleft)
        self.rect.move_ip(vector_division(vector, 0.3 * vector_norm(vector)))
        animation_down, sprite_changed = self.walk_animation.play()
        if sprite_changed:
            self.face_target()

    def swing(self, target):
        return self.attack_skill(target, self.swing_animation, 1.5)

    def attack_skill(self, target, animation, power, effect_sprite=None):
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

    def __str__(self):
        return 'Enemy'
