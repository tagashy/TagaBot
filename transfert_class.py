# coding: utf8
from __future__ import unicode_literals

import IRC
from utils import send_private_message


class Transferrer(IRC.Bot):
    """
    Transfer class, it will transfer all message from a channel to another
    """

    def __init__(self, parent, send_sock, original_chan, pseudo=None, couleur=2):
        IRC.Bot.__init__(self, parent)
        self.pseudo = pseudo
        self.send_sock = send_sock
        self.couleur = couleur
        self.original_chan = original_chan
        self.invisible_cara = u"\u200B"

    def send_message(self, message):
        """
        send a message (obsolete)

        :param message: the content to send
        :return:
        """
        if self.pseudo is not None:
            send_private_message(chr(3) + str(self.couleur) + message, self.pseudo, self.send_sock)
        else:
            send_private_message(chr(3) + str(self.couleur) + message, self.original_chan, self.send_sock)

    def user_join(self, message):
        """
        method called when user join channel

        :param message: the message received (IRC message object)
        :return:
        """
        self.add_user(message)
        send_res = "User {} has join channel {}".format(message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:],
                                                        message.target)
        self.send_message(send_res)

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
        self.send_message(send_res)

    def user_pubmsg(self, message):
        """
        method called when user send a public message

        :param message: the message received (IRC message object)
        :return:
        """
        self.update_user_last_seen(message)
        send_res = "{} : {}>{}".format(message.target, message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:],
                                       message.content)
        self.send_message(send_res)

    def user_quit(self, message):
        """
        method called when user quit the server

        :param message: the message received (IRC message object)
        :return:
        """
        self.deactivate_user(message)
        send_res = "User {} has quit server with msg : {}".format(
            message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:], message.content)
        self.send_message(send_res)

    def user_part(self, message):
        """
        method called when user leave the channel

        :param message: the message received (IRC message object)
        :return:
        """
        self.deactivate_user(message)
        send_res = "User {} has quit channel {} with msg : {}".format(
            message.pseudo[0:1] + self.invisible_cara + message.pseudo[1:], message.target, message.content)
        self.send_message(send_res)

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
        self.send_message(send_res)

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
        self.send_message(send_res)
