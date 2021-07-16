import pygame

from Utils import vector_norm, vector_division
from Animation import Animation
from UI import get_task_button


class npc(pygame.sprite.Sprite):
    walk_sprites_surf = None
    grid = None

    def __init__(self, tile_pos, grid):
        pygame.sprite.Sprite.__init__(self)
        if npc.walk_sprites_surf is None:
            npc.walk_sprites_surf = [
                pygame.transform.scale(pygame.image.load('../Assets/步行1_0_0.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_1_1.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_2_2.png').convert_alpha(), (29, 47)),
                pygame.transform.scale(pygame.image.load('../Assets/步行1_3_3.png').convert_alpha(), (29, 47))]
        if npc.grid is None:
            npc.grid = grid
        self.walk_animation = Animation(self, npc.walk_sprites_surf, 6)
        self.change_sprites(npc.walk_sprites_surf[0])
        self.mask = pygame.mask.from_surface(self.image)
        self.tile = grid.tile_at(tile_pos)
        self.tile.obj_on.append(self)
        self.rect = self.image.get_rect(center=grid.tile_to_pos(self.tile))
        self.target_tile = None

    def update(self):
        if self.target_tile:
            if self.walk(self.target_tile):
                self.target_tile = None

    # return arrived or not
    def walk(self, target_tile):
        animation_down, sprite_changed = self.walk_animation.play()
        if sprite_changed:
            self.face_target(target_tile)
        self.move_to_tile(target_tile)

    def face_target(self, target_tile):
        if self.rect.center[0] == self.grid.tile_to_pos(target_tile)[0]:
            return
        self.image = pygame.transform.flip(self.image, self.rect.center[0] < self.grid.tile_to_pos(target_tile)[0],
                                           False)

    def move_to_tile(self, target_tile):
        arrived = False
        if self in self.tile.obj_on:
            self.tile.obj_on.remove(self)
        if self not in target_tile.obj_on:
            target_tile.obj_on.append(self)
        if self.tile.position != target_tile.position:
            vector = npc(npc.grid.tile_to_pos(target_tile),
                         npc.grid.tile_to_pos(self.tile))
            self.rect.move_ip(vector_division(vector, 0.3 * vector_norm(vector)))
            self.tile = npc.grid.pos_to_tile(self.rect.center)
        else:
            self.tile = npc.grid.pos_to_tile(self.rect.center)
            self.rect.center = npc.grid.tile_to_pos(self.tile)
            arrived = True
            if self not in self.tile.obj_on:
                self.tile.obj_on.append(self)
        return arrived

    def set_target_tile(self, tile):
        self.target_tile = tile

    def change_sprites(self, sprites):
        length, height = sprites.get_size()
        height += 10
        self.image = pygame.Surface((length, height), pygame.SRCALPHA)
        self.image.blit(sprites, (0, 10), (0, 0, length, height))

    def draw(self, surface):
        assert isinstance(surface, pygame.Surface)
        surface.blit(self.image, self.rect)


class Task_npc(npc):
    def __init__(self, tile_pos, grid, tasks: list, dialogs=None):
        npc.__init__(self, tile_pos, grid)
        self.tasks = tasks
        self.task_list = None
        self.dialogs = dialogs

    def show_task(self, gui_manager, task_Manager):
        x, y = self.grid.tile_to_pos(self.tile)
        if self.task_list is None:
            self.task_list = get_task_button(x - 50, y - 50, gui_manager, self.tasks, task_Manager, self)

    def collision_exit(self):
        self.task_list.kill()
        self.task_list = None

    def remove_task(self, task):
        assert task in self.tasks
        self.tasks.remove(task)
