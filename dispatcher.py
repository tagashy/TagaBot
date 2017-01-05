from __future__ import unicode_literals

import Queue

import message_parsing
import mythread
from IRC import Bot


class Dispatcher(mythread.Thread):
    def __init__(self):
        mythread.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.elems = []

    def append(self, queue, message_form):
        if isinstance(queue, Bot):
            queue = queue.queue
        self.elems.append((message_form, queue))

    def main(self):
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
                                            #print "[D] good message"
                                            el[1].put(message)

    def remove(self, target):
        for el in self.elems:
            if target == el[0]:
                self.elems.remove(el)
                break
