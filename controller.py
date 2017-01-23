# coding: utf8
from __future__ import unicode_literals

import IRC
import dispatcher
import learning
import message_parsing
import mythread
import replyer
import users
import utils


class Controller(mythread.Thread):
    """
    master class, control all resource, allow to create or delete new ressource
    """

    def __init__(self):
        mythread.Thread.__init__(self)
        self.users = users.Users()
        self.dispatcher = dispatcher.Dispatcher()
        self.replyer = replyer.Replyer()
        self.socks = []
        self.bots = []
        self.kb = learning.KnowledgeBase()

    def init(self):
        """
        init the controller and start the dispatcher and the replyer

        :return: Nothing what did you expect
        """
        self.dispatcher.start()
        self.replyer.start()

    def join_channel(self, server, username, channel):
        """
        join a IRC channel, use a existent socket if parameter match, if not create a new socket

        :param server: server where channel is located
        :param username: username of the bot
        :param channel: channel to join
        :return: sock which join the server
        """
        for sock in self.socks:
            if sock.server == server and username == sock.username:
                if sock.channel == channel:
                    return sock
                sock.send("JOIN {}\r\n".format(channel))
                print ("[!] channel {} joined on {} with username {}".format(channel, server, username))
                sock = IRC.Socket(self.dispatcher, sock.sock, username, server, channel)
                self.replyer.add_sock(sock)
                return sock
        return self.add_sock(server=server, username=username, channel=channel)

    def add_bot(self, pattern, bot, bot_name=None, server=None, channel=None):
        """
        add new bot to resource pool,

        :param pattern: pattern to transfer Message to bot
        :param bot: the bot object
        :param bot_name: the bot name (used only if server and channel are not None to join a new channel)
        :param server: the server (used only if bot_name and channel are not None to join a new channel)
        :param channel: the channel (used only if server and bot_name are not None to join a new channel)
        :return: Nothing what did you expect
        """
        if bot_name is not None and server is not None and channel is not None:
            self.join_channel(server=server, username=bot_name, channel=channel)
        self.dispatcher.append(bot.queue, pattern)
        self.bots.append(bot)
        bot.start()
        if not bot_name:
            utils.print_message("[!] bot {} added matching {}".format(bot.__class__, pattern))
        else:
            utils.print_message("[!] bot {} added matching {}".format(bot_name, pattern))

    def add_sock(self, server, username, channel):
        """
        add a new socket to pool of resources

        :param server: the server to join
        :param username: the username to use for login into server
        :param channel: the channel to join
        :return: IRC.Socket
        """
        sock = IRC.Socket(self.dispatcher, utils.create_irc_socket(server, username, channel, self.users), username,
                          server, channel)
        self.socks.append(sock)
        sock.start()
        utils.print_message("[!] Sock added in channel {} on {} with username {}".format(channel, server, username))
        self.replyer.add_sock(sock)
        return sock

    def add_bot_listener(self, pattern, bot):
        """
        add a new listener for the bot passed as parameter

        :param pattern: the pattern to match
        :param bot: the who will receive the Message
        :return: Nothing what did you expect
        """
        self.dispatcher.append(bot.queue, pattern)
        utils.print_message("[!] bot {} listener added for pattern {}".format(bot.__class__, pattern))

    def end(self):
        """
        kill all other thread then finish

        :return: Nothing what did you expect
        """
        for bot in self.bots:
            bot.stop()
        for sock in self.socks:
            sock.stop()
        self.replyer.stop()
        self.stop()

    def send_reply(self, username, msg_type, content, target, server):
        """
        create a Message object and send it

        :param username: the username of the bot to send Message
        :param msg_type: the Message type
        :param content: the content of the Message
        :param target: the target (channel/username)
        :param server: the server to reply
        :return: Nothing what did you expect
        """
        self.replyer.queue.put(
            message_parsing.Message(pseudo=username, msg_type=msg_type, content=content, target=target, server=server))
