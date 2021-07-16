import sys
import threading
from Battle_Module import init_battle

import pygame.sprite
import pygame_gui

import UI
from grid import *

import Enemy
import Task
import Npc


class WorldManger:
    _instance_lock = threading.Lock()
    window_size = (1280, 720)

    def __init__(self, player_team, npc_teams, gui_manager, surface, background, dialogs, plot):
        self.gui_manager = gui_manager
        self.player_team = player_team
        self.npc_teams = npc_teams
        self.surface = surface
        self.background = background
        self.task_Manager = Task.Task_Manager(gui_manager)
        self.player_collision = None
        self.plot_display = UI.plot_display('', gui_manager)
        self.plot_display.hide()
        self.dialogs = dialogs
        self.plot = plot

    def __new__(cls, *args, **kwargs):
        if not hasattr(WorldManger, "_instance"):
            with WorldManger._instance_lock:
                if not hasattr(WorldManger, "_instance"):
                    WorldManger._instance = object.__new__(cls)
        return WorldManger._instance

    def show_plot(self, text):
        self.plot_display.update_text(text)
        self.plot_display.show()

    def update(self, time_delta):
        gameManager = self
        self.player_team.update()
        for npc in self.npc_teams:
            if self.player_team.tile.position == npc.tile.position:
                if isinstance(npc, Enemy.Enemies_team):
                    gameManager = init_battle(WorldManger.window_size, self.surface, self.player_team.members,
                                              npc, self)
                elif isinstance(npc, Npc.Task_npc):
                    npc.show_task(self.gui_manager, self.task_Manager)
                    self.player_collision = npc
            elif self.player_collision is npc:
                self.player_collision.collision_exit()
                self.player_collision = None
            npc.update()
        self.check_events()
        self.gui_manager.update(time_delta)
        self.draw()
        return gameManager

    def draw(self):
        self.surface.blit(self.background, (0, 0))
        self.player_team.draw(self.surface)
        self.npc_teams.draw(self.surface)
        self.gui_manager.draw_ui(self.surface)

    def next_plot(self):
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player_team.set_target_tile(self.player_team.tile.north)
                elif event.key == pygame.K_s:
                    self.player_team.set_target_tile(self.player_team.tile.south)
                elif event.key == pygame.K_a:
                    self.player_team.set_target_tile(self.player_team.tile.west)
                elif event.key == pygame.K_d:
                    self.player_team.set_target_tile(self.player_team.tile.east)
            # if event.type == pygame.KEYUP:
            #     if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
            #         self.player_team.set_target_tile(self.player_team.tile)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and self.plot_display.visible:
                    self.next_plot()
            if event.type == pygame.QUIT:
                sys.exit()
            self.gui_manager.process_events(event)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    event.ui_element.press()

    def load_World(self):
        background = pygame.transform.scale(pygame.image.load('../Assets/World.jpg').convert(),
                                            WorldManger.window_size)
        self.surface.blit(background, (0, 0))
        return self

    def remove_npc(self, npc):
        self.npc_teams.remove(npc)

    def update_task(self, target):
        self.task_Manager.update_all_task(target)


def init_world(window_size, surface, player_team, enemy_group, dialogs=None, plot=None):
    world_gui_manager = pygame_gui.UIManager(window_size)
    background = pygame.transform.scale(pygame.image.load('../Assets/World.jpg').convert(), window_size)
    surface.blit(background, (0, 0))
    worldManger = WorldManger(player_team, enemy_group, world_gui_manager, surface, background, dialogs, plot)
    return worldManger
