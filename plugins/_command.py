class Command:
    def __init__(self, client_handler, name, command):
        self.client_handler = client_handler
        self.name = name
        self.command = command

    def get_command(self):
        return "/" + self.name

    def matches(self, string):
        if string.startsWith(self.get_command()):
            return True
        return False

    def execute(self, string):
        self.command(string.split(" ")[1:])

    def command(self, args):
        raise NotImplementedError