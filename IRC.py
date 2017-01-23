# coding: utf8
from __future__ import unicode_literals

import Queue

import message_parsing
import mythread


class Socket(mythread.Thread):
    """
    IRC socket to grab Message
    it is a wrapper from classical socket to keep IRC connection alive and transfer Message to his dispatcher
    """

    def __init__(self, dispatcher, sock, username, server, channel):
        mythread.Thread.__init__(self)
        self.dispatcher = dispatcher
        self.sock = sock
        self.username = username
        self.server = server
        self.channel = channel

    def main(self):
        """
        main loop for socket

        :return: Nothing what did you expect
        """
        for msg in self.sock.recv(1024).decode('utf-8', errors='replace').split("\r\n"):
            if msg.startswith("PING"):
                self.sock.send(msg.replace("PING", "PONG") + "\r\n")
            elif msg != "":
                message = message_parsing.parse(msg)
                message.server = self.server
                self.dispatcher.queue.put(message)

    def send(self, message):
        """
        send method of socket

        :param message: Message to send
        :return: Nothing what did you expect
        """
        self.sock.send(message.encode('utf-8', errors="replace"))

    def recv(self, size):
        """
        recv method of socket

        :param size: size of data to receive
        :return: data received by sock
        """
        return self.sock.recv(size)

    def __str__(self):
        return "IRC:{}:{}>{}".format(self.server, self.channel, self.username)


class Bot(mythread.Thread):
    """
    Base class for IRC bot
    """

    def __init__(self, parent, target, username, server):
        mythread.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.parent = parent
        self.target = target
        self.username = username
        self.server = server

    def reply(self, content, msg_type, username=None, target=None, server=None):
        """
        send a Message

        :param content: the content of the Message
        :param msg_type: the type of Message
        :param username: the username of the socket
        :param target: the channel or user to reply to
        :param server: the server to reply to
        :return: Nothing what did you expect
        """
        if username is None:
            username = self.username
        if target is None:
            target = self.target
        if server is None:
            server = self.server
        self.parent.send_reply(username, msg_type, content, target, server)

    def update_user_last_seen(self, message=None, pseudo=None, server=None, channel=None):
        """
        update the last time a user has been seen

        :param message: the Message received by IRC sock (or stuff who countain at least pseudo, server and target attribute) OVERIDE OTHER PARAMS !!!!!
        :param pseudo: the pseudo of the user
        :param server: the server of the user
        :param channel: the channel of the user
        :return: Nothing what did you expect what did you expect
        """
        if message is not None:
            if self.parent.users.update_user(message.pseudo, message.server, message.target) < 1:
                self.parent.users.add_user(message.pseudo, message.server, message.target)
        elif pseudo is not None and server is not None and channel is not None:
            if self.parent.users.update_user(pseudo, server, channel) < 1:
                self.parent.users.add_user(pseudo, server, channel)

    def add_user(self, message=None, pseudo=None, server=None, channel=None):
        """
        add a user to user list

        :param message:the Message received by IRC sock (or stuff who countain at least pseudo, server and target attribute) OVERIDE OTHER PARAMS !!!!!
        :param pseudo: the pseudo of the user
        :param server: the server of the user
        :param channel: the channel of the user
        :return: Nothing what did you expect
        """
        if message is not None:
            self.parent.users.add_user(message.pseudo, message.server, message.target)
        elif pseudo is not None and server is not None and channel is not None:
            self.parent.users.add_user(pseudo, server, channel)

    def deactivate_user(self, pseudo):
        """
        deactivate a user

        :param pseudo: the username of user to deactivate
        :return: Nothing what did you expect
        """
        self.parent.users.deactivate_user(pseudo)

    def main(self):
        """
        main loop to allow callback on specific type of Message

        :return: Nothing what did you expect
        """
        message = self.queue.get()
        self.update_user_last_seen(message)
        if message.msg_type == "PART":
            self.deactivate_user(message.pseudo)
            self.user_part(message)
        elif message.msg_type == "QUIT":
            self.deactivate_user(message.pseudo)
            self.user_quit(message)
        elif message.msg_type == "JOIN":
            self.add_user(message)
            self.user_join(message)
        elif message.msg_type == "PRIVMSG":
            self.update_user_last_seen(message)
            self.user_privmsg(message)
        elif message.msg_type == "PUBMSG":
            self.update_user_last_seen(message)
            self.user_pubmsg(message)
        elif message.msg_type == "KICK":
            self.deactivate_user(message.pseudo)
            self.user_kick(message)
        elif message.msg_type == "BAN":
            self.deactivate_user(message.pseudo)
            self.user_ban(message)

    def user_join(self, message):
        """
        method called when user join channel

        :param message: the message received (IRC message object)
        :return:
        """
        pass

    def user_privmsg(self, message):
        """
        method called when user send a private message

        :param message: the message received (IRC message object)
        :return:
        """
        pass

    def user_pubmsg(self, message):
        """
        method called when user send a public message

        :param message: the message received (IRC message object)
        :return:
        """
        pass

    def user_quit(self, message):
        """
        method called when user quit the server

        :param message: the message received (IRC message object)
        :return:
        """
        pass

    def user_part(self, message):
        """
        method called when user leave the channel

        :param message: the message received (IRC message object)
        :return:
        """
        pass

    def user_ban(self, message):
        """
        method called when user has been banned

        :param message: the message received (IRC message object)
        :return:
        """
        pass

    def user_kick(self, message):
        """
        method called when user has been kicked

        :param message: the message received (IRC message object)
        :return:
        """
        pass

    def end(self):
        self.parent.bots.remove(self)
        self.parent.dispatcher.remove(self)