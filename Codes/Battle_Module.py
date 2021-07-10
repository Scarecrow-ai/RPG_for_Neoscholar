import sys
import threading
import random
import pygame_gui

from grid import *

import Player
import Enemy

# This class is expected to be used directly in the final work with With the modification of player_move and enemy_move
import UI


class BattleManger:
    _instance_lock = threading.Lock()

    def __init__(self, players, enemy_team, gui_manager, surface, background, world_Manager):
        self.gui_manager = gui_manager
        self.players = players
        self.enemy_team = enemy_team
        self.enemies = enemy_team.members
        self.moving = None  # A character is moving
        self.characters = players.sprites() + self.enemies.sprites()
        self.characters.sort(key=lambda character: character.speed, reverse=True)
        self.next_character = 0
        self.selecting = False
        self.targetButtons = None
        self.skillButtons = None
        self.surface = surface
        self.background = background
        self.world_Manager = world_Manager

    def __new__(cls, *args, **kwargs):
        if not hasattr(BattleManger, "_instance"):
            with BattleManger._instance_lock:
                if not hasattr(BattleManger, "_instance"):
                    BattleManger._instance = object.__new__(cls)
        return BattleManger._instance

    def update(self, time_delta):
        if self.selecting:
            self.player_select(self.selecting)
        elif self.moving:
            self.moving = self.moving.battle_update()
        else:
            self.check_corpse()
            self.change_character()

        self.check_events()
        self.gui_manager.update(time_delta)
        self.draw()
        if not self.enemies.sprites() or not self.players.sprites():
            return self.battle_end()
        else:
            return self

    def player_move(self, character):
        self.selecting = character

    def enemy_move(self, character):
        self.moving = character.use_skill(random.choice(character.get_skills()))
        character.choose_target(self.players.sprites()[len(self.players.sprites()) - 1])

    def player_select(self, player):
        if self.selecting.using_skill is None:
            if self.skillButtons is None:
                self.skillButtons = UI.get_skills_button(1000, 100, self.selecting, self.gui_manager)
        elif self.selecting.skill_target is None:
            if self.skillButtons is not None:
                self.skillButtons.kill()
                self.skillButtons = None
            if self.targetButtons is None:
                self.targetButtons = UI.get_target_button(1000, 100, self.selecting, self.gui_manager, self.enemies)
        else:
            if self.targetButtons is not None:
                self.targetButtons.kill()
                self.targetButtons = None
            self.moving = self.selecting
            self.selecting = None

    def check_corpse(self):
        for character in self.players:
            if character.is_dead():
                self.players.remove(character)
                self.characters.remove(character)
                character.kill()
        for character in self.enemies:
            if character.is_dead():
                self.enemies.remove(character)
                self.characters.remove(character)
                character.kill()

    def change_character(self):
        if self.next_character >= len(self.characters):
            self.next_character = 0
        character = self.characters[self.next_character]
        self.next_character += 1
        assert isinstance(character, Player.Player) or isinstance(character, Enemy.Enemy)
        if isinstance(character, Player.Player):
            self.player_move(character)
        else:
            self.enemy_move(character)

    def battle_end(self):
        self.world_Manager.remove_npc(self.enemy_team)
        return self.world_Manager.load_World()

    def draw(self):
        self.surface.blit(self.background, (0, 0))
        self.players.draw(self.surface)
        self.enemies.draw(self.surface)
        self.gui_manager.draw_ui(self.surface)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            self.gui_manager.process_events(event)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    event.ui_element.press()


def init_battle(window_size, surface, player_group, enemy_group, world_Manager):
    battle_gui_manager = pygame_gui.UIManager(window_size)
    background = pygame.transform.scale(pygame.image.load('../Assets/BackGround.jpg').convert(), window_size)
    surface.blit(background, (0, 0))
    battleManger = BattleManger(player_group, enemy_group, battle_gui_manager, surface, background, world_Manager)
    return battleManger
