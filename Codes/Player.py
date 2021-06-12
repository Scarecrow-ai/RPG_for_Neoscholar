# A simple demo to support Battle_Module.py, not expected to be used directly in the final work
import pygame
from Utils import vector_subtraction, vector_norm, vector_division


class Player:
    skills = None
    atk = None
    defense = None
    speed = None

    def use_skill(self, skill):  # Switch-case are not supported.
        return self

    def get_skills(self):
        return list(self.skills.keys())

    def update(self):
        pass

    def lose_hp(self, val):
        pass


class boy(Player, pygame.sprite.Sprite):
    skills = {'Swing': 0, 'Punch': 1}
    atk = 50
    defense = 50
    speed = 4
    max_hp = 1000
    walk_sprites_surf = None
    swing_sprites_surf = None
    punch_sprites_surf = None
    punch_effect_sprite = None
    sit_sprites = None
    death_sprites = None
    name = 'boy'

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.hp = self.max_hp
        if self.walk_sprites_surf is None:
            self.walk_sprites_surf = [
                pygame.transform.scale(pygame.image.load('../Assets/步行1_0_0.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_1_1.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_2_2.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_3_3.png').convert_alpha(), (29, 47))]

            self.swing_sprites_surf = [
                pygame.transform.scale(pygame.image.load('../Assets/swingT1_0_16.png').convert_alpha(), (50, 46)),
                pygame.transform.scale(pygame.image.load('../Assets/swingT1_1_17.png').convert_alpha(), (71, 63)),
                pygame.transform.scale(pygame.image.load('../Assets/swingT1_2_18.png').convert_alpha(), (75, 79))]
            self.punch_sprites_surf = [
                pygame.transform.scale(pygame.image.load('../Assets/容易刺_0_32.png').convert_alpha(), (50, 46)),
                pygame.transform.scale(pygame.image.load('../Assets/容易刺_1_33.png').convert_alpha(), (71, 63)),
            ]
            self.sit_sprites = pygame.transform.scale(pygame.image.load('../Assets/sit_0.png').convert_alpha(),
                                                      (28, 44))

            self.death_sprites = pygame.transform.scale(pygame.image.load('../Assets/S_Holy02.png').convert_alpha(),
                                                        (28, 44))
            self.punch_effect_sprite = pygame.transform.scale(
                pygame.image.load('../Assets/S_Thunder07.png').convert_alpha(),
                (58, 94))

        self.change_sprites(self.sit_sprites)
        self.mask = pygame.mask.from_surface(self.image)
        self.draw_health_bar()
        self.rect = self.image.get_rect(center=pos)
        self.using_skill = None
        self.skill_target = None
        self.dead = False
        self.walk_call_time = 0
        self.walk_pic_count = 0
        self.fire_call_time = 0
        self.fire_pic_count = 0
        self.effect_done = False

    def use_skill(self, skill):  # Switch-case are not supported.
        if self.skills[skill] == 0:
            self.using_skill = 0
        elif self.skills[skill] == 1:
            self.using_skill = 1
        return None

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
                if self.walk_pic_count != 0 or self.walk_call_time != 0:
                    self.walk_call_time = 0
                    self.walk_pic_count = 0
                return self.swing(self.skill_target)
        if self.using_skill == 1:
            if vector_norm(vector_subtraction(self.rect.topleft, self.skill_target.rect.topleft)) < 100:
                self.walk(self.skill_target, False)
                return self
            else:
                if self.walk_pic_count != 0 or self.walk_call_time != 0:
                    self.walk_call_time = 0
                    self.walk_pic_count = 0
                return self.punch(self.skill_target)

    def walk(self, target, direction):  # direction is a bool whether character walk to target
        if direction:
            vector = vector_subtraction(target.rect.topleft, self.rect.topleft)
        else:
            vector = vector_subtraction(self.rect.topleft, target.rect.topleft)
        self.rect.move_ip(vector_division(vector, 0.3 * vector_norm(vector)))
        if self.walk_call_time == 10:
            self.change_sprites(self.walk_sprites_surf[self.walk_pic_count])
            self.image = pygame.transform.flip(self.image, vector[0] > 0, False)
            self.walk_pic_count += 1
            if self.walk_pic_count == len(self.walk_sprites_surf):
                self.walk_pic_count = 0
            self.walk_call_time = 0
        else:
            self.walk_call_time += 1

    def swing(self, target):
        return self.attack_skill(target, self.swing_sprites_surf, 1.5)

    def punch(self, target):
        return self.attack_skill(target, self.punch_sprites_surf, 1.0, effect_sprit=self.punch_effect_sprite)

    def attack_skill(self, target, spirits, power, effect_sprit=None):
        if self.fire_call_time == 10:
            self.change_sprites(spirits[self.fire_pic_count])
            self.image = pygame.transform.flip(self.image, self.rect.left < target.rect.left, False)
            self.fire_pic_count += 1
            if self.fire_pic_count == len(spirits):
                if effect_sprit and not self.effect_done:
                    target.change_sprites(effect_sprit)
                    self.fire_pic_count -= 1
                    self.effect_done = True
                elif effect_sprit and self.effect_done:
                    target.change_sprites(target.sit_sprites)
                    self.effect_done = False
                if self.fire_pic_count == len(spirits):
                    self.fire_pic_count = 0
                    self.fire_call_time = 0
                    self.change_sprites(self.sit_sprites)
                    self.image = pygame.transform.flip(self.image, self.rect.left < target.rect.left, False)
                    target.lose_hp(self.atk * power)
                    self.using_skill = None
                    self.skill_target = None
                    return None
            self.fire_call_time = 0
        else:
            self.fire_call_time += 1
        return self

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

    def __str__(self):
        return 'player'
