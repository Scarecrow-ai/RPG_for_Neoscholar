import pygame
import Level


def Main():
    pygame.mixer.init()
    pygame.init()
    window_size_x = 1280
    window_size_y = 720
    surface = pygame.display.set_mode([window_size_x, window_size_y])
    pygame.display.set_caption('RPG')
    game_Manager = Level.level1(window_size_x, window_size_y, surface)
    clock = pygame.time.Clock()

    while True:
        time_delta = clock.tick(60) / 1000
        game_Manager = game_Manager.update(time_delta)
        pygame.display.update()


if __name__ == '__main__':
    Main()
