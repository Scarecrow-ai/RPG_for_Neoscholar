#! /usr/bin/env python3

import pygame
import pygame_gui
import grid

class Callback_button(pygame_gui.elements.UIButton):
    def __init__(self, size, text, manager, pos=(0, 0)):
        pygame_gui.elements.UIButton.__init__(self, relative_rect=pygame.Rect(pos, size), text=text,
                                              manager=manager)
        self.size = size

    def press(self):
        pass


class Skill_callback_button(Callback_button):
    def __init__(self, skill_name, player, manager, pos=(0, 0)):
        Callback_button.__init__(self, (100, 50), skill_name, manager, pos=pos)
        self.player = player
        self.skill_name = skill_name

    def press(self):
        self.player.use_skill(self.skill_name)


class Target_callback_button(Callback_button):
    def __init__(self, target, player, manager, pos=(0, 0)):
        Callback_button.__init__(self, (100, 50), target.name, manager, pos=pos)
        self.player = player
        self.target = target

    def press(self):
        self.player.choose_target(self.target)

class Task_callback_button(Callback_button):
    def __init__(self, task, task_manager, manager, npc, pos=(0, 0)):
        Callback_button.__init__(self, (100, 50), task.name, manager, pos=pos)
        self.task = task
        self.task_Manager = task_manager
        self.npc = npc

    def press(self):
        self.task_Manager.add_task(self.task)
        self.task_Manager.update_display()
        self.npc.remove_task(self.task)
        self.kill()

class Skip_callback_button(Callback_button):
    def __init__(self, bm, manager, pos=(0, 0)):
        Callback_button.__init__(self, (100, 50), "Skip Moving", manager, pos=pos)
        self.bm = bm

    def press(self):
        self.bm.stepsleft = 0

class Button_list:
    def __init__(self, buttons: list, pos, horizontal=True):
        self.buttons = buttons
        self.pos = pos
        self.horizontal = horizontal
        self.__update_buttons__()

    def set_pos(self, pos):
        self.pos = pos
        self.__update_buttons__()

    def __update_buttons__(self):
        x, y = self.pos
        if self.horizontal:
            for button in self.buttons:
                assert isinstance(button, Callback_button)
                button.set_position((x, y))
                x += button.size[0]
        else:
            for button in self.buttons:
                assert isinstance(button, Callback_button)
                button.set_position((x, y))
                y += button.size[1]

    def kill(self):
        while self.buttons:
            button = self.buttons[0]
            self.buttons.remove(button)
            button.kill()
        del self


class task_display(pygame_gui.elements.ui_text_box.UITextBox):
    def __init__(self, tasks, gui_manager):
        html_text = self.get_html_text(tasks)
        pos = (1000, 10)
        size = (200, 150)
        pygame_gui.elements.ui_text_box.UITextBox.__init__(self, html_text, pygame.Rect(pos, size), gui_manager)

    def update_text(self, tasks):
        self.html_text = self.get_html_text(tasks)
        self.parse_html_into_style_data()
        self.full_redraw()

    def get_html_text(self, tasks):
        html_text = '<font face=’verdana’ color=’#000000’ size=3.5></font>'
        html_text += '<i>Tasks:</i><br>'
        for task in tasks:
            html_text += '<i>' + '    ' + task.name + ':</i><br>'
            html_text += '<b>' + task.text + '</b>' + '<br>'
        return html_text


class plot_display(pygame_gui.elements.ui_text_box.UITextBox):
    def __init__(self, texts, gui_manager):
        html_text = ''
        pos = (370, 600)
        size = (500, 100)
        pygame_gui.elements.ui_text_box.UITextBox.__init__(self, html_text, pygame.Rect(pos, size), gui_manager)
        self.texts = texts
        self.text_count = 0

    def get_html_text(self, text):
        html_text = '<font face=’verdana’ color=’#000000’ size=3.5></font>'
        html_text += '<b>' + text + '</b>' + '<br>'
        return html_text

    def next_text(self):
        if self.text_count < len(self.texts):
            self.html_text = self.get_html_text(self.texts[self.text_count])
            self.parse_html_into_style_data()
            self.full_redraw()
            self.text_count += 1
        else:
            self.text_count = 0
            self.hide()

    def set_texts(self, texts):
        self.texts = texts


def get_skills_button(x, y, player, manager):
    buttons = []
    skill_list = player.get_skills()
    for i in range(0, len(skill_list)):
        buttons.append(Skill_callback_button(skill_list[i], player, manager))
    return Button_list(buttons, (x, y), horizontal=False)


def get_target_button(x, y, player, manager, enemy_group: pygame.sprite.Group):
    buttons = []
    enemy_list = enemy_group.sprites()
    for i in range(0, len(enemy_list)):
        buttons.append(Target_callback_button(enemy_list[i], player, manager))
    return Button_list(buttons, (x, y), horizontal=False)


def get_task_button(x, y, manager, tasks, task_Manager, npc):
    buttons = []
    for task in tasks:
        buttons.append(Task_callback_button(task, task_Manager, manager, npc))
    return Button_list(buttons, (x, y), horizontal=True)

def get_skip_button(x, y, bm, manager):
    buttons = []
    buttons.append(Skip_callback_button(bm, manager))
    return Button_list(buttons, (x, y), horizontal=False)