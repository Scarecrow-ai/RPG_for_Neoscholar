#! /usr/bin/env python3

import threading
import random

import pygame
import pygame_gui

import Player
import Enemy

# This class is expected to be used directly in the final work with With the modification of player_move and enemy_move
import UI


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
        self.moving = character.use_skill('Swing', random.choice(self.players.sprites()))

    def player_select(self, player):
        if self.selecting.using_skill is None:
            if self.skillButtons is None:
                self.skillButtons = UI.get_skills_button(1000, 100, self.selecting, self.gui_manager)
        elif self.selecting.skill_target is None:
            if self.skillButtons is not None:
                for button in self.skillButtons:
                    button.kill()
                self.skillButtons = None
            if self.targetButtons is None:
                self.targetButtons = UI.get_target_button(1000, 100, self.selecting, self.gui_manager, self.enemies)
        else:
            if self.targetButtons is not None:
                for button in self.targetButtons:
                    button.kill()
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


# A simple function to run the demo, not expected to be used directly in the final work
def demo():
    pygame.init()
    window_size_x = 1280
    window_size_y = 720
    surface = pygame.display.set_mode([window_size_x, window_size_y])

    gui_manager = pygame_gui.UIManager((window_size_x, window_size_y))

    pygame.display.set_caption('BattleDemo')
    background = pygame.transform.scale(pygame.image.load('../Assets/mario_background.png').convert(),
                                        (window_size_x, window_size_y))
    surface.blit(background, (0, 0))

    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    player_group.add(Player.boy((1000, 300)))
    player_group.add(Player.boy((1000, 500)))
    enemy_group.add(Enemy.boy((300, 500)))
    enemy_group.add(Enemy.boy((800, 500)))

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

        surface.blit(background, (0, 0))
        player_group.draw(surface)
        enemy_group.draw(surface)

        gui_manager.draw_ui(surface)
        pygame.display.update()


def check_events(gui_manager):
    ''' A controller of sorts.  Looks for Quit, several simple events.
        Returns: True/False for if a Quit event happened.
    '''

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


if __name__ == '__main__':
    demo()
