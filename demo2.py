#! /bin/python3

import threading
import random

from grid import *
from pawn import *
from damage import *
from capability import *
import ui

import pygame
import pygame_gui

class BattleManger:
    _instance_lock = threading.Lock()

    def __init__(self, players, enemies, gui_manager):
        self.gui_manager = gui_manager
        self.players = players
        self.enemies = enemies
        self.moving = None  # A character is moving
        self.characters = players.sprites() + enemies.sprites()
        self.characters.sort(key=lambda character: character.speed, reverse=True)
        self.next_character = 0
        self.selecting = False
        self.targetButtons = None
        self.skillButtons = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(BattleManger, "_instance"):
            with BattleManger._instance_lock:
                if not hasattr(BattleManger, "_instance"):
                    BattleManger._instance = object.__new__(cls)
        return BattleManger._instance

    def update(self):
        if self.selecting:
            self.player_select(self.selecting)
        elif self.moving:
            self.moving = self.moving.update()
        else:
            self.check_corpse()
            if not self.enemies.sprites() or not self.players.sprites():
                return True
            self.change_character()

    def player_move(self, character):
        self.selecting = character

    def enemy_move(self, character):
        self.moving = character.use_skill(random.choice(character.get_skills()))
        character.choose_target(random.choice(self.players.sprites()))

    def player_select(self, player):
        if self.selecting.using_skill is None:
            if self.skillButtons is None:
                self.skillButtons = ui.get_skills_button(1000, 100, self.selecting, self.gui_manager)
        elif self.selecting.skill_target is None:
            if self.skillButtons is not None:
                for button in self.skillButtons:
                    button.kill()
                self.skillButtons = None
            if self.targetButtons is None:
                self.targetButtons = ui.get_target_button(1000, 100, self.selecting, self.gui_manager, self.enemies)
        else:
            if self.targetButtons is not None:
                for button in self.targetButtons:
                    button.kill()
                self.targetButtons = None
            self.moving = self.selecting
            self.selecting = None

    def check_corpse(self):
        for character in self.players:
            if not character.is_alive():
                self.players.remove(character)
                self.characters.remove(character)
                character.kill()
        for character in self.enemies:
            if not character.is_alive():
                self.enemies.remove(character)
                self.characters.remove(character)
                character.kill()

    def change_character(self):
        if self.next_character >= len(self.characters):
            self.next_character = 0
        character = self.characters[self.next_character]
        self.next_character += 1
        assert isinstance(character, Actor) or isinstance(character, Actor)
        if character.IsPlayer: #isinstance(character, Player.Player):
            self.player_move(character)
        else:
            self.enemy_move(character)

def main():
    pygame.init()
    window_size_x = 1280
    window_size_y = 720
    surface = pygame.display.set_mode([window_size_x, window_size_y])
    gui_manager = pygame_gui.UIManager((window_size_x, window_size_y))

    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    grid = MapGrid(8, 8)
    player = Actor("Player", grid.grid[0][0])
    player.IsPlayer = True
    player.capabilities = [
        CAP_Attack(player, 300),
        CAP_Thunder(player, 250)
    ]

    enemy1 = Actor("Enemy 1", grid.grid[3][3])
    enemy1.health_max = 500
    enemy1.health = 500
    enemy1.capabilities = [
        CAP_Attack(enemy1, 150),
    ]

    enemy2 = Actor("Enemy 2", grid.grid[3][0])
    enemy2.health_max = 500
    enemy2.health = 500
    enemy2.capabilities = [
        CAP_Attack(enemy2, 150),
    ]
    enemies = [enemy1, enemy2]

    input_to_dir = {
        'n': Dir.NORTH,
        'e': Dir.EAST,
        's': Dir.SOUTH,
        'w': Dir.WEST,
    }

    player_group.add(player)
    enemy_group.add(enemy1)
    enemy_group.add(enemy2)

    battle_end = False
    battleManger = BattleManger(player_group, enemy_group, gui_manager)

    clock = pygame.time.Clock()

    while not battle_end:
        time_delta = clock.tick(60) / 1000
        quit, click, click2 = check_events(gui_manager)
        if quit:
            break
        if click:
            pass
        if click2:
            pass

        battle_end = battleManger.update()
        gui_manager.update(time_delta)

        #surface.blit(background, (0, 0))
        player_group.draw(surface)
        enemy_group.draw(surface)

        gui_manager.draw_ui(surface)
        pygame.display.update()
    

def check_events(gui_manager):
    quit = False
    click = click2 = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                click = event.pos
            if event.button == 3:
                click2 = event.pos
        gui_manager.process_events(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                event.ui_element.press()
    return quit, click, click2

                
if __name__ == "__main__":
    main()