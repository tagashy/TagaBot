# coding: utf8
from __future__ import unicode_literals

import Queue

import message_parsing
import mythread
from IRC import Bot


class Dispatcher(mythread.Thread):
    """
    Dispatcher of Message class.
    It will take msg from is queue and dispatch them to the correct elems if the Message match the pattern
    """

    def __init__(self):
        mythread.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.elems = []

    def append(self, queue, message_form):
        """
        add of new queue to dispatch a Message

        :param queue: queue to store Message if they match message_form
        :param message_form: pattern to match to put the Message to the queue
        :return: Nothing what did you expect
        """
        if isinstance(queue, Bot):
            queue = queue.queue
        self.elems.append((message_form, queue))

    def main(self):
        """
        Main loop of the boot once it is start

        :return: Nothing what did you expect
        """
        message = self.queue.get()
        print ("[D] received {}".format(message))
        if isinstance(message, message_parsing.Message):
            for el in self.elems:
                param = el[0]
                if param.pseudo is None or param.pseudo == message.pseudo:
                    if param.user_account is None or param.user_account == message.user_account:
                        if param.ip is None or param.ip == message.ip:
                            if param.msg_type is None or param.msg_type == message.msg_type:
                                if param.content is None or param.content in message.content:
                                    if param.target is None or param.target == message.target:
                                        if param.server is None or param.server == "NOT_IMPLEMENTED_YET" or param.server == message.server:
                                            # print "[D] good Message"
                                            el[1].put(message)

    def remove(self, target):
        """
        remove a queue from elements

        :param target: the pattern to remove
        :return: Nothing what did you expect
        """
        if isinstance(target , message_parsing.Message):
            for el in self.elems:
                if target == el[0]:
                    self.elems.remove(el)
                    break
        else:
            for el in self.elems:
                if target == el[1]:
                    self.elems.remove(el)
