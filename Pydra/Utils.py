__author__ = 'Hwaipy'

import queue
import threading


class Communicator:
    def __init__(self, channel, dataFetcher, dataSender):
        self.channel = channel
        self.dataFetcher = dataFetcher
        self.dataSender = dataSender
        self.sendQueue = queue.Queue()

    def start(self):
        self.running = True
        threading._start_new_thread(self.receiveLoop, ())
        threading._start_new_thread(self.sendLoop, ())

    def receiveLoop(self):
        try:
            while self.running:
                self.dataFetcher(self.channel)
        except BaseException as re:
            pass
        finally:
            self.running = False

    def sendLater(self, message):
        self.sendQueue.put(message)

    def sendLoop(self):
        try:
            while self.running:
                message = self.sendQueue.get()
                self.dataSender(self.channel, message)
        except BaseException as e:
            pass
        finally:
            self.running = False


class BlockingCommunicator(Communicator):
    def __init__(self, channel, dataFetcher, dataSender):
        Communicator.__init__(self, channel, self.dataQueuer, dataSender)
        self.dataQueue = queue.Queue()
        self.dataFetcherIn = dataFetcher

    def dataQueuer(self, channel):
        data = self.dataFetcherIn(channel)
        self.dataQueue.put(data)

    def query(self, message):
        self.sendLater(message)
        return self.dataQueue.get()
