# coding: utf8
from __future__ import unicode_literals

import IRC
import action
from action import Command, command_loop
from utils import print_message


class Bot(IRC.Bot):
    def __init__(self, parent, server, username, channel):  # , server, bot_name, channel, port):
        # if channel == "#root-me":
        #    self.error = "BANNED CHANNEL"
        #    exit(0)
        IRC.Bot.__init__(self, parent, channel, username, server)
        self.cmds = commands_init()

    def end(self):
        """
        end the bot
        :return: Nothing what did you expect
        """
        self.reply("va faire une revision", "QUIT")
        exit(0)

    def main(self):
        """
        main loop for the bot
        :return: Nothing what did you expect
        """
        message = self.queue.get()
        reply=command_loop(message, self.cmds, self)
        if not reply:
            print_message("[" + message.msg_type + "] USER: " + message.pseudo + " send: " + message.content)
        else:
            self.reply(reply.content,reply.msg_type)


def commands_init():
    """
    initialisation of the commands supported by the bot
    :return: Nothing what did you expect
    """
    cmds = list()
    cmds.append(Command(["!transfert"], action.create_transferer, "TRANSFERT",
                        args=[("server", "require"), ("#channel", "require"), ("public/publique", "optional")]))
    return cmds
