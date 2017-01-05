from __future__ import unicode_literals

import IRC
import action
from action import Command, command_loop
from utils import print_message


class Bot(IRC.Bot):
    def __init__(self, parent, sock):  # , server, bot_name, channel, port):
        # if channel == "#root-me":
        #    self.error = "BANNED CHANNEL"
        #    exit(0)
        IRC.Bot.__init__(self, parent)
        self.cmds = commands_init(self)
        self.sock = sock

    def end(self):
        self.sock.send("QUIT : va faire une revision\r\n")
        self.sock.close()
        exit(0)

    def main(self):
        message = self.queue.get()
        if not command_loop(message, self.sock, self.cmds, self.parent):
            print_message("[" + message.msg_type + "] USER: " + message.pseudo + " send: " + message.content)


def commands_init(bot):
    cmds = []
    cmds.append(Command(["!transfert"], action.create_transferer, "TRANSFERT",
                        args=[("server", "require"), ("#channel", "require"), ("public/publique", "optional")]))
    return cmds
