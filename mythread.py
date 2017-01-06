#  coding: utf8
from __future__ import unicode_literals

import threading
import Queue

class Thread(threading.Thread):
    """
    override of threading.Thread to offer a stop mechanism, a queue from default a
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.started = False
        self.error = None
        self.pause = False
        self._stop = threading.Event()
        self.queue=Queue.Queue()


    def stop(self):
        """
        tell the thread to stop when he finish his current job
        :return: Nothing
        """
        self._stop.set()

    def stopped(self):
        """
        check if the bot has been stopped
        :return:
        """
        return self._stop.isSet()

    def end(self):
        """
        method call when bot end
        :return:
        """
        print ("ENDING")
        exit(0)

    def init(self):
        """
        method called before entering main loop, allow to make initialisation of stuff
        :return:
        """
        pass

    def run(self):
        """
        main loop of thread,will exec init, then run main in loop until the thread is stopped, then it called end
        :return:
        """
        self.init()
        self.started = True
        while not self.stopped():
            self.main()
        self.end()

    def main(self):
        """
        main loop
        :return:
        """
        pass
