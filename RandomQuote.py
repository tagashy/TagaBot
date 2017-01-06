# coding: utf8
from __future__ import unicode_literals

import Queue
import time

import requests

import IRC
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
        self.reply("I can help you {} :)".format(self.target),"PRIVMSG")

    def main(self):
        """
        main loop of bot , reply to every Message with a quote and send the conversation to main channel
        :return: Nothing what did you expect
        """
        message = self.queue.get()
        res = self.get_citation()
        self.reply("{}=>{}".format(message.pseudo, message.content),"PUBMSG", target=self.channel_to_reply)
        self.reply("{}<={}".format(message.pseudo, res),"PUBMSG", target=self.channel_to_reply)
        time.sleep(0.1 * len(res))
        self.reply(res,"PRIVMSG")

    @staticmethod
    def get_citation():
        """
        get a random quote
        :return: random quote
        """
        r = requests.get("http://www.quotationspage.com/random.php3")
        return utils.parse_html_balise("a", utils.parse_html_balise("dt", r.text))
