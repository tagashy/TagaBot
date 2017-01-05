from __future__ import unicode_literals

import Queue
import time

import requests

import IRC
import utils


class troll(IRC.Bot):
    def __init__(self, parent, username, Target, server, channel_to_reply):
        IRC.Bot.__init__(self, parent, Target, username, server)
        self.queue = Queue.Queue()
        self.channel_to_reply = channel_to_reply

    def init(self):
        self.reply("I can help you {} :)".format(self.target),"PRIVMSG")

    def main(self):
        message = self.queue.get()
        res = self.get_citation()
        self.reply("{}=>{}".format(message.pseudo, message.content),"PUBMSG", target=self.channel_to_reply)
        self.reply("{}<={}".format(message.pseudo, res),"PUBMSG", target=self.channel_to_reply)
        time.sleep(0.1 * len(res))
        self.reply(res,"PRIVMSG")

    @staticmethod
    def get_citation():
        r = requests.get("http://www.quotationspage.com/random.php3")
        return utils.parse_html_balise("a", utils.parse_html_balise("dt", r.text))
