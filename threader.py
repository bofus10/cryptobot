#
# Library to collect coin information
#

import random
import time
from threading import Thread


class Worker_Collector(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        time.sleep(random.randint(1,3))
        print("Thread{}".format(self._threadnum))


for i in range(10):
    t = SomeThread(i)
    t.start()

print("Done")