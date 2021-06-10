import threading
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
        self.characters = players + enemies
        self.characters.sort(key=lambda character: character.speed)
        self.next_character = 0

    def __new__(cls, *args, **kwargs):
        if not hasattr(BattleManger, "_instance"):
            with BattleManger._instance_lock:
                if not hasattr(BattleManger, "_instance"):
                    BattleManger._instance = object.__new__(cls)
        return BattleManger._instance

    def update(self):
        if self.moving:
            self.moving.update()
        else:
            character = self.characters[self.next_character]
            assert isinstance(character, Player.Player) or isinstance(character, Enemy.Enemy)
            if isinstance(character, Player.Player):
                self.player_move(character)
            else:
                self.enemy_move(character)

    def player_move(self, character):
        pass

    def enemy_move(self, character):
        pass


# A simple function to run the demo, not expected to be used directly in the final work
def demo():
    pygame.init()
    window_size_x = 1200
    window_size_y = 622
    surface = pygame.display.set_mode([window_size_x, window_size_y])
    pygame.display.set_caption('BattleDemo')
    background = pygame.image.load('../Assets/mario_background.png').convert()
    surface.blit(background, (0, 0))
    clock = pygame.time.Clock()
    battle_end = False
    battleManger = BattleManger([Player.MarioBright((0, 0))], [Enemy.MarioDark((0, 100))])
    while not battle_end:
        clock.tick(60)
        battleManger.update()


if __name__ == '__main__':
    demo()
