# coding=utf-8
from __future__ import unicode_literals

import time

import IRC
import message_parsing
from utils import ConnectionError


class KnowledgeBase(object):
    """
    simple database of word
    """

    def __init__(self):
        self.__data = []
        self.acceptable_short_word = ["js", "rop", "jop", "cop", "asm", "sql", "c++"]

    def append(self, data):
        """
        add a data to KB

        :param data: the data to add
        :return:
        """
        if not isinstance(data, (str, unicode)):
            return
        if data not in self.__data:
            self.__data.append(data)

    def search(self, phrase):

        count = 0
        words = self.split(phrase)
        ret = ""
        ret_count = count
        for data in self.__data:
            for key in self.split(data):
                for word in words:
                    if not (len(word) < 3 or len(key) < 3) and word == key:
                        count += 1
            if count > ret_count:
                ret = data
                ret_count = count
            count = 0
        return ret

    def split(self, phrase):
        tmp = []
        dico = []
        for word in phrase.split("'"):
            tmp += word.split()
        for word in tmp:
            if word.lower() in self.acceptable_short_word or len(word) > 3:
                dico.append(word)
        return dico

    def __str__(self):
        ret = "DATA:\n"
        for data in self.__data:
            ret += data + "\n"
        return ret


class Learner(IRC.Bot):
    """
    learning class for bot (mostly troll)
    """

    def __init__(self, parent, target, username, server):
        IRC.Bot.__init__(self, parent, target, username, server)

    def user_pubmsg(self, message):
        if message.content != "!stop_learning":
            if not message.content[-1:] == "?":
                for user in self.parent.users:
                    message.content=message.content.replace(str(user), "")
                self.parent.kb.append(message.content)
        else:
            ret = "OK learning ended"
            if message.msg_type == "PRIVMSG":
                self.reply(content=ret, msg_type=message.msg_type, target=message.pseudo)
            else:
                self.reply(content=ret, msg_type=message.msg_type, target=message.target)
            self.stop()

    def user_privmsg(self, message):
        self.user_pubmsg(message)


class Helper(IRC.Bot):
    """
    reply with accuracy to message
    """

    def __init__(self, parent, target, username, server, target_to_reply, server_to_reply, username_to_reply_with):
        IRC.Bot.__init__(self, parent, target, username, server)
        self.target_to_reply = target_to_reply
        self.server_to_reply = server_to_reply
        self.username_to_reply_with = username_to_reply_with
        if self.target.startswith("#"):
            self.reply_type = "PUBMSG"
        else:
            self.reply_type = "PRIVMSG"

    def init(self):
        if not self.target.startswith("#"):
            self.reply("I can help you :)", "PRIVMSG")

    def user_privmsg(self, message):
        msg = self.parent.kb.search(message.content)
        if msg == "":
            msg = "sry i don't understand"
        time.sleep(0.1 * len(msg) / 3)
        self.reply("{}=>{}".format(message.pseudo, message.content), self.reply_type, self.username_to_reply_with,
                   self.target_to_reply, self.server_to_reply)

        self.reply("{}<={}".format(message.pseudo, msg), self.reply_type, self.username_to_reply_with,
                   self.target_to_reply, self.server_to_reply)
        self.reply(msg, "PRIVMSG", target=message.pseudo)

    def user_pubmsg(self, message):
        msg = self.parent.kb.search(message.content)
        time.sleep(0.1 * len(msg) / 3)
        if self.target != self.target_to_reply:
            self.reply("{}=>{}".format(message.pseudo, message.content), self.reply_type, self.username_to_reply_with,
                       self.target_to_reply, self.server_to_reply)

            self.reply("{}<={}".format(message.pseudo, msg), self.reply_type, self.username_to_reply_with,
                       self.target_to_reply, self.server_to_reply)

        self.reply(msg, "PUBMSG")


def create_learner(message, bot):
    param = message.content.split()
    username = bot.username
    if len(param) > 1:
        if len(param) == 2:
            server = message.server
            channel = param[1]
        if len(param) == 3:
            server = param[2]
            channel = param[1]
        if len(param) >= 4:
            server = param[2]
            channel = param[1]
            username = param[3]
        reg = message_parsing.Message(server=server, target=channel)
        lrn = Learner(bot.parent, channel, username, server)
        try:
            bot.parent.add_bot(reg, lrn, username, server, channel)
        except ConnectionError as e:
            res = "Learning cannot be start because of {}".format(e)
        else:
            res = "Learning started"
        if message.msg_type == "PRIVMSG":
            bot.reply(res, message.msg_type, target=message.pseudo)
        else:
            bot.reply(res, message.msg_type, target=message.target)


def create_helper(message, bot):
    param = message.content.split()
    username = bot.username
    if len(param) > 1:
        if len(param) == 2:
            server = message.server
            channel = param[1]
        if len(param) == 3:
            server = param[2]
            channel = param[1]
        if len(param) >= 4:
            server = param[2]
            channel = param[1]
            username = param[3]
        if channel == "#root-me":
            if message.msg_type == "PRIVMSG":
                bot.reply("eum no", message.msg_type, target=message.pseudo)
            else:
                bot.reply("eum no", message.msg_type, target=message.target)
            return
        if message.msg_type == "PUBMSG":
            hp = Helper(bot.parent, channel, username, server, message.target, message.server, bot.username)
        else:
            hp = Helper(bot.parent, channel, username, server, message.pseudo, message.server, bot.username)
        if not channel.startswith("#"):
            reg = message_parsing.Message(pseudo=channel, server=server, target=username)
        else:
            reg = message_parsing.Message(server=server, target=channel)
        try:
            bot.parent.add_bot(reg, hp, username, server, channel)
        except ConnectionError as e:
            res = "Helper cannot be start because of {}".format(e)
        else:
            res = "Helper started"
        if message.msg_type == "PRIVMSG":
            bot.reply(res, message.msg_type, target=message.pseudo)
        else:
            bot.reply(res, message.msg_type, target=message.target)
