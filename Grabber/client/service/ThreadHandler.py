import threading


class Thread(threading.Thread):
    def __init__(self, target, *args):
        super(Thread, self).__init__(target=target, args=args)
        self.result = None

    def run(self):
        self.result = self._target(*self._args)
