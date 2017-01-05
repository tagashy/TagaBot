from __future__ import unicode_literals

import IRC
import message_parsing
import mythread
from utils import print_message


class Replyer(mythread.Thread):
    def __init__(self):
        mythread.Thread.__init__(self)
        self.socks = []

    def add_sock(self, sock):
        if not isinstance(sock, IRC.Socket):
            raise TypeError
        self.socks.append(sock)
        print_message("[!] adding sock {} to replyer".format(sock))

    def main(self):
        reply = self.queue.get()
        if isinstance(reply, message_parsing.message):
            for sock in self.socks:
                if reply.pseudo == sock.username:
                    if reply.server == sock.server:
                        if not reply.target.startswith("#"):
                            sock.send(reply.construct_message())
                        elif reply.target == sock.channel:
                            sock.send(reply.construct_message())
