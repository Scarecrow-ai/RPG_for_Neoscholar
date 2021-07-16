import pygame
from grid import MapGrid
import Player
import Enemy
import World_module
import Npc
import Task


def init_characters(grid):
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
    tasks = [Task.Battle_Task('kill monster', 'zombie', 2), Task.Task('collect', '')]
    npc_teams.add(Npc.Task_npc((20, 10), grid, tasks))

    return player_team, npc_teams


# A simple function to run the demo, not expected to be used directly in the final work
def Main():
    pygame.init()
    window_size_x = 1280
    window_size_y = 720
    surface = pygame.display.set_mode([window_size_x, window_size_y])
    pygame.display.set_caption('RPG')
    grid = MapGrid(30, 20)

    player_team, npc_teams = init_characters(grid)
    world_Manager = World_module.init_world((window_size_x, window_size_y), surface, player_team,
                                            npc_teams)
    game_Manager = world_Manager
    clock = pygame.time.Clock()

    while True:
        time_delta = clock.tick(60) / 1000
        game_Manager = game_Manager.update(time_delta)
        pygame.display.update()


if __name__ == '__main__':
    Main()
