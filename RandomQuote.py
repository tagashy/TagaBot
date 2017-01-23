# coding: utf8
from __future__ import unicode_literals

import Queue
import time

import requests

import IRC
import message_parsing
import utils


class Troll(IRC.Bot):
    """
    Troll class who respond with random quote
    """

    def __init__(self, parent, username, Target, server, channel_to_reply):
        IRC.Bot.__init__(self, parent, Target, username, server)
        self.queue = Queue.Queue()
        self.channel_to_reply = channel_to_reply

    def init(self):
        """
        init the bot (send i can help you to target)

        :return: Nothing what did you expect
        """
        self.reply("I can help you {} :)".format(self.target), "PRIVMSG")

    def main(self):
        """
        main loop of bot , reply to every Message with a quote and send the conversation to main channel

        :return: Nothing what did you expect
        """
        message = self.queue.get()
        res = self.get_citation()
        self.reply("{}=>{}".format(message.pseudo, message.content), "PUBMSG", target=self.channel_to_reply)
        time.sleep(0.1 * len(res))
        self.reply("{}<={}".format(message.pseudo, res), "PUBMSG", target=self.channel_to_reply)
        self.reply(res, "PRIVMSG")

    @staticmethod
    def get_citation():
        """
        get a random quote

        :return: random quote
        """
        r = requests.get("http://www.quotationspage.com/random.php3")
        return utils.parse_html_balise("a", utils.parse_html_balise("dt", r.text))


def create_troll(message, bot):
    param = message.content.split()
    if message.pseudo.startswith("soufedj"):
        return
    if len(param) != 2:
        if message.msg_type == "PRIVMSG":
            bot.reply("!troll <pseudo|required>", "PRIVMSG", target=message.pseudo)
        else:
            bot.reply("!troll <pseudo|required>", "PUBMSG")
    else:
        if param[1].lower() not in {"hackira", "arod", "dazax", "dvor4x", "notfound", "sambecks", "thanat0s", "gelu",
                                    "geluchat", bot.username, "#root-me"}:
            troll = Troll(bot.parent, bot.username, param[1], bot.server, bot.target)
            reg = message_parsing.Message(pseudo=param[1], msg_type="PRIVMSG")
            bot.parent.add_bot(reg, troll, bot.username, bot.server, bot.target)
            if message.msg_type == "PRIVMSG":
                bot.reply("trolling {} :P".format(param[1]), "PRIVMSG", target=message.pseudo)
            else:
                bot.reply("trolling {} :P".format(param[1]), "PUBMSG")
