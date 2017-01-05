from __future__ import unicode_literals

import IRC
import dispatcher
import message_parsing
import mythread
import replyer
import users
import utils


class Controler(mythread.Thread):
    def __init__(self):
        mythread.Thread.__init__(self)
        self.users = users.Users()
        self.dispatcher = dispatcher.Dispatcher()
        self.replyer = replyer.Replyer()
        self.socks = []
        self.bots = []

    def init(self):
        self.dispatcher.start()
        self.replyer.start()

    def join_channel(self, server, username, channel):
        for sock in self.socks:
            if sock.server == server and username == sock.username:
                sock.send("JOIN {}\r\n".format(channel))
                print "[!] channel {} joined on {} with username {}".format(channel, server, username)
                return sock
        return self.add_sock(server=server, username=username, channel=channel)

    def add_bot(self, pattern, bot, bot_name=None, server=None, channel=None):
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
        sock = IRC.Socket(self.dispatcher, utils.create_irc_socket(server, username, channel, self.users), username,
                          server, channel)
        self.socks.append(sock)
        sock.start()
        utils.print_message("[!] Sock added in channel {} on {} with username {}".format(channel, server, username))
        self.replyer.add_sock(sock)
        return sock

    def add_bot_listener(self, pattern, bot):
        self.dispatcher.append(bot.queue, pattern)
        utils.print_message("[!] bot {} listener added for pattern {}".format(bot.__class__, pattern))

    def end(self):
        for bot in self.bots:
            bot.end()

    def send_reply(self, username, msg_type, content, target, server):
        self.replyer.queue.put(
            message_parsing.message(pseudo=username, msg_type=msg_type, content=content, target=target, server=server))
