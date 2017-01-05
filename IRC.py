from __future__ import unicode_literals

import Queue

import message_parsing
import mythread


class Socket(mythread.Thread):
    def __init__(self, dispatcher, sock, username, server, channel):
        mythread.Thread.__init__(self)
        self.dispatcher = dispatcher
        self.sock = sock
        self.username = username
        self.server = server
        self.channel = channel

    def main(self):
        for msg in self.sock.recv(1024).decode('utf-8', errors='replace').split("\r\n"):
            if msg.startswith("PING"):
                self.sock.send(msg.replace("PING", "PONG") + "\r\n")
            elif msg != "":
                print "[D] {}".format(msg)
                message = message_parsing.parse(msg)
                message.server = self.server
                self.dispatcher.queue.put(message)

    def send(self, message):
        self.sock.send(message.encode('utf-8', errors="replace"))

    def recv(self, size):
        self.sock.recv(size)

    def __str__(self):
        return "IRC:{}:{}>{}".format(self.server, self.channel, self.username)


class Bot(mythread.Thread):
    def __init__(self, parent, target, username, server):
        mythread.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.parent = parent
        self.target = target
        self.username = username
        self.server = server

    def reply(self, content,msg_type, username=None, target=None, server=None):
        if username is None:
            username = self.username
        if target is None:
            target = self.target
        if server is None:
            server = self.server
        self.parent.send_reply(username,msg_type, content, target, server)

    def update_user_last_seen(self, message):
        if self.parent.users.update_user(message.pseudo, message.server, message.target) < 1:
            self.parent.users.add_user(message.pseudo, message.server, message.target)

    def add_user(self, message=None, pseudo=None, server=None, channel=None):
        if message is not None:
            self.parent.users.add_user(message.pseudo, message.server, message.target)
        elif pseudo is not None and server is not None and channel is not None:
            self.parent.users.add_user(pseudo, server, channel)

    def deactivate_user(self, pseudo):
        self.parent.users.deactivate_user(pseudo)

    def main(self):
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
        pass

    def user_privmsg(self, message):
        pass

    def user_pubmsg(self, message):
        pass

    def user_quit(self, message):
        pass

    def user_part(self, message):
        pass

    def user_ban(self, message):
        pass

    def user_kick(self, message):
        pass
