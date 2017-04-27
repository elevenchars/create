import _command
import json

class Command(_command.Command):
    def __init__(self, client_handler):
        _command.Command.__init__(self, client_handler, "echo", self.command)

    def command(self, args):
        self.client_handler.cs.sendall(json.dumps({"type": "message",
                                                "body": "ECHO : " + str(args)}))