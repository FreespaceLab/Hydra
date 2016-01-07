__author__ = 'Benli'
__version__ = 'v1.0.20160105'

from Instruments import DeviceException,VISAInstrument
import time

class PM200(VISAInstrument):
    manufacturer = 'Thorlabs'
    model = 'PM200'

    def __init__(self, resourceID):
        super().__init__(resourceID,1)
        self.setLineFrequency()

    def getIdentity(self):
        idn = self.scpi._IDN.query()
        if idn is None:
            return [''] * 4
        if len(idn) is 0:
            return [''] * 4
        idns = idn.split(',')
        while len(idns) < 4:
            idns.append('')
        return idns[:4]

    def getWavelength(self, channel):
        self.checkChannel(channel)
        wl = self.scpi.SENSE.CORRECTION.WAVELENGTH.query()
        return float(wl)

    def setWavelength(self, channel, wavelength):
        self.checkChannel(channel)
        wavelengthI = wavelength * 100 // 1 / 100
        self.scpi.SENSE.CORRECTION.WAVELENGTH.write(wavelengthI)
        wavelengthC = self.getWavelength(channel)
        if wavelengthI != wavelengthC:
            raise DeviceException('Wavelength {} out of range.'.format(wavelength))

    def isAutoRange(self, channel):
        self.checkChannel(channel)
        return self.scpi.SENSE.POWER.DC.RANGE.AUTO.query() == '1'

    def setAutoRange(self, channel, status):
        self.checkChannel(channel)
        self.scpi.SENSE.POWER.RANGE.AUTO.write(1 if status else 0)

    def getMeasureRange(self, channel):
        self.checkChannel(channel)
        return self.scpi.SENSE.POWER.DC.RANGE.query()

    def setMeasureRange(self, channel, measureRange):
        self.checkChannel(channel)
        self.scpi.SENSE.POWER.RANGE.write(measureRange)

    def beeper(self):
        self.scpi.SYSTem.BEEPer.write()

    def getAveragingRate(self, channel):
        self.checkChannel(channel)
        return int(self.scpi.SENSe.AVERage.COUNt.query())

    def setAveragingRate(self, channel, averagingRate):
        self.checkChannel(channel)
        self.scpi.SENSe.AVERage.COUNt.write(averagingRate)

    def getBandWidthFilterStatus(self, channel):
        self.checkChannel(channel)
        return self.scpi.INPut.FILTer.query() == '1'

    def setBandWidthFilterStatus(self, channel, status):
        self.checkChannel(channel)
        self.scpi.INPut.FILTer.write(1 if status else 0)

    def getBeamDiameter(self, channel):
        self.checkChannel(channel)
        return self.scpi.SENSE.CORRECTION.BEAMdiameter.query()

    def setBeamDiameter(self, channel, diameter):
        self.checkChannel(channel)
        self.scpi.SENSE.CORRECTION.BEAMdiameter.write(diameter)

    def measure(self, channel):
        self.checkChannel(channel)
        return float(self.scpi.MEASure.query())

    def reset(self):
        self.scpi._RST.write()

    def setLineFrequency(self):
        return self.scpi.SYSTem.LFRequency.write(50)

    def __getSensorInfo__NotComplete(self):
        si = self.scpi.SYSTem.SENsor.IDN.query()
        print(si)
        # sis=re.split(',',si[:-1])
        # print(sis)
        # sibin=bin(int(sis[5]))
        # if sibin＆(1<<5)
        return si

if __name__ == '__main__':
    print('go')
    id = 'USB0::0x1313::0x80B0::P3000997::INSTR'
    pm = PM200.connect(id)
    print(pm.getWavelength(0))
    time.sleep(2)