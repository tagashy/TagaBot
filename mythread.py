from __future__ import unicode_literals

import threading
import Queue

class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.started = False
        self.error = None
        self.pause = False
        self._stop = threading.Event()
        self.queue=Queue.Queue()


    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def end(self):
        print ("ENDING")
        exit(0)

    def init(self):
        pass

    def run(self):
        self.init()
        self.started = True
        while not self.stopped():
            self.main()
        self.end()

    def main(self):
        pass
