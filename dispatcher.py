from __future__ import unicode_literals

import Queue

import message_parsing
import mythread
from IRC import Bot


class Dispatcher(mythread.Thread):
    """
    Dispatcher of message class.
    It will take msg from is queue and dispatch them to the correct elems if the message match the pattern
    """

    def __init__(self):
        mythread.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.elems = []

    def append(self, queue, message_form):
        """
        add of new queue to dispatch a message
        :param queue: queue to store message if they match message_form
        :param message_form: pattern to match to put the message to the queue
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
        if isinstance(message, message_parsing.message):
            for el in self.elems:
                param = el[0]
                if param.pseudo is None or param.pseudo == message.pseudo:
                    if param.user_account is None or param.user_account == message.user_account:
                        if param.ip is None or param.ip == message.ip:
                            if param.msg_type is None or param.msg_type == message.msg_type:
                                if param.content is None or param.content in message.content:
                                    if param.target is None or param.target == message.target:
                                        if param.server is None or param.server == "NOT_IMPLEMENTED_YET" or param.server == message.server:
                                            # print "[D] good message"
                                            el[1].put(message)

    def remove(self, target):
        """
        remove a queue from elements
        :param target: the pattern to remove
        :return: Nothing what did you expect
        """
        for el in self.elems:
            if target == el[0]:
                self.elems.remove(el)
                break
