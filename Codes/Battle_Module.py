import pygame

# This class is expected to be used directly in the final work
import Characters
import Monsters


class BattleManger:
    characters = []
    enemies = []

    def __init__(self, characters, enemies):
        self.characters = characters
        self.enemies = enemies

    def update(self):
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
    battleManger = BattleManger([Characters.MarioBright((0, 0))], [])
    print(0)
    while not battle_end:
        clock.tick(60)
        battleManger.update()


if __name__ == '__main__':
    demo()
