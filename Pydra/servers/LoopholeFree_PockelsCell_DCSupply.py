__author__ = 'Hwaipy'

from InstrumentServers import InstrumentServer
import threading
import serial
import sys
import Utils
import time

class PCControllerServer(InstrumentServer):
    def __init__(self, name, address, comA, comB):
        super().__init__(name, address, [], {"Output": self.cmdOutput, "Measure": self.cmdMeasure})
        self.dcA = BKDCSupply(comA)
        self.dcB = BKDCSupply(comB)
        self.dcA.remote()
        self.dcB.remote()
        self.outputStatus = False

    def cmdOutput(self, message):
        threading._start_new_thread(self.__outputProcess__, (message,0))

    def __outputProcess__(self,message,useless):
        status = message.content.__getitem__('Status')=='true'
        response = message.response()
        response.content.__setitem__('OutputStatusChanged',status==self.outputStatus)
        setPoints = [[24,24,6], [1,1.5,1], [12,0,0],[3,3,3]]
        if status!=self.outputStatus:
            for i in range(3):
                self.dcA.setVoltage(i, setPoints[0][i])
                self.dcA.setCurrent(i, setPoints[1][i])
                self.dcB.setVoltage(i, setPoints[2][i])
                self.dcB.setCurrent(i, setPoints[3][i])
            self.dcA.__applyVoltage__()
            self.dcB.__applyVoltage__()
            time.sleep(0.5)
            self.dcA.__applyCurrent__()
            self.dcB.__applyCurrent__()
            time.sleep(0.5)

            setPointsA = [[1,0,0],[1,1,0],[1,1,1]] if status else [[1,1,0],[1,0,0],[0,0,0]]
            setPointsB = [[1,0,0],[1,0,0],[1,0,0]] if status else [[1,0,0],[1,0,0],[0,0,0]]
            for loop in range(3):
                setPointsAL = setPointsA[loop]
                setPointsBL = setPointsB[loop]
                for i in range(3):
                    self.dcA.turnOn(i) if setPointsAL[i]==1 else self.dcA.turnOff(i)
                    self.dcB.turnOn(i) if setPointsBL[i]==1 else self.dcB.turnOff(i)
                self.dcA.__applyOutput__()
                self.dcB.__applyOutput__()
                time.sleep(1)
        self.outputStatus=status

    def cmdMeasure(self, message):
        resultsA = self.dcA.measureAll()
        resultsB = self.dcB.measureAll()
        response = message.response()
        response.content.__setitem__("Voltages", resultsA[0]+resultsB[0])
        response.content.__setitem__("Currents", resultsA[1]+resultsB[1])
        response.content.__setitem__("Source", self.name)
        super().sendMessageLater(response)

class BKDCSupply:
    def __init__(self, port):
        self.underlying = DCSupplyBKUnderlying(port)
        self.voltages = [0, 0, 0]
        self.currents = [0, 0, 0]
        self.outputs = [0, 0, 0]
        threading._start_new_thread(self.underlying.start, ())

    def remote(self):
        self.underlying.remote()

    def setVoltage(self, channel, level):
        if channel >= 0 & channel < 3:
            self.voltages[channel] = level

    def setCurrent(self, channel, level):
        if channel >= 0 & channel < 3:
            self.currents[channel] = level

    def turnOn(self, channel):
        if channel >= 0 & channel < 3:
            self.outputs[channel] = True

    def turnOff(self, channel):
        if channel >= 0 & channel < 3:
            self.outputs[channel] = False

    def __applyVoltage__(self):
        self.underlying.setVoltage(self.voltages)

    def __applyCurrent__(self):
        self.underlying.setCurrent(self.currents)

    def __applyOutput__(self):
        self.underlying.setOutput(self.outputs)

    def measureAll(self):
        return self.underlying.measure()


class DCSupplyBKUnderlying:
    def __init__(self, port):
        self.serial = serial.Serial(port, 9600, timeout=1)
        self.communicator = Utils.BlockingCommunicator(self.serial, self.dataFetcher, self.dataSender)

    def start(self):
        self.communicator.start()

    def dataFetcher(self, serialChannel):
        while True:
            data = serialChannel.readline()
            if data.__len__() > 0:
                return str(data, encoding='utf-8')

    def dataSender(self, serialChannel, message):
        serialChannel.write(message.encode('utf-8'))




__clientName__ = 'PC Controller Bob'
__serverPort__ = 20102
__serverAddress__ = '172.16.60.199'
__comA__ = 'COM11'
__comB__ = 'COM12'

if __name__ == '__main__':
    if len(sys.argv) == 4:
        __clientName__ = sys.argv[1]
        __comA__ = sys.argv[2]
        __comB__ = sys.argv[3]
    print("{}, {}, {}".format(__clientName__, __comA__, __comB__))
    server = PCControllerServer(__clientName__, (__serverAddress__, __serverPort__),__comA__,__comB__)
    server.start()
