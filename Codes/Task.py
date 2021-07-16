import UI


class Task:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.finished = False

    def update_task_status(self, target_list):
        pass


class Battle_Task(Task):
    def __init__(self, name, target_specie, number: int):
        Task.__init__(self, name, "kill " + str(number) + ' ' + target_specie)
        self.target_specie = target_specie
        self.target_number = number

    def update_task_status(self, target):
        print(self.text)
        print(target.name)
        if target.specie == self.target_specie:
            self.target_number -= 1
        if self.target_number <= 0:
            self.finished = True
        else:
            self.text = "kill " + str(self.target_number) + ' ' + self.target_specie
        return self.finished


class Task_Manager:
    def __init__(self, gui_manager):
        self.tasks = []
        self.task_display = UI.task_display(self.tasks, gui_manager)

    def add_task(self, task):
        self.tasks.append(task)

    def update_all_task(self, target):
        for task in self.each_task():
            finished = task.update_task_status(target)
            if finished:
                self.tasks.remove(task)
                del task
        self.task_display.update_text(self.tasks)

    def each_task(self):
        for task in self.tasks:
            yield task
