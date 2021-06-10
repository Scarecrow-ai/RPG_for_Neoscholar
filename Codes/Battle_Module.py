import threading
import pygame
import Player
import Enemies


# This class is expected to be used directly in the final work
class BattleManger:
    _instance_lock = threading.Lock()
    characters = []
    enemies = []
    round_end = False  # All characters moved at least once.
    characters = []

    def __init__(self, characters, enemies):
        self.characters = characters
        self.enemies = enemies

    def __new__(cls, *args, **kwargs):
        if not hasattr(BattleManger, "_instance"):
            with BattleManger._instance_lock:
                if not hasattr(BattleManger, "_instance"):
                    BattleManger._instance = object.__new__(cls)
        return BattleManger._instance

    def update(self):
        pass

    def player_move(self):
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
    battleManger = BattleManger([Player.MarioBright((0, 0))], [Enemies.MarioDark((0, 100))])
    print(0)
    while not battle_end:
        clock.tick(60)
        battleManger.update()


if __name__ == '__main__':
    demo()
