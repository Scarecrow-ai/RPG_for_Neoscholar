class Task:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.finished = False


class Task_Manager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def each_task(self):
        for task in self.tasks:
            yield task