import pygame
from grid import MapGrid
import Player
import Enemy
import World_module
import Npc
import Task


def level1(window_size_x, window_size_y, surface):
    grid = MapGrid(30, 20)

    player_group = pygame.sprite.Group()
    enemy_group1 = pygame.sprite.Group()

    player_group.add(Player.boy((5, 10), grid))
    player_group.add(Player.boy((8, 10), grid))
    enemy_group1.add(Enemy.zombie((20, 10), grid))
    enemy_group1.add(Enemy.zombie((18, 10), grid))

    enemy_group2 = pygame.sprite.Group()
    enemy_group2.add(Enemy.zombie((20, 10), grid))
    enemy_group2.add(Enemy.zombie((18, 10), grid))

    player_team = Player.Player_team(player_group, (5, 10), grid)
    enemies_team = Enemy.Enemies_team(enemy_group1, (10, 10), grid)

    npc_teams = pygame.sprite.Group()
    npc_teams.add(enemies_team)
    npc_teams.add(Enemy.Enemies_team(enemy_group2, (15, 5), grid))
    tasks = [Task.Battle_Task('kill monster', 'zombie', 4), Task.Collect_Task('collect', 'key', 1)]
    npc_teams.add(Npc.Task_npc((20, 10), grid, tasks))

    dialogs = ['I can\'t tell you too much now',
               'But you may try finishing some simple task first',
               'Now choose a task you want to finish']

    plot = ['When you wake up, you find that you are in a dangerous world full of zombies',
            'You find that there is a normal person not far away',
            'You decide to ask him what happened']

    world_manager = World_module.init_world((window_size_x, window_size_y), surface, player_team,
                                            npc_teams, dialogs=dialogs, plot=plot)

    return world_manager
