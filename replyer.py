# coding: utf8
from __future__ import unicode_literals

import IRC
import message_parsing
import mythread
from utils import print_message


class Replyer(mythread.Thread):
    """
    class designed to search for the good socket and then reply with it
    """
    def __init__(self):
        mythread.Thread.__init__(self)
        self.socks = []

    def add_sock(self, sock):
        """
        add a new IRC socket to pool
        :param sock: the socket to add (IRC sock)
        :return: Nothing what did you expect
        """
        if not isinstance(sock, IRC.Socket):
            raise TypeError
        self.socks.append(sock)
        print_message("[!] adding sock {} to replyer".format(sock))

    def main(self):
        """
        main loop, search for the right socket and send Message through it
        :return: Nothing what did you expect
        """
        reply = self.queue.get()
        if isinstance(reply, message_parsing.Message):
            for sock in self.socks:
                if reply.pseudo == sock.username:
                    if reply.server == sock.server:
                        if not reply.target.startswith("#"):
                            sock.send(reply.construct_message())
                        elif reply.target == sock.channel:
                            sock.send(reply.construct_message())
