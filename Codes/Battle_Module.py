import threading
import random

import pygame
import Player
import Enemy


# This class is expected to be used directly in the final work with With the modification of player_move and enemy_move
class BattleManger:
    _instance_lock = threading.Lock()

    def __init__(self, players, enemies):
        self.players = players
        self.enemies = enemies
        self.moving = None  # A character is moving
        self.characters = players.sprites() + enemies.sprites()
        self.characters.sort(key=lambda character: character.speed, reverse=True)
        self.next_character = 0

    def __new__(cls, *args, **kwargs):
        if not hasattr(BattleManger, "_instance"):
            with BattleManger._instance_lock:
                if not hasattr(BattleManger, "_instance"):
                    BattleManger._instance = object.__new__(cls)
        return BattleManger._instance

    def update(self):
        if self.moving:
            self.moving = self.moving.update()
        else:
            for character in self.players:
                if character.is_dead():
                    self.players.remove(character)
                    self.characters.remove(character)
            for character in self.enemies:
                if character.is_dead():
                    self.enemies.remove(character)
                    self.characters.remove(character)
            if len(self.enemies.sprites()) == 0 or len(self.players.sprites()) == 0:
                return True
            if self.next_character >= len(self.characters):
                self.next_character = 0
            character = self.characters[self.next_character]
            self.next_character += 1
            assert isinstance(character, Player.Player) or isinstance(character, Enemy.Enemy)
            if isinstance(character, Player.Player):
                self.player_move(character)
            else:
                self.enemy_move(character)

    def player_move(self, character):
        self.moving = character.use_skill('Swing', random.choice(self.enemies.sprites()))

    def enemy_move(self, character):
        self.moving = character.use_skill('Swing', random.choice(self.players.sprites()))


# A simple function to run the demo, not expected to be used directly in the final work
def demo():
    pygame.init()
    window_size_x = 1200
    window_size_y = 622
    surface = pygame.display.set_mode([window_size_x, window_size_y])
    pygame.display.set_caption('BattleDemo')
    background = pygame.image.load('../Assets/mario_background.png').convert()
    surface.blit(background, (0, 0))

    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    player_group.add(Player.boy((1000, 300)))
    player_group.add(Player.boy((1000, 400)))
    enemy_group.add(Enemy.boy((300, 100)))
    enemy_group.add(Enemy.boy((300, 500)))

    battle_end = False
    battleManger = BattleManger(player_group, enemy_group)

    clock = pygame.time.Clock()

    while not battle_end:
        clock.tick(60)
        battle_end = battleManger.update()

        player_group.clear(surface, background)
        enemy_group.clear(surface, background)
        player_group.draw(surface)
        enemy_group.draw(surface)
        pygame.display.flip()

        quit, click, click2 = check_events()
        if quit:
            break
        if click:
            pass
        if click2:
            pass


def check_events():
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

    return quit, click, click2


if __name__ == '__main__':
    demo()
