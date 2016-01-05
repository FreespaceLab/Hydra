import visa
import sys
import time

def listResources():
    rm = visa.ResourceManager()
    return rm.list_resources()

class PM200:
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

class PM320:
    def __init__(self,id):
        self.id = id
        self.rm = visa.ResourceManager().open_resource(id)

    def getIdentity(self):
        return self.rm.query('*IDN?')

    def getWavelength(self,channel):
        wl = self.rm.query(':WAVEL{}:VAL?'.format(channel))
        return float(wl)

    def setWavelength(self,channel,wavelength):
        self.rm.write(':WAVEL{}:VAL {}'.format(channel,wavelength))

    def setAutoRange(self,channel):
        self.rm.write(':PRANGE{} AUTO'.format(channel))

    def measure(self,channel):
        return float(self.rm.query(':POW{}:VAL?'.format(channel)))

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
    print(listResources())
