#! /usr/bin/env python3

import pygame
import pygame_gui
from grid import Dir


def get_skills_button(x, y, player, manager):
    buttons = []
    skill_list = player.capabilities #player.get_skills()
    for i in range(0, len(skill_list)):
        buttons.append(skill_button(x, y+50*i, skill_list[i], player, manager))
    return buttons


def get_target_button(x, y, player, manager, enemy_group: pygame.sprite.Group):
    buttons = []
    enemy_list = enemy_group.sprites()
    for i in range(0, len(enemy_list)):
        buttons.append(target_button(x, y+50*i, enemy_list[i], player, manager))
    return buttons


class skill_button(pygame_gui.elements.UIButton):
    def __init__(self, x, y, skill, player, manager):
        pygame_gui.elements.UIButton.__init__(self, relative_rect=pygame.Rect((x, y), (100, 50)), text=skill.name,
                                              manager=manager)
        self.player = player
        self.skill = skill

    def press(self):
        self.player.use_capability(self.skill, Dir.NORTH)


class target_button(pygame_gui.elements.UIButton):
    def __init__(self, x, y, target, player, manager):
        pygame_gui.elements.UIButton.__init__(self, relative_rect=pygame.Rect((x, y), (100, 50)), text=target.name,
                                              manager=manager)
        self.player = player
        self.target = target

    def press(self):
        self.player.choose_target(self.target)