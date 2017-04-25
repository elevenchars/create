class Command:
    def __init__(self, name, command):
        self.name = name
        self.command = command

    def get_command(self):
        return "/" + self.name
