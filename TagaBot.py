# coding: utf8
from __future__ import unicode_literals

import IRC
import learning
import transfert_class
from action import Command, command_loop
from utils import print_message
import RandomQuote
import action

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
        reply = command_loop(message, self.cmds, self)
        if not reply:
            print_message("[" + message.msg_type + "] USER: " + message.pseudo + " send: " + message.content)


def commands_init():
    """
    initialisation of the commands supported by the bot

    :return: Nothing what did you expect
    """
    cmds = list()
    cmds.append(Command(["!transfert"], transfert_class.create_transferer, "TRANSFERT",
                        args=[("server", "require"), ("#channel", "require"), ("public/publique", "optional")]))
    #cmds.append(Command(["!learn"], learning.create_learner, "LEARNER",
    #                    args=[("#channel", "require"), ("server", "optional"), ("name", "optional")]))
    #cmds.append(Command(["!helper"], learning.create_helper, "HELPER",
    #                    args=[("target(#channel/username)", "require"), ("server", "optional"), ("name", "optional")]))
    cmds.append(Command(["!quotes"], RandomQuote.create_troll, "RANDOM QUOTE", args=[("target", "require")]))
    cmds.append(Command(["!speak"], action.speak, "SPEAK", args=[("target", "require"),("content","require")]))
    cmds.append(Command(["!h2s"], action.h2s, "HEX2STRING", args=[("hexstring", "require")]))

    return cmds
