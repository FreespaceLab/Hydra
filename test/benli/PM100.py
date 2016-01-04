import visa
import sys
#print(pm100.query('SENSE:CORRECTION:WAVELENGTH?'))
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
import matplotlib.animation as animation

def listResources():
    rm = visa.ResourceManager()
    return rm.list_resources()

class PM100:
    def __init__(self,id):
        self.id = id
        self.rm = visa.ResourceManager().open_resource(id)

    def getIdentity(self):
        return self.rm.query('*IDN?')

    def getWavelength(self):
        wl = self.rm.query('SENSE:CORRECTION:WAVELENGTH?')
        return float(wl)

    def setWavelength(self,wavelength):
        self.rm.write('SENSE:CORRECTION:WAVELENGTH {}'.format(wavelength))

    def isAutoRange(self):
        return self.rm.query('SENSE:POWER:DC:RANGE:AUTO?')

    def setAutoRange(self,status):
        self.rm.write('SENSE:POWER:DC:RANGE:AUTO {}'.format(1 if status else 0))

    def measure(self):
        return float(self.rm.query('read?')[:-1])

ID_PM200_A = 'USB0::0x1313::0x80B0::P3000997::INSTR'
ID_PM200_B = 'USB0::0x1313::0x80B0::P3000934::INSTR'


def measureLoop():
    for i in range(3600*24*365):
        time.sleep(1)
        pA = pmA.measure()
        pB = pmB.measure()
        contrast = pA/pB
        print('{}--------{}-----------{}'.format(pA,pB,contrast))
        file = open(fileName,'a')
        file.write('{},{},{},{}\n'.format(time.time(),pA,pB,contrast))
        file.close()

def update_line(num, data, line):
    pA = pmA.measure()
    pB = pmB.measure()
    contrast = pA/pB
    print('{}--------{}-----------{}'.format(pA,pB,contrast))
    file = open(fileName,'a')
    file.write('{},{},{},{}\n'.format(time.time(),pA,pB,contrast))
    file.close()
    print(data)
    line.set_data(data[..., :num])
    return line,

if __name__ == '__main__':
    print('go')
#    print(listResources())
#    sys.exit(0)
    fileName = '../data/data{}.txt'.format(time.time())
    print(fileName)
    pmA = PM100(ID_PM200_A)
    pmA.setWavelength(805)
    pmA.setAutoRange(True)
    pmB = PM100(ID_PM200_B)
    pmB.setWavelength(805)
    pmB.setAutoRange(True)
    measureLoop()
