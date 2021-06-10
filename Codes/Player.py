# A simple demo to support Battle_Module.py, not expected to be used directly in the final work
import pygame


class Player:
    pass


class MarioBright(Player, pygame.sprite.Sprite):
    skills = {'Fire': 1, 'Punch': 2}
    atk = 100
    defense = 50
    speed = 15

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        sprites_surf = pygame.image.load('../Assets/mario_sprites.png').convert()
        self.image = pygame.Surface((29, 47))
        self.image.blit(sprites_surf, (0, 0), (4, 13, 29, 47))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def using_skill(self, skill, target):  # Switch-case are not supported.
        if self.skills[skill] == 1:
            pass
        elif self.skills[skill] == 2:
            pass

    def get_skills(self):
        return self.skills.keys()

