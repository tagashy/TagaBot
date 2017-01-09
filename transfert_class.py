# coding: utf8
from __future__ import unicode_literals

import random

import IRC
import message_parsing
from utils import ConnectionError


class Transferrer(IRC.Bot):
    """
    Transfer class, it will transfer all message from a channel to another
    """

    def __init__(self, parent, target, bot_name, server_to_reply, bot_name_replyer, couleur=2):
        """
        initialisation of Transfer class

        :param parent: the dispatcher
        :param target: the target to reply to (channel or username)
        :param bot_name: the name of the bot
        :param server_to_reply: the server to reply to
        :param couleur: the color of the message to write
        """
        IRC.Bot.__init__(self, parent, target, bot_name, server_to_reply)
        self.couleur = couleur
        self.invisible_cara = u"\u200B"
        self.bot_name_replyer = bot_name_replyer

    def user_join(self, message):
        """
        method called when user join channel

        :param message: the message received (IRC message object)
        :return:
        """
        self.add_user(message)
        send_res = "User {} has join channel {}".format(message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:],
                                                        message.target)
        # self.send_message(send_res)
        self.reply(send_res, "PRIVMSG", self.bot_name_replyer)

    def user_privmsg(self, message):
        """
        method called when user send a private message

        :param message: the message received (IRC message object)
        :return:
        """
        self.update_user_last_seen(message.pseudo)
        send_res = "Private Message from user {}>{}".format(
            message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:],
            message.content)
        # self.send_message(send_res)
        self.reply(send_res, "PRIVMSG", self.bot_name_replyer)

    def user_pubmsg(self, message):
        """
        method called when user send a public message

        :param message: the message received (IRC message object)
        :return:
        """
        self.update_user_last_seen(message)
        send_res = "{} : {}>{}".format(message.target, message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:],
                                       message.content)
        # self.send_message(send_res)
        self.reply(send_res, "PRIVMSG", self.bot_name_replyer)

    def user_quit(self, message):
        """
        method called when user quit the server

        :param message: the message received (IRC message object)
        :return:
        """
        self.deactivate_user(message)
        send_res = "User {} has quit server with msg : {}".format(
            message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:], message.content)
        # self.send_message(send_res)
        self.reply(send_res, "PRIVMSG", self.bot_name_replyer)

    def user_part(self, message):
        """
        method called when user leave the channel

        :param message: the message received (IRC message object)
        :return:
        """
        self.deactivate_user(message)
        send_res = "User {} has quit channel {} with msg : {}".format(
            message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:], message.target, message.content)
        # self.send_message(send_res)
        self.reply(send_res, "PRIVMSG", self.bot_name_replyer)

    def user_ban(self, message):
        """
        method called when user has been banned

        :param message: the message received (IRC message object)
        :return:
        """
        self.deactivate_user(message)
        send_res = "User {} has been banned from channel {} by {}".format(message.content[0:1] + self.invisible_cara +
                                                                          message.content[1:], message.target,
                                                                          message.pseudo)
        # self.send_message(send_res)
        self.reply(send_res, "PRIVMSG", self.bot_name_replyer)

    def user_kick(self, message):
        """
        method called when user has been kicked

        :param message: the message received (IRC message object)
        :return:
        """
        self.deactivate_user(message)
        send_res = "User {} has been kicked from channel {} by {}".format(message.content[0:1] + self.invisible_cara +
                                                                          message.content[1:], message.target,
                                                                          message.pseudo)
        # self.send_message(send_res)
        self.reply(send_res, "PRIVMSG", self.bot_name_replyer)


def create_transferer(message, bot):
    """
    create a transfer

    :param message: commands line (message_parsing.Message)
    :param bot: the bot
    :return:
    """
    # geting_param
    num_generator = random.Random()
    num_generator.seed()
    param = message.content.split()
    if len(param) >= 3:
        addr = param[1]
        server_addr = addr.split(":")
        if len(server_addr) == 1:
            server_addr = addr
            port = 6667
        elif len(server_addr) == 2:
            port = int(server_addr[1])
            server_addr = server_addr[0]
        else:
            if message.msg_type == "PRIVMSG":
                bot.reply("too much :", message.msg_type, target=message.pseudo)
            else:
                bot.reply("too much :", message.msg_type)
            # print_message("too much :", message.msg_type, message.pseudo, message.target)
            return
        channel = param[2]
        # check existence:
        # create bot
        # transfert_class.Transferrer(bot.dispatcher,)
        reg = message_parsing.Message(server=server_addr, target=channel)
        bot_name = "Guest" + str(num_generator.randint(10000, 99999))
        if message.msg_type == "PRIVMSG":
            tr = Transferrer(bot.parent, message.pseudo, bot_name, bot.server, bot.username)
        else:
            tr = Transferrer(bot.parent, bot.target, bot_name, bot.server, bot.username)
        try:
            bot.parent.add_bot(reg, tr, bot_name, server_addr, channel)
            bot.parent.add_bot_listener(message_parsing.Message(server=server_addr, target=bot_name), tr)
        except ConnectionError as e:
            res = "Transfer cannot be start because of {}".format(e)
        else:
            res = "transfert added"
        if message.msg_type == "PRIVMSG":
            bot.reply(res, message.msg_type, target=message.pseudo)
        else:
            bot.reply(res, message.msg_type, target=message.target)
